using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Media;
using SafetySystem.Models;
using SafetySystem.Services;
using System;

namespace SafetySystem.Views
{
    public partial class SettingsView : UserControl
    {
        private bool _isUpdatingControls;

        public SettingsView()
        {
            InitializeComponent();
            InitializeCameraList();
            SettingsFilePathText.Text = AppSettingsService.SettingsFilePath;

            ConfidenceSlider.ValueChanged += OnSliderValueChanged;
            DangerZoneXSlider.ValueChanged += OnSliderValueChanged;
            DangerZoneYSlider.ValueChanged += OnSliderValueChanged;
            DangerZoneWidthSlider.ValueChanged += OnSliderValueChanged;
            DangerZoneHeightSlider.ValueChanged += OnSliderValueChanged;

            LoadSettings();
        }

        private void InitializeCameraList()
        {
            CameraIndexComboBox.Items.Clear();

            for (var i = 0; i <= 4; i++)
            {
                CameraIndexComboBox.Items.Add($"Камера {i}");
            }
        }

        private void LoadSettings()
        {
            ApplySettingsToControls(AppSettingsService.Load());
            SetStatus("Настройки загружены", Brushes.LightGreen);
        }

        private void ApplySettingsToControls(AppSettings settings)
        {
            _isUpdatingControls = true;

            CameraIndexComboBox.SelectedIndex = Math.Clamp(settings.CameraIndex, 0, CameraIndexComboBox.Items.Count - 1);
            YoloModelPathTextBox.Text = settings.YoloModelPath;
            DatabasePathTextBox.Text = settings.DatabasePath;
            AutoStartMonitoringCheckBox.IsChecked = settings.AutoStartMonitoring;
            ConfidenceSlider.Value = settings.ConfidenceThreshold * 100;
            DangerZoneXSlider.Value = settings.DangerZoneXPercent;
            DangerZoneYSlider.Value = settings.DangerZoneYPercent;
            DangerZoneWidthSlider.Value = settings.DangerZoneWidthPercent;
            DangerZoneHeightSlider.Value = settings.DangerZoneHeightPercent;

            _isUpdatingControls = false;
            UpdateCalculatedText();
        }

        private void OnSliderValueChanged(object? sender, RangeBaseValueChangedEventArgs e)
        {
            UpdateCalculatedText();
        }

        private void UpdateCalculatedText()
        {
            if (_isUpdatingControls)
            {
                return;
            }

            _isUpdatingControls = true;

            var x = DangerZoneXSlider.Value;
            var y = DangerZoneYSlider.Value;
            var width = Math.Min(DangerZoneWidthSlider.Value, 100 - x);
            var height = Math.Min(DangerZoneHeightSlider.Value, 100 - y);

            DangerZoneWidthSlider.Value = width;
            DangerZoneHeightSlider.Value = height;
            ConfidenceValueText.Text = $"{ConfidenceSlider.Value:0}%";
            DangerZoneValueText.Text = $"X {x:0}%, Y {y:0}%, W {width:0}%, H {height:0}%";

            _isUpdatingControls = false;
        }

        private void OnSaveClick(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            try
            {
                var settings = ReadSettingsFromControls();
                AppSettingsService.Save(settings);
                ApplySettingsToControls(settings);
                SetStatus("Сохранено", Brushes.LightGreen);
            }
            catch (Exception ex)
            {
                SetStatus($"Ошибка: {ex.Message}", Brushes.OrangeRed);
            }
        }

        private void OnResetClick(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            AppSettingsService.Reset();
            LoadSettings();
        }

        private AppSettings ReadSettingsFromControls()
        {
            return new AppSettings
            {
                CameraIndex = Math.Max(0, CameraIndexComboBox.SelectedIndex),
                YoloModelPath = YoloModelPathTextBox.Text?.Trim() ?? string.Empty,
                DatabasePath = DatabasePathTextBox.Text?.Trim() ?? string.Empty,
                AutoStartMonitoring = AutoStartMonitoringCheckBox.IsChecked == true,
                ConfidenceThreshold = ConfidenceSlider.Value / 100,
                DangerZoneXPercent = DangerZoneXSlider.Value,
                DangerZoneYPercent = DangerZoneYSlider.Value,
                DangerZoneWidthPercent = DangerZoneWidthSlider.Value,
                DangerZoneHeightPercent = DangerZoneHeightSlider.Value
            };
        }

        private void SetStatus(string message, IBrush brush)
        {
            SettingsStatusText.Text = message;
            SettingsStatusText.Foreground = brush;
        }
    }
}
