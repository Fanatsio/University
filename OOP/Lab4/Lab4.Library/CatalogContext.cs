using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace Lab4.Library
{
    internal class CatalogContext : DbContext
    {
        public DbSet<Products> Products { get; set; }
        public DbSet<Brands> Brands { get; set; }
        public DbSet<Categories> Categories { get; set; }

        public CatalogContext(DbContextOptions<CatalogContext> options) : base(options) { }

        public class CatalogContextFactory : IDesignTimeDbContextFactory<CatalogContext>
        {
            public CatalogContext CreateDbContext(string[] args)
            {
                var optionsBuilder = new DbContextOptionsBuilder<CatalogContext>();
                optionsBuilder.UseSqlite("Data Source=.\\ClothingCatalog.db");

                return new CatalogContext(optionsBuilder.Options);
            }
        }

    }
}

#region Migration
//Add-Migration InitialMigration -Project Lab4.Library -StartupProject Lab4.Library

//Update-Database -Project Lab4.Library -StartupProject Lab4.Library
#endregion