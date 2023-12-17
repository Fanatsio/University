using Microsoft.EntityFrameworkCore;

namespace Lab4.Library
{
    internal class CatalogService : ICatalogService
    {
        private readonly IDbContextFactory<ClothingCatalogContext> _contextFactory;

        public CatalogService(IDbContextFactory<ClothingCatalogContext> contextFactory)
        {
            _contextFactory = contextFactory;
        }

        public int AddProducts(Product Products)
        {
            using var context = _contextFactory.CreateDbContext();
            context.Products.Add(Products);
            return context.SaveChanges();
        }

        public int AddBrands(Brand Brands)
        {
            using var context = _contextFactory.CreateDbContext();
            context.Brands.Add(Brands);
            return context.SaveChanges();
        }

        public int AddCategories(Category categories)
        {
            using var context = _contextFactory.CreateDbContext();
            context.Categories.Add(categories);
            return context.SaveChanges();
        }

        public int UpdateProducts(int Id, string updatedProducts)
        {
            using var context = _contextFactory.CreateDbContext();
            var Product = context.Products.Find(Id);
            if (Product != null)
            {
                Product.NameProduct = updatedProducts;
                context.Products.Update(Product);
                return context.SaveChanges();
            }
            return 0;
        }

        public int UpdateBrands(int Id, string updatedBrands)
        {
            using var context = _contextFactory.CreateDbContext();
            var brand = context.Brands.Find(Id);
            if (brand != null)
            {
                brand.Name = updatedBrands;
                context.Brands.Update(brand);
                return context.SaveChanges();
            }
            return 0;
        }

        public int UpdateCategories(int Id, string updatedCategories)
        {
            using var context = _contextFactory.CreateDbContext();
            var Category = context.Categories.Find(Id);
            if (Category != null)
            {
                Category.Name = updatedCategories;
                context.Categories.Update(Category);
                return context.SaveChanges();
            }
            return 0;
        }

        public Product ReadProducts(int ProductsId)
        {
            using var context = _contextFactory.CreateDbContext();
            return context.Products.Find(ProductsId);
        }

        public Brand ReadBrands(int BrandsId)
        {
            using var context = _contextFactory.CreateDbContext();
            return context.Brands.Find(BrandsId);
        }

        public Category ReadCategories(int CategoriesId)
        {
            using var context = _contextFactory.CreateDbContext();
            return context.Categories.Find(CategoriesId);
        }

        public int RemoveProducts(int ProductsName)
        {
            using var context = _contextFactory.CreateDbContext();
            var Product = context.Products.Find(ProductsName);
            if (Product != null)
            {
                context.Products.Remove(Product);
                return context.SaveChanges();
            }
            return 0;
        }

        public int RemoveBrands(string nameBrands)
        {
            using var context = _contextFactory.CreateDbContext();
            var Brand = context.Brands.Find(nameBrands);
            if (Brand != null)
            {
                context.Brands.Remove(Brand);
                return context.SaveChanges();
            }
            return 0;
        }

        public int RemoveCategories(int nameCategories)
        {
            using var context = _contextFactory.CreateDbContext();
            var Category = context.Categories.Find(nameCategories);
            if (Category != null)
            {
                context.Categories.Remove(Category);
                return context.SaveChanges();
            }
            return 0;
        }
    }
}
