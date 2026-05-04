using SafetySystem.Models;
using System;
using System.IO;
using System.Text.Json;

namespace SafetySystem.Services
{
    public static class AppSettingsService
    {
        private const string AppFolderName = "SafetySystem";
        private const string SettingsFileName = "settings.json";

        private static readonly JsonSerializerOptions JsonOptions = new()
        {
            WriteIndented = true
        };

        public static string SettingsFilePath
        {
            get
            {
                var appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
                return Path.Combine(appData, AppFolderName, SettingsFileName);
            }
        }

        public static AppSettings Load()
        {
            try
            {
                if (!File.Exists(SettingsFilePath))
                {
                    return new AppSettings();
                }

                var json = File.ReadAllText(SettingsFilePath);
                return JsonSerializer.Deserialize<AppSettings>(json, JsonOptions) ?? new AppSettings();
            }
            catch
            {
                return new AppSettings();
            }
        }

        public static void Save(AppSettings settings)
        {
            ArgumentNullException.ThrowIfNull(settings);

            Normalize(settings);

            var directory = Path.GetDirectoryName(SettingsFilePath);
            if (!string.IsNullOrWhiteSpace(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var json = JsonSerializer.Serialize(settings, JsonOptions);
            File.WriteAllText(SettingsFilePath, json);
        }

        public static void Reset()
        {
            Save(new AppSettings());
        }

        private static void Normalize(AppSettings settings)
        {
            settings.CameraIndex = Math.Clamp(settings.CameraIndex, 0, 8);
            settings.ConfidenceThreshold = Math.Clamp(settings.ConfidenceThreshold, 0.1, 0.95);
            settings.DangerZoneXPercent = Math.Clamp(settings.DangerZoneXPercent, 0, 95);
            settings.DangerZoneYPercent = Math.Clamp(settings.DangerZoneYPercent, 0, 95);
            settings.DangerZoneWidthPercent = Math.Clamp(settings.DangerZoneWidthPercent, 5, 100 - settings.DangerZoneXPercent);
            settings.DangerZoneHeightPercent = Math.Clamp(settings.DangerZoneHeightPercent, 5, 100 - settings.DangerZoneYPercent);
            settings.YoloModelPath = string.IsNullOrWhiteSpace(settings.YoloModelPath) ? "yolov8s-seg.pt" : settings.YoloModelPath.Trim();
            settings.DatabasePath = string.IsNullOrWhiteSpace(settings.DatabasePath) ? "safetysystem.db" : settings.DatabasePath.Trim();
        }
    }
}
