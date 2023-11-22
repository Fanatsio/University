// ReSharper disable All

using System.Data.Entity;

namespace Lab3.Library;

public static class DbContextTestHelper
{
    public static int AddEntities()
    {
        // Добавляем данные в БД.
        using var context = new ClothingCatalogContext();
        context.Database.EnsureCreated();

        var Products = new Products { NameProduct = "tests" };
        var Brands = new Brands { NameBrands = "testar" };
        var Categories = new Categories { NameCategories = "testal" };

        context.Products.Add(Products);
        context.Brands.Add(Brands);
        context.Categories.Add(Categories);

        return context.SaveChanges();
    }

    public static int UpdateEntities()
    {
        // Обновляем данные в БД.
        using var context = new ClothingCatalogContext();
        context.Database.EnsureCreated();

        var ProductsToUpdate = context.Products.FirstOrDefault(s => s.NameProduct == "tests");
        var BrandsToUpdate = context.Brands.FirstOrDefault(s => s.NameBrands == "testar");
        var CategoriesToUpdate = context.Categories.FirstOrDefault(s => s.NameCategories == "testal");

        if (ProductsToUpdate != null)
        {
            ProductsToUpdate.NameProduct = "tests (upd)";
        }
        if (BrandsToUpdate != null)
        {
            BrandsToUpdate.NameBrands = "testar (upd)";
        }
        if (CategoriesToUpdate != null)
        {
            CategoriesToUpdate.NameCategories = "testal (upd)";
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
            Console.WriteLine($"ID: {brand.Id}, Name: {brand.NameBrands}");
        }

        Console.WriteLine("Categories:");
        foreach (var category in context.Categories)
        {
            Console.WriteLine($"ID: {category.Id}, Name: {category.NameCategories}");
        }

        return context.Products.Count() + context.Brands.Count() + context.Categories.Count();
    }


    public static int RemoveEntities()
    {
        // Удаляем данные в БД.
        using var context = new ClothingCatalogContext();
        context.Database.EnsureCreated();

        var ProductsToDelete = context.Products.FirstOrDefault(s => s.NameProduct == "tests (upd)");
        var BrandsToDelete = context.Brands.FirstOrDefault(a => a.NameBrands == "testar (upd)");
        var CategoriesToDelete = context.Categories.FirstOrDefault(al => al.NameCategories == "testal (upd)");

        if (ProductsToDelete != null)
        {
            context.Products.Remove(ProductsToDelete);
        }
        if (BrandsToDelete != null)
        {
            context.Brands.Remove(BrandsToDelete);
        }
        if (CategoriesToDelete != null)
        {
            context.Categories.Remove(CategoriesToDelete);
        }

        return context.SaveChanges();
    }
}
