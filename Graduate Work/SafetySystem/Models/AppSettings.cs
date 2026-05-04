namespace SafetySystem.Models
{
    public class AppSettings
    {
        public int CameraIndex { get; set; } = 0;
        public string YoloModelPath { get; set; } = "yolov8s.pt";
        public double ConfidenceThreshold { get; set; } = 0.5;
        public string DatabasePath { get; set; } = "safetysystem.db";
        public bool AutoStartMonitoring { get; set; } = true;
        public double DangerZoneXPercent { get; set; } = 25;
        public double DangerZoneYPercent { get; set; } = 55;
        public double DangerZoneWidthPercent { get; set; } = 50;
        public double DangerZoneHeightPercent { get; set; } = 35;
    }
}
