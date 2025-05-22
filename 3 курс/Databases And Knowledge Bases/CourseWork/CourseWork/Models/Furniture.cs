namespace CourseWork.Models
{
    public class Furniture
    {
        public int FurnitureId { get; set; }
        public string FurnitureColour { get; set; }
        public int FurnitureArticle { get; set; }
        public int IdMaterial { get; set; }
        public string FurnitureType { get; set; }
        public decimal FurnitureSize { get; set; }
        public string FurnitureName { get; set; }
        public int IdAccessories { get; set; }
    }
}