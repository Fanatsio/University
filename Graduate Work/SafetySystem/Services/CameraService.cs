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
        private const int DangerZoneBottomBoundary = 400;
        private const string PythonReadyMessage = "READY";

        private readonly object _syncRoot = new();
        private readonly ConcurrentQueue<string> _pythonErrorLog = new();
        private VideoCapture? _capture;
        private Process? _python;
        private Task? _startupTask;
        private Task? _cameraTask;
        private CancellationTokenSource? _cancellationTokenSource;

        public event Action<Bitmap, List<DetectionResult>> FrameReady = delegate { };
        public event Action<string, bool> StatusChanged = delegate { };

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

                var detections = DetectWithYolo(frame);
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

        private List<DetectionResult> DetectWithYolo(Mat frame)
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
                    var danger = box["y"] + box["h"] > DangerZoneBottomBoundary;

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
    }
}
