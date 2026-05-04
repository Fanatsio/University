using Avalonia.Media.Imaging;
using OpenCvSharp;
using SafetySystem.Models;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
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

                var settings = AppSettingsService.Load();
                SetDangerZoneRectPercent(
                    settings.DangerZoneXPercent,
                    settings.DangerZoneYPercent,
                    settings.DangerZoneWidthPercent,
                    settings.DangerZoneHeightPercent);

                var capture = new VideoCapture(settings.CameraIndex);
                if (!capture.IsOpened())
                {
                    capture.Dispose();
                    throw new Exception($"Не удалось открыть камеру {settings.CameraIndex}.");
                }

                cancellationToken.ThrowIfCancellationRequested();

                lock (_syncRoot)
                {
                    _capture = capture;
                }

                StatusChanged.Invoke("Загрузка модели...", false);

                var python = StartPythonYolo(settings);
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

        private static Process StartPythonYolo(AppSettings settings)
        {
            var python = new Process();
            var scriptPath = ResolveRuntimeFilePath("yolo_server.py");
            var modelPath = ResolveModelPath(settings.YoloModelPath, scriptPath);
            var confidence = settings.ConfidenceThreshold.ToString(CultureInfo.InvariantCulture);

            python.StartInfo.FileName = "py";
            python.StartInfo.Arguments = $"-u \"{scriptPath}\" --model \"{modelPath}\" --confidence {confidence}";
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

                var detectionsFromYolo = JsonSerializer.Deserialize<List<DetectionResult>>(line) ?? [];
                var id = 1;

                foreach (var detection in detectionsFromYolo)
                {
                    detection.Id = id++;
                    detection.InDangerZone = IsDetectionInDangerZone(detection, dangerZone);
                    detections.Add(detection);
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

        private static bool IsDetectionInDangerZone(DetectionResult detection, Rect dangerZone)
        {
            if (detection.Contour.Count < 3)
            {
                var personRect = new Rect(detection.X, detection.Y, detection.Width, detection.Height);
                return personRect.IntersectsWith(dangerZone);
            }

            if (detection.Contour.Any(point => IsPointInsideRect(point, dangerZone)))
            {
                return true;
            }

            var dangerCorners = new[]
            {
                new DetectionPoint { X = dangerZone.X, Y = dangerZone.Y },
                new DetectionPoint { X = dangerZone.X + dangerZone.Width, Y = dangerZone.Y },
                new DetectionPoint { X = dangerZone.X + dangerZone.Width, Y = dangerZone.Y + dangerZone.Height },
                new DetectionPoint { X = dangerZone.X, Y = dangerZone.Y + dangerZone.Height }
            };

            if (dangerCorners.Any(corner => IsPointInsidePolygon(corner, detection.Contour)))
            {
                return true;
            }

            var dangerEdges = new[]
            {
                (dangerCorners[0], dangerCorners[1]),
                (dangerCorners[1], dangerCorners[2]),
                (dangerCorners[2], dangerCorners[3]),
                (dangerCorners[3], dangerCorners[0])
            };

            for (var index = 0; index < detection.Contour.Count; index++)
            {
                var current = detection.Contour[index];
                var next = detection.Contour[(index + 1) % detection.Contour.Count];

                if (dangerEdges.Any(edge => SegmentsIntersect(current, next, edge.Item1, edge.Item2)))
                {
                    return true;
                }
            }

            return false;
        }

        private static bool IsPointInsideRect(DetectionPoint point, Rect rect)
        {
            return point.X >= rect.X
                && point.X <= rect.X + rect.Width
                && point.Y >= rect.Y
                && point.Y <= rect.Y + rect.Height;
        }

        private static bool IsPointInsidePolygon(DetectionPoint point, IReadOnlyList<DetectionPoint> polygon)
        {
            var inside = false;

            for (int current = 0, previous = polygon.Count - 1; current < polygon.Count; previous = current++)
            {
                var currentPoint = polygon[current];
                var previousPoint = polygon[previous];
                var crossesY = currentPoint.Y > point.Y != previousPoint.Y > point.Y;

                if (crossesY)
                {
                    var intersectionX = (double)(previousPoint.X - currentPoint.X)
                        * (point.Y - currentPoint.Y)
                        / (previousPoint.Y - currentPoint.Y)
                        + currentPoint.X;

                    if (point.X < intersectionX)
                    {
                        inside = !inside;
                    }
                }
            }

            return inside;
        }

        private static bool SegmentsIntersect(DetectionPoint a, DetectionPoint b, DetectionPoint c, DetectionPoint d)
        {
            var d1 = Direction(c, d, a);
            var d2 = Direction(c, d, b);
            var d3 = Direction(a, b, c);
            var d4 = Direction(a, b, d);

            if (((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0))
                && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0)))
            {
                return true;
            }

            return d1 == 0 && IsPointOnSegment(c, d, a)
                || d2 == 0 && IsPointOnSegment(c, d, b)
                || d3 == 0 && IsPointOnSegment(a, b, c)
                || d4 == 0 && IsPointOnSegment(a, b, d);
        }

        private static long Direction(DetectionPoint a, DetectionPoint b, DetectionPoint c)
        {
            return (long)(c.X - a.X) * (b.Y - a.Y) - (long)(c.Y - a.Y) * (b.X - a.X);
        }

        private static bool IsPointOnSegment(DetectionPoint a, DetectionPoint b, DetectionPoint point)
        {
            return Math.Min(a.X, b.X) <= point.X
                && point.X <= Math.Max(a.X, b.X)
                && Math.Min(a.Y, b.Y) <= point.Y
                && point.Y <= Math.Max(a.Y, b.Y);
        }

        private static void DrawDetections(Mat frame, List<DetectionResult> detections)
        {
            using var overlay = frame.Clone();
            var hasMasks = false;

            foreach (var detection in detections)
            {
                var color = detection.InDangerZone ? Scalar.Red : Scalar.Green;

                if (detection.Contour.Count >= 3)
                {
                    var contour = detection.Contour
                        .Select(point => new Point(point.X, point.Y))
                        .ToArray();

                    Cv2.FillPoly(overlay, [contour], color);
                    hasMasks = true;
                }
            }

            if (hasMasks)
            {
                Cv2.AddWeighted(overlay, 0.18, frame, 0.82, 0, frame);
            }

            foreach (var detection in detections)
            {
                var color = detection.InDangerZone ? Scalar.Red : Scalar.Green;

                if (detection.Contour.Count >= 3)
                {
                    var contour = detection.Contour
                        .Select(point => new Point(point.X, point.Y))
                        .ToArray();

                    Cv2.Polylines(frame, [contour], true, color, 2);
                }
                else
                {
                    Cv2.Rectangle(
                        frame,
                        new Rect(detection.X, detection.Y, detection.Width, detection.Height),
                        color,
                        2);
                }

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

        private static string ResolveModelPath(string modelPath, string scriptPath)
        {
            if (Path.IsPathRooted(modelPath) && File.Exists(modelPath))
            {
                return Path.GetFullPath(modelPath);
            }

            var scriptDirectory = Path.GetDirectoryName(scriptPath) ?? Environment.CurrentDirectory;
            var candidates = new[]
            {
                Path.Combine(Environment.CurrentDirectory, modelPath),
                Path.Combine(AppContext.BaseDirectory, modelPath),
                Path.Combine(scriptDirectory, modelPath)
            };

            foreach (var candidate in candidates)
            {
                if (File.Exists(candidate))
                {
                    return Path.GetFullPath(candidate);
                }
            }

            throw new FileNotFoundException($"YOLO model file was not found: {modelPath}");
        }

        private readonly record struct DangerZoneRatios(double X, double Y, double Width, double Height);
    }
}
