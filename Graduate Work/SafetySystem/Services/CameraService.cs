using Avalonia.Media.Imaging;
using OpenCvSharp;
using SafetySystem.Models;
using System;
using System.Collections.Concurrent;
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
        private const int PythonStartupTimeoutMs = 30000;
        private const int PythonResponseTimeoutMs = 5000;
        private const double DefaultDangerZoneXRatio = 0.25;
        private const double DefaultDangerZoneYRatio = 0.55;
        private const double DefaultDangerZoneWidthRatio = 0.5;
        private const double DefaultDangerZoneHeightRatio = 0.35;
        private const string PythonReadyMessage = "READY";

        private readonly object _syncRoot = new();
        private readonly ConcurrentQueue<string> _pythonErrorLog = new();
        private DangerZoneRatios _dangerZone = new(
            DefaultDangerZoneXRatio,
            DefaultDangerZoneYRatio,
            DefaultDangerZoneWidthRatio,
            DefaultDangerZoneHeightRatio);
        private VideoCapture? _capture;
        private Process? _python;
        private Task? _startupTask;
        private Task? _cameraTask;
        private CancellationTokenSource? _cancellationTokenSource;

        public event Action<Bitmap, List<DetectionResult>> FrameReady = delegate { };
        public event Action<string, bool> StatusChanged = delegate { };

        public void SetDangerZoneRectPercent(double xPercent, double yPercent, double widthPercent, double heightPercent)
        {
            var x = Math.Clamp(xPercent / 100.0, 0, 0.95);
            var y = Math.Clamp(yPercent / 100.0, 0, 0.95);
            var width = Math.Clamp(widthPercent / 100.0, 0.05, 1.0 - x);
            var height = Math.Clamp(heightPercent / 100.0, 0.05, 1.0 - y);

            lock (_syncRoot)
            {
                _dangerZone = new DangerZoneRatios(x, y, width, height);
            }
        }

        public void StartCamera()
        {
            lock (_syncRoot)
            {
                if (_startupTask is { IsCompleted: false } || _cameraTask is { IsCompleted: false })
                {
                    return;
                }

                _cancellationTokenSource = new CancellationTokenSource();
                _startupTask = Task.Run(() => StartCameraCore(_cancellationTokenSource.Token));
            }
        }

        public void StopCamera()
        {
            Task? startupTask;
            Task? cameraTask;
            Process? python;
            VideoCapture? capture;
            CancellationTokenSource? cancellationTokenSource;

            lock (_syncRoot)
            {
                startupTask = _startupTask;
                cameraTask = _cameraTask;
                python = _python;
                capture = _capture;
                cancellationTokenSource = _cancellationTokenSource;

                _startupTask = null;
                _cameraTask = null;
                _python = null;
                _capture = null;
                _cancellationTokenSource = null;
            }

            if (startupTask is null && cameraTask is null && python is null && capture is null)
            {
                return;
            }

            cancellationTokenSource?.Cancel();

            if (python != null)
            {
                TryStopPythonProcess(python);
            }

            if (startupTask != null)
            {
                try
                {
                    startupTask.Wait(TimeSpan.FromSeconds(2));
                }
                catch (AggregateException)
                {
                }
            }

            if (cameraTask != null)
            {
                try
                {
                    cameraTask.Wait(TimeSpan.FromSeconds(2));
                }
                catch (AggregateException)
                {
                }
            }

            capture?.Release();
            capture?.Dispose();
            cancellationTokenSource?.Dispose();
        }

        private void StartCameraCore(CancellationToken cancellationToken)
        {
            try
            {
                StatusChanged.Invoke("Инициализация камеры...", false);

                var capture = new VideoCapture(0);
                if (!capture.IsOpened())
                {
                    capture.Dispose();
                    throw new Exception("Не удалось открыть камеру.");
                }

                cancellationToken.ThrowIfCancellationRequested();

                lock (_syncRoot)
                {
                    _capture = capture;
                }

                StatusChanged.Invoke("Загрузка модели...", false);

                var python = StartPythonYolo();
                WaitForPythonReady(python, cancellationToken);
                cancellationToken.ThrowIfCancellationRequested();

                lock (_syncRoot)
                {
                    _python = python;
                    _cameraTask = Task.Run(() => CaptureLoop(cancellationToken), cancellationToken);
                }
            }
            catch (OperationCanceledException)
            {
            }
            catch (Exception ex)
            {
                StatusChanged.Invoke($"Ошибка запуска мониторинга: {ex.Message}", true);
                StopCamera();
            }
            finally
            {
                lock (_syncRoot)
                {
                    _startupTask = null;
                }
            }
        }

        private void CaptureLoop(CancellationToken cancellationToken)
        {
            using var frame = new Mat();
            var startupCompleted = false;

            while (!cancellationToken.IsCancellationRequested)
            {
                var capture = _capture;
                if (capture is null)
                {
                    break;
                }

                if (!capture.Read(frame) || frame.Empty())
                {
                    Thread.Sleep(30);
                    continue;
                }

                var dangerZone = GetDangerZoneRect(frame.Width, frame.Height);
                var detections = DetectWithYolo(frame, dangerZone);
                DrawDangerZone(frame, dangerZone);
                DrawDetections(frame, detections);

                var bitmap = ConvertToBitmap(frame);
                if (!startupCompleted)
                {
                    StatusChanged.Invoke("Мониторинг запущен.", false);
                    startupCompleted = true;
                }

                FrameReady.Invoke(bitmap, detections);

                if (cancellationToken.WaitHandle.WaitOne(30))
                {
                    break;
                }
            }
        }

        private static Process StartPythonYolo()
        {
            var python = new Process();
            var scriptPath = ResolveRuntimeFilePath("yolo_server.py");

            python.StartInfo.FileName = "py";
            python.StartInfo.Arguments = $"-u \"{scriptPath}\"";
            python.StartInfo.UseShellExecute = false;
            python.StartInfo.RedirectStandardOutput = true;
            python.StartInfo.RedirectStandardInput = true;
            python.StartInfo.RedirectStandardError = true;
            python.StartInfo.CreateNoWindow = true;
            python.StartInfo.WorkingDirectory = Path.GetDirectoryName(scriptPath) ?? Environment.CurrentDirectory;

            python.Start();
            return python;
        }

        private List<DetectionResult> DetectWithYolo(Mat frame, Rect dangerZone)
        {
            var detections = new List<DetectionResult>();

            try
            {
                Cv2.ImEncode(".jpg", frame, out var data);
                var base64 = Convert.ToBase64String(data);

                var python = _python;
                if (python?.StandardInput == null || python.HasExited)
                {
                    return detections;
                }

                python.StandardInput.WriteLine(base64);
                python.StandardInput.Flush();

                var lineTask = python.StandardOutput.ReadLineAsync();
                if (!lineTask.Wait(PythonResponseTimeoutMs))
                {
                    throw new TimeoutException("Python YOLO service did not answer in time.");
                }

                var line = lineTask.Result;
                if (string.IsNullOrEmpty(line))
                {
                    return detections;
                }

                var boxes = JsonSerializer.Deserialize<List<Dictionary<string, int>>>(line) ?? [];
                var id = 1;

                foreach (var box in boxes)
                {
                    var personRect = new Rect(box["x"], box["y"], box["w"], box["h"]);
                    var danger = personRect.IntersectsWith(dangerZone);

                    detections.Add(new DetectionResult
                    {
                        Id = id++,
                        X = box["x"],
                        Y = box["y"],
                        Width = box["w"],
                        Height = box["h"],
                        InDangerZone = danger
                    });
                }
            }
            catch (TimeoutException ex)
            {
                StatusChanged.Invoke($"Ошибка YOLO: {ex.Message}", true);
                StopCamera();
            }
            catch (JsonException ex)
            {
                StatusChanged.Invoke($"Ошибка ответа YOLO: {ex.Message}", true);
                StopCamera();
            }
            catch (InvalidOperationException ex)
            {
                StatusChanged.Invoke($"Ошибка Python-процесса: {ex.Message}", true);
                StopCamera();
            }
            catch
            {
            }

            return detections;
        }

        private Rect GetDangerZoneRect(int frameWidth, int frameHeight)
        {
            DangerZoneRatios ratios;

            lock (_syncRoot)
            {
                ratios = _dangerZone;
            }

            var x = Math.Clamp((int)(frameWidth * ratios.X), 0, frameWidth - 1);
            var y = Math.Clamp((int)(frameHeight * ratios.Y), 0, frameHeight - 1);
            var width = Math.Clamp((int)(frameWidth * ratios.Width), 1, frameWidth - x);
            var height = Math.Clamp((int)(frameHeight * ratios.Height), 1, frameHeight - y);

            return new Rect(x, y, width, height);
        }

        private static void DrawDangerZone(Mat frame, Rect dangerZone)
        {
            if (frame.Empty() || dangerZone.Width <= 0 || dangerZone.Height <= 0)
            {
                return;
            }

            using var overlay = frame.Clone();

            Cv2.Rectangle(
                overlay,
                dangerZone,
                new Scalar(40, 40, 180),
                -1);

            Cv2.AddWeighted(overlay, 0.2, frame, 0.8, 0, frame);
            Cv2.Rectangle(frame, dangerZone, Scalar.Red, 2);
            Cv2.PutText(
                frame,
                "Danger zone",
                new Point(dangerZone.X + 10, Math.Max(28, dangerZone.Y - 10)),
                HersheyFonts.HersheySimplex,
                0.65,
                Scalar.Red,
                2);
        }

        private static void DrawDetections(Mat frame, List<DetectionResult> detections)
        {
            foreach (var detection in detections)
            {
                var color = detection.InDangerZone ? Scalar.Red : Scalar.Green;

                Cv2.Rectangle(
                    frame,
                    new Rect(detection.X, detection.Y, detection.Width, detection.Height),
                    color,
                    2);

                Cv2.PutText(
                    frame,
                    $"ID {detection.Id}",
                    new Point(detection.X, detection.Y - 10),
                    HersheyFonts.HersheySimplex,
                    0.6,
                    color,
                    2);
            }
        }

        private static Bitmap ConvertToBitmap(Mat frame)
        {
            Cv2.ImEncode(".bmp", frame, out var data);
            return new Bitmap(new MemoryStream(data));
        }

        private static void TryStopPythonProcess(Process python)
        {
            try
            {
                if (!python.HasExited)
                {
                    python.Kill(true);
                    python.WaitForExit(1000);
                }
            }
            catch
            {
            }
            finally
            {
                python.Dispose();
            }
        }

        private void WaitForPythonReady(Process python, CancellationToken cancellationToken)
        {
            _pythonErrorLog.Clear();
            _ = Task.Run(() => PumpPythonErrors(python), cancellationToken);

            var readyTask = python.StandardOutput.ReadLineAsync();
            if (!readyTask.Wait(PythonStartupTimeoutMs))
            {
                throw new TimeoutException("Python YOLO service startup timed out.");
            }

            var readyLine = readyTask.Result;
            if (!string.Equals(readyLine, PythonReadyMessage, StringComparison.Ordinal))
            {
                var errorText = TryGetRecentPythonError();
                throw new InvalidOperationException(
                    string.IsNullOrWhiteSpace(errorText)
                        ? $"Unexpected Python startup response: {readyLine ?? "<null>"}"
                        : $"Python startup failed: {errorText}");
            }

            cancellationToken.ThrowIfCancellationRequested();
        }

        private void PumpPythonErrors(Process python)
        {
            try
            {
                while (!python.HasExited)
                {
                    var line = python.StandardError.ReadLine();
                    if (string.IsNullOrWhiteSpace(line))
                    {
                        continue;
                    }

                    _pythonErrorLog.Enqueue(line);
                    while (_pythonErrorLog.Count > 10 && _pythonErrorLog.TryDequeue(out _))
                    {
                    }
                }
            }
            catch
            {
            }
        }

        private string? TryGetRecentPythonError()
        {
            return _pythonErrorLog.IsEmpty ? null : string.Join(" | ", _pythonErrorLog.ToArray());
        }

        private static string ResolveRuntimeFilePath(string fileName)
        {
            var candidates = new[]
            {
                Path.Combine(Environment.CurrentDirectory, fileName),
                Path.Combine(AppContext.BaseDirectory, fileName)
            };

            foreach (var candidate in candidates)
            {
                if (File.Exists(candidate))
                {
                    return Path.GetFullPath(candidate);
                }
            }

            throw new FileNotFoundException($"Required runtime file was not found: {fileName}");
        }

        private readonly record struct DangerZoneRatios(double X, double Y, double Width, double Height);
    }
}
