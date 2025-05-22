// ReSharper disable All

namespace Lab3.Library
{
    public static class DbContextTestHelper
    {
        public static int AddEntities()
        {
            // Добавляем данные в БД.
            using var context = new ClothingCatalogContext();
            context.Database.EnsureCreated();

            var product = new Product { NameProduct = "testa" };
            var brand = new Brand { Name = "testb" };
            var category = new Category { Name = "testc" };

            context.Products.Add(product);
            context.Brands.Add(brand);
            context.Categories.Add(category);

            return context.SaveChanges();
        }

        public static int UpdateEntities()
        {
            // Обновляем данные в БД.
            using var context = new ClothingCatalogContext();
            context.Database.EnsureCreated();

            var productToUpdate = context.Products.FirstOrDefault(s => s.NameProduct == "testa");
            var brandToUpdate = context.Brands.FirstOrDefault(s => s.Name == "testb");
            var categoryToUpdate = context.Categories.FirstOrDefault(s => s.Name == "testc");

            if (productToUpdate != null)
            {
                productToUpdate.NameProduct = "testa (upd)";
            }
            if (brandToUpdate != null)
            {
                brandToUpdate.Name = "testb (upd)";
            }
            if (categoryToUpdate != null)
            {
                categoryToUpdate.Name = "testc (upd)";
            }

            return context.SaveChanges();
        }

        public static int ReadEntities()
        {
            // Читаем данные из БД.
            using var context = new ClothingCatalogContext();
            context.Database.EnsureCreated();

            Console.WriteLine("Products:");
            foreach (var product in context.Products)
            {
                Console.WriteLine($"ID: {product.Id}, Name: {product.NameProduct}");
            }

            Console.WriteLine("Brands:");
            foreach (var brand in context.Brands)
            {
                Console.WriteLine($"ID: {brand.Id}, Name: {brand.Name}");
            }

            Console.WriteLine("Categories:");
            foreach (var category in context.Categories)
            {
                Console.WriteLine($"ID: {category.Id}, Name: {category.Name}");
            }

            return context.Products.Count() + context.Brands.Count() + context.Categories.Count();
        }

        public static int RemoveEntities()
        {
            // Удаляем данные в БД.
            using var context = new ClothingCatalogContext();
            context.Database.EnsureCreated();

            var productToDelete = context.Products.FirstOrDefault(s => s.NameProduct == "testa (upd)");
            var brandToDelete = context.Brands.FirstOrDefault(a => a.Name == "testb (upd)");
            var categoryToDelete = context.Categories.FirstOrDefault(al => al.Name == "testc (upd)");

            if (productToDelete != null)
            {
                context.Products.Remove(productToDelete);
            }
            if (brandToDelete != null)
            {
                context.Brands.Remove(brandToDelete);
            }
            if (categoryToDelete != null)
            {
                context.Categories.Remove(categoryToDelete);
            }

            return context.SaveChanges();
        }
    }
}
