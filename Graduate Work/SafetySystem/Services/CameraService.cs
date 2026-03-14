using OpenCvSharp;
using Avalonia.Media.Imaging;
using SafetySystem.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace SafetySystem.Services
{
    public class CameraService
    {
        private VideoCapture? _capture;
        private bool _running;
        private Process? _python;

        public event Action<Bitmap, List<DetectionResult>> FrameReady = delegate { };

        public void StartCamera()
        {
            // Запускаем камеру
            _capture = new VideoCapture(0);

            if (!_capture.IsOpened())
                throw new Exception("Не удалось открыть камеру!");

            // Запускаем Python YOLO сервер
            StartPythonYolo();

            _running = true;

            Task.Run(() =>
            {
                var frame = new Mat();

                while (_running)
                {
                    _capture.Read(frame);

                    if (frame.Empty())
                        continue;

                    // Получаем детекции от YOLO
                    var detections = DetectWithYolo(frame);

                    // Рисуем bounding boxes и линию опасной зоны
                    DrawDetections(frame, detections);

                    // Конвертируем в Bitmap для Avalonia
                    var bitmap = ConvertToBitmap(frame);

                    // Отправляем событие в UI
                    FrameReady?.Invoke(bitmap, detections);

                    Thread.Sleep(30);
                }
            });
        }

        public void StopCamera()
        {
            _running = false;
            _capture?.Release();

            if (_python != null && !_python.HasExited)
            {
                _python.Kill();
                _python.Dispose();
            }
        }

        private void StartPythonYolo()
        {
            _python = new Process();

            _python.StartInfo.FileName = "py";
            _python.StartInfo.Arguments = "yolo_server.py";
            _python.StartInfo.UseShellExecute = false;
            _python.StartInfo.RedirectStandardOutput = true;
            _python.StartInfo.RedirectStandardInput = true;
            _python.StartInfo.CreateNoWindow = true;

            _python.Start();
        }

        private List<DetectionResult> DetectWithYolo(Mat frame)
        {
            var detections = new List<DetectionResult>();

            try
            {
                // Кодируем кадр в JPEG и в Base64
                Cv2.ImEncode(".jpg", frame, out var data);
                string base64 = Convert.ToBase64String(data);

                // Отправляем в Python
                if (_python?.StandardInput == null || _python.HasExited)
                    return detections;

                _python.StandardInput.WriteLine(base64);
                _python.StandardInput.Flush();

                // Получаем JSON с детекциями
                string? line = _python.StandardOutput.ReadLine();
                if (string.IsNullOrEmpty(line))
                    return detections;


                if (string.IsNullOrEmpty(line))
                    return detections;

                var boxes = JsonSerializer.Deserialize<List<Dictionary<string,int>>>(line) ?? [];

                int id = 1;

                foreach (var b in boxes)
                {
                    bool danger = b["y"] + b["h"] > 400;

                    detections.Add(new DetectionResult
                    {
                        Id = id++,
                        X = b["x"],
                        Y = b["y"],
                        Width = b["w"],
                        Height = b["h"],
                        InDangerZone = danger
                    });
                }
            }
            catch
            {
                // Игнорируем ошибки (например, если Python не отвечает)
            }

            return detections;
        }

        private static void DrawDetections(Mat frame, List<DetectionResult> detections)
        {
            foreach (var d in detections)
            {
                var color = d.InDangerZone ? Scalar.Red : Scalar.Green;

                Cv2.Rectangle(frame,
                    new Rect(d.X, d.Y, d.Width, d.Height), color, 2);

                Cv2.PutText(frame, $"ID {d.Id}", new Point(d.X, d.Y - 10), HersheyFonts.HersheySimplex, 0.6, color, 2);
            }

            // Линия опасной зоны
            // Cv2.Line(frame, new Point(0, 400), new Point(frame.Width, 400), Scalar.Red, 2);
        }

        private static Bitmap ConvertToBitmap(Mat frame)
        {
            Cv2.ImEncode(".bmp", frame, out var data);
            return new Bitmap(new MemoryStream(data));
        }
    }
}