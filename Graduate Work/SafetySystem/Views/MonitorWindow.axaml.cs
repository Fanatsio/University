using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using SafetySystem.Models;
using SafetySystem.Services;
using System;
using System.Collections.Generic;
using System.Linq;

namespace SafetySystem.Views
{
    public partial class MonitorWindow : UserControl
    {
        private readonly CameraService _cameraService;
        private Bitmap? _currentFrame;
        private bool _isMonitoring;
        private bool _isUpdatingDangerZoneControls;

        public MonitorWindow()
        {
            _cameraService = new CameraService();

            InitializeComponent();
            SubscribeDangerZoneControls();
            UpdateDangerZone();

            _cameraService.FrameReady += OnFrameReady;
            _cameraService.StatusChanged += OnStatusChanged;

            AttachedToVisualTree += OnAttachedToVisualTree;
            DetachedFromVisualTree += OnDetachedFromVisualTree;
        }

        private void OnAttachedToVisualTree(object? sender, VisualTreeAttachmentEventArgs e)
        {
            StartMonitoring();
        }

        private void OnDetachedFromVisualTree(object? sender, VisualTreeAttachmentEventArgs e)
        {
            StopMonitoring("Мониторинг остановлен.", false);
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

                var dangerCount = detections.Count(detection => detection.InDangerZone);
                var safeCount = detections.Count - dangerCount;

                TotalPeopleText.Text = detections.Count.ToString();
                DangerPeopleText.Text = dangerCount.ToString();
                SafePeopleText.Text = safeCount.ToString();
                LastUpdateText.Text = DateTime.Now.ToString("HH:mm:ss");

                PeopleInZoneList.Items.Clear();

                foreach (var detection in detections)
                {
                    if (!detection.InDangerZone)
                    {
                        continue;
                    }

                    PeopleInZoneList.Items.Add($"ID {detection.Id} - в опасной зоне");
                }

                if (dangerCount == 0)
                {
                    PeopleInZoneList.Items.Add("Нарушений не зафиксировано");
                }

                var dangerDetected = dangerCount > 0;
                IntrusionAlert.Text = dangerDetected ? "НАРУШЕНИЕ!" : "Нет нарушений";
                IntrusionAlert.Foreground = dangerDetected ? Brushes.OrangeRed : Brushes.LightGreen;
            });
        }

        private void OnStatusChanged(string message, bool isError)
        {
            Dispatcher.UIThread.Post(() =>
            {
                MonitorStatusText.Text = message;
                MonitorStatusText.Foreground = isError ? Brushes.OrangeRed : Brushes.White;

                if (isError)
                {
                    _isMonitoring = false;
                    SetMonitorControlsState(false);
                }

                ShowLoadingState(message, isError);
            });
        }

        private void ShowLoadingState(string message, bool isError)
        {
            LoadingStatusText.Text = message;
            LoadingStatusText.Foreground = isError ? Brushes.OrangeRed : Brushes.White;
            LoadingOverlay.IsVisible = true;
        }

        private void OnStartMonitorClick(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            StartMonitoring();
        }

        private void OnStopMonitorClick(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            StopMonitoring("Мониторинг на паузе.", false);
        }

        private void OnDangerZoneSliderChanged(object? sender, RangeBaseValueChangedEventArgs e)
        {
            UpdateDangerZone();
        }

        private void SubscribeDangerZoneControls()
        {
            DangerZoneXSlider.ValueChanged += OnDangerZoneSliderChanged;
            DangerZoneYSlider.ValueChanged += OnDangerZoneSliderChanged;
            DangerZoneWidthSlider.ValueChanged += OnDangerZoneSliderChanged;
            DangerZoneHeightSlider.ValueChanged += OnDangerZoneSliderChanged;
        }

        private void StartMonitoring()
        {
            if (_isMonitoring)
            {
                return;
            }

            _isMonitoring = true;
            SetMonitorControlsState(true);
            ShowLoadingState("Инициализация камеры...", false);
            MonitorStatusText.Text = "Инициализация камеры...";
            MonitorStatusText.Foreground = Brushes.White;
            UpdateDangerZone();
            _cameraService.StartCamera();
        }

        private void StopMonitoring(string message, bool isError)
        {
            if (!_isMonitoring)
            {
                ShowLoadingState(message, isError);
                return;
            }

            _isMonitoring = false;
            _cameraService.StopCamera();
            DisposeCurrentFrame();
            ResetMetrics();
            SetMonitorControlsState(false);
            ShowLoadingState(message, isError);
            MonitorStatusText.Text = message;
            MonitorStatusText.Foreground = isError ? Brushes.OrangeRed : Brushes.White;
        }

        private void UpdateDangerZone()
        {
            if (_isUpdatingDangerZoneControls)
            {
                return;
            }

            _isUpdatingDangerZoneControls = true;

            var x = DangerZoneXSlider.Value;
            var y = DangerZoneYSlider.Value;
            var width = Math.Min(DangerZoneWidthSlider.Value, 100 - x);
            var height = Math.Min(DangerZoneHeightSlider.Value, 100 - y);

            DangerZoneWidthSlider.Value = width;
            DangerZoneHeightSlider.Value = height;
            DangerZoneValueText.Text = $"X {x:0}%, Y {y:0}%, W {width:0}%, H {height:0}%";
            _cameraService.SetDangerZoneRectPercent(x, y, width, height);

            _isUpdatingDangerZoneControls = false;
        }

        private void SetMonitorControlsState(bool isRunning)
        {
            StartMonitorButton.IsEnabled = !isRunning;
            StopMonitorButton.IsEnabled = isRunning;
            MonitorModeText.Text = isRunning ? "LIVE" : "PAUSED";
            MonitorModeText.Foreground = isRunning ? Brushes.OrangeRed : Brushes.LightGray;
        }

        private void ResetMetrics()
        {
            TotalPeopleText.Text = "0";
            DangerPeopleText.Text = "0";
            SafePeopleText.Text = "0";
            LastUpdateText.Text = "Кадров пока нет";
            PeopleInZoneList.Items.Clear();
            IntrusionAlert.Text = "Нет нарушений";
            IntrusionAlert.Foreground = Brushes.LightGreen;
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
