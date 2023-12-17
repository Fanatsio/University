using Microsoft.EntityFrameworkCore;

namespace Lab4.Library
{
    internal class ClothingCatalogContext : DbContext
    {
        public DbSet<Brand> Brands { get; set; }
        public DbSet<Category> Categories { get; set; }
        public DbSet<Product> Products { get; set; }

        public DbSet<ProductBrand> ProductBrands { get; set; }
        public DbSet<ProductCategory> ProductCategories { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Product>().HasIndex(t => t.Id);
            modelBuilder.Entity<Category>().HasIndex(t => t.Id);
            modelBuilder.Entity<Brand>().HasIndex(t => t.Id);

            modelBuilder.Entity<ProductBrand>()
                .HasKey(pb => new { pb.ProductId, pb.BrandId });

            modelBuilder.Entity<ProductCategory>()
                .HasKey(pc => new { pc.ProductId, pc.CategoryId });

            modelBuilder.Entity<ProductBrand>()
                .HasOne(pb => pb.Product)
                .WithMany(p => p.Brands)
                .HasForeignKey(pb => pb.ProductId);

            modelBuilder.Entity<ProductBrand>()
                .HasOne(pb => pb.Brand)
                .WithMany(b => b.Products)
                .HasForeignKey(pb => pb.BrandId);

            modelBuilder.Entity<ProductCategory>()
                .HasOne(pc => pc.Product)
                .WithMany(p => p.Categories)
                .HasForeignKey(pc => pc.ProductId);

            modelBuilder.Entity<ProductCategory>()
                .HasOne(pc => pc.Category)
                .WithMany(c => c.Products)
                .HasForeignKey(pc => pc.CategoryId);
        }

        public ClothingCatalogContext()
        {
            Database.EnsureDeleted();
            Database.EnsureCreated();
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlite("Data Source=ClothingCatalog.db");
        }
    }
}