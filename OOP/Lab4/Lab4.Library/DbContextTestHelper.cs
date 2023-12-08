// ReSharper disable All

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Internal;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyModel;
using Microsoft.Extensions.Hosting;
using System.IO;
using System.Runtime.InteropServices.JavaScript;

namespace Lab4.Library
{
    public static class DbContextTestHelper
    {
        static DbContextTestHelper()
        {
            // Создаем и настраиваем IoC - контейнер.
        }

        public static int AddEntities()
        {
            // Добавляем данные в БД через службу.

            return 0;
        }

        public static int UpdateEntities()
        {
            // Обновляем данные в БД через службу.

            return 0;
        }

        public static int ReadEntities()
        {
            // Читаем данные из БД через службу.

            return 0;
        }

        public static int RemoveEntities()
        {
            // Удаляем данные в БД через службу.

            return 0;
        }
    }
}
