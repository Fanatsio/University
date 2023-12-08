// ReSharper disable All

using Autofac;
using Autofac.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Internal;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyModel;
using Microsoft.Extensions.Hosting;
using System.IO;
using System.Runtime.InteropServices.JavaScript;

namespace Lab4.Library;

public static class DbContextTestHelper
{
    private static readonly IHost _host;

    static DbContextTestHelper()
    {
        // Создаем и настраиваем IoC - контейнер.
        AutofacServiceProviderFactory provider = new AutofacServiceProviderFactory(configurationAction: builder =>
        {
            builder.RegisterType<CatalogService>().As<ICatalogService>().SingleInstance();
        });

        _host = Host.CreateDefaultBuilder()
            .UseServiceProviderFactory(provider)
            .ConfigureServices((context, services) =>
            {
                services.AddPooledDbContextFactory<CatalogContext>(options => options.UseSqlite("Data Source=C:\\Users\\Lenovo\\Desktop\\SurGU\\3 курс\\ООП 3 курс\\4 лаба\\SoundCatalog.db"));
            })
            .Build(); // .Services.CreateScope();

    }

    public static int AddEntities()
    {
        // Добавляем данные в БД через службу.

        using var scope = _host.Services.CreateScope();
        var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();

        var song = new Song
        {
            nameSong = "Never gonna give u up",
        };

        return serviceProvider.AddSong(song);
    }

    public static int UpdateEntities()
    {
        // Обновляем данные в БД через службу.

        using var scope = _host.Services.CreateScope();
        var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();

        var songId = 1;
        var updatedSong = "Updated Never Gonna";

        return serviceProvider.UpdateSong(songId, updatedSong);
    }

    public static Song ReadEntities()
    {
        // Читаем данные из БД через службу.

        using var scope = _host.Services.CreateScope();
        var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();

        var songId = 2;

        return serviceProvider.ReadSong(songId);
    }

    public static int RemoveEntities()
    {
        // Удаляем данные в БД через службу.

        using var scope = _host.Services.CreateScope();

        int songName = 1;

        var serviceProvider = scope.ServiceProvider.GetRequiredService<ICatalogService>();
        return serviceProvider.RemoveSong(songName);
    }
}
