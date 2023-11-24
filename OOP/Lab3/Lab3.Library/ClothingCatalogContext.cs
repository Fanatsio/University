using Microsoft.EntityFrameworkCore;

namespace Lab3.Library
{
    internal class ClothingCatalogContext : DbContext
    {
        public DbSet<Brands> Brands { get; set; }
        public DbSet<Categories> Categories { get; set; }
        public DbSet<Products> Products { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Products>().HasIndex(t => t.Id);
            modelBuilder.Entity<Products>().HasOne(m => m.Brand);
            modelBuilder.Entity<Products>().HasOne(m => m.Category);

            modelBuilder.Entity<Categories>().HasIndex(t => t.Id);
            modelBuilder.Entity<Brands>().HasIndex(t => t.Id);
        }

        public ClothingCatalogContext()
        {
            Database.EnsureDeleted();   // удаляем бд со старой схемой
            Database.EnsureCreated();   // создаем бд с новой схемой
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlite("DataSource=ClothingCatalog.db");
        }
    }
}
