using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using SafetySystem.Models;
using SafetySystem.Services;
using System.Collections.Generic;

namespace SafetySystem.Views
{
    public partial class MonitorWindow : UserControl
    {
        private readonly CameraService _cameraService;
        private Bitmap? _currentFrame;

        public MonitorWindow()
        {
            InitializeComponent();

            _cameraService = new CameraService();
            _cameraService.FrameReady += OnFrameReady;
            _cameraService.StatusChanged += OnStatusChanged;

            AttachedToVisualTree += OnAttachedToVisualTree;
            DetachedFromVisualTree += OnDetachedFromVisualTree;
        }

        private void OnAttachedToVisualTree(object? sender, VisualTreeAttachmentEventArgs e)
        {
            ShowLoadingState("Инициализация камеры...", false);
            _cameraService.StartCamera();
        }

        private void OnDetachedFromVisualTree(object? sender, VisualTreeAttachmentEventArgs e)
        {
            _cameraService.StopCamera();
            DisposeCurrentFrame();
            ShowLoadingState("Инициализация камеры...", false);
        }

        private void OnFrameReady(Bitmap frame, List<DetectionResult> detections)
        {
            Dispatcher.UIThread.Post(() =>
            {
                var previousFrame = _currentFrame;
                _currentFrame = frame;

                CameraStream.Source = frame;
                previousFrame?.Dispose();
                LoadingOverlay.IsVisible = false;

                PeopleInZoneList.Items.Clear();

                var dangerDetected = false;

                foreach (var detection in detections)
                {
                    if (!detection.InDangerZone)
                    {
                        continue;
                    }

                    PeopleInZoneList.Items.Add($"ID {detection.Id} - в опасной зоне");
                    dangerDetected = true;
                }

                IntrusionAlert.Text = dangerDetected ? "НАРУШЕНИЕ!" : "Нет нарушений";
                IntrusionAlert.Foreground = dangerDetected ? Brushes.OrangeRed : Brushes.LightGreen;
            });
        }

        private void OnStatusChanged(string message, bool isError)
        {
            Dispatcher.UIThread.Post(() => ShowLoadingState(message, isError));
        }

        private void ShowLoadingState(string message, bool isError)
        {
            LoadingStatusText.Text = message;
            LoadingStatusText.Foreground = isError ? Brushes.OrangeRed : Brushes.White;
            LoadingOverlay.IsVisible = true;
        }

        private void DisposeCurrentFrame()
        {
            var frame = _currentFrame;
            _currentFrame = null;
            CameraStream.Source = null;
            frame?.Dispose();
        }
    }
}
