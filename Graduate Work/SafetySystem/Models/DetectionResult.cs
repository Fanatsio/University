using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace SafetySystem.Models
{
    public class DetectionPoint
    {
        [JsonPropertyName("x")]
        public int X { get; set; }

        [JsonPropertyName("y")]
        public int Y { get; set; }
    }

    public class DetectionResult
    {
        public int Id { get; set; }

        [JsonPropertyName("x")]
        public int X { get; set; }

        [JsonPropertyName("y")]
        public int Y { get; set; }

        [JsonPropertyName("w")]
        public int Width { get; set; }

        [JsonPropertyName("h")]
        public int Height { get; set; }

        [JsonPropertyName("contour")]
        public List<DetectionPoint> Contour { get; set; } = [];

        public bool InDangerZone { get; set; }
    }
}
