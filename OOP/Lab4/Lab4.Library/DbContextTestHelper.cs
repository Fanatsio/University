// ReSharper disable All

using Autofac;
using Autofac.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace Lab4.Library
{
    public static class DbContextTestHelper
    {
        private static readonly IHost _host;

        static DbContextTestHelper()
        {
            // Создаем и настраиваем IoC - контейнер.
            AutofacServiceProviderFactory provider = new(configurationAction: builder =>
            {
                builder.RegisterType<CatalogService>().As<ICatalogService>().SingleInstance();
            });

            _host = Host.CreateDefaultBuilder()
                .UseServiceProviderFactory(provider)
                .ConfigureServices((context, services) =>
                {
                    services.AddPooledDbContextFactory<ClothingCatalogContext>(options => options.UseSqlite("Data Source=ClothingCatalog.db"));
                })
                .Build();

        }

        public static int AddEntities()
        {
            // Добавляем данные в БД через службу.
            using var scope = _host.Services.CreateScope();
            var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();

            var product = new Product
            {
                NameProduct = "product1",
            };

            return serviceProvider.AddProducts(product);
        }

        public static int UpdateEntities()
        {
            // Обновляем данные в БД через службу.
            using var scope = _host.Services.CreateScope();
            var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();

            var productID = 1;
            var updatedProduct = "Updated product1";

            return serviceProvider.UpdateProducts(productID, updatedProduct);
        }

        internal static Product ReadEntities()
        {
            // Читаем данные из БД через службу.
            using var scope = _host.Services.CreateScope();
            var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();

            var productID = 1;

            return serviceProvider.ReadProducts(productID);
        }

        public static int RemoveEntities()
        {
            // Удаляем данные в БД через службу.
            using var scope = _host.Services.CreateScope();

            int productName = 1;

            var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();
            return serviceProvider.RemoveProducts(productName);
        }
    }
}