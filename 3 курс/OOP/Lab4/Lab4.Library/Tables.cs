namespace Lab4.Library
{
    internal class Product
    {
        public int Id { get; set; }
        public string? NameProduct { get; set; }
        public int Price { get; set; }

        public List<ProductBrand> Brands { get; set; } = new List<ProductBrand>();
        public List<ProductCategory> Categories { get; set; } = new List<ProductCategory>();
    }

    internal class Brand
    {
        public int Id { get; set; }
        public string? Name { get; set; }

        public List<ProductBrand> Products { get; set; } = new List<ProductBrand>();
    }

    internal class Category
    {
        public int Id { get; set; }
        public string? Name { get; set; }

        public List<ProductCategory> Products { get; set; } = new List<ProductCategory>();
    }

    internal class ProductBrand
    {
        public int ProductId { get; set; }
        public Product? Product { get; set; }

        public int BrandId { get; set; }
        public Brand? Brand { get; set; }
    }

    internal class ProductCategory
    {
        public int ProductId { get; set; }
        public Product? Product { get; set; }

        public int CategoryId { get; set; }
        public Category? Category { get; set; }
    }
}
