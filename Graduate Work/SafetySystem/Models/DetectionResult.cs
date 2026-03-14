namespace SafetySystem.Models
{
    public class DetectionResult
    {
        public int Id { get; set; }

        public int X { get; set; }

        public int Y { get; set; }

        public int Width { get; set; }

        public int Height { get; set; }

        public bool InDangerZone { get; set; }
    }
}