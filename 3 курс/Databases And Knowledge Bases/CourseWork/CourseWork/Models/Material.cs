namespace CourseWork.Models
{
    public class Material
    {
        public int MaterialId { get; set; }
        public string MaterialColour { get; set; }
        public string MaterialName { get; set; }
        public string MaterialType { get; set; }
        public int MaterialQuantity { get; set; }
        public string ProviderInn { get; set; }
        public decimal MaterialCost { get; set; }
    }
}