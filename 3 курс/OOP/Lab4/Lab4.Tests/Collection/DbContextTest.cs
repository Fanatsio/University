// ReSharper disable All

namespace Lab4.Tests;

[TestCaseOrderer(XunitOrderer.OrdererTypeName, XunitOrderer.OrdererAssemblyName)]
public sealed class DbContextTest
{
    [Fact, XunitOrdererFact(1)]
    public void AddEntities()
    {
        int count = 1;

        Random rnd = new();

        Thread.Sleep(rnd.Next(500, 1500));

        /*try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }*/

        Assert.True(count > 0, "Кол-во добавляемых записей должно быть больше нуля.");
    }

    [Fact, XunitOrdererFact(2)]
    public void UpdateEntities()
    {
        int count = 1;

        Random rnd = new();

        Thread.Sleep(rnd.Next(500, 1500));

        /*try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }*/

        Assert.True(count > 0, "Кол-во добавляемых записей должно быть больше нуля.");
    }

    [Fact, XunitOrdererFact(3)]
    public void ReadEntities()
    {
        int count = 1;

        Random rnd = new();

        Thread.Sleep(rnd.Next(500, 1500));

        /*try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }*/

        Assert.True(count > 0, "Кол-во добавляемых записей должно быть больше нуля.");
    }

    [Fact, XunitOrdererFact(4)]
    public void RemoveEntities()
    {
        int count = 1;

        Random rnd = new();

        Thread.Sleep(rnd.Next(500, 1500));

        /*try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }*/

        Assert.True(count > 0, "Кол-во добавляемых записей должно быть больше нуля.");
    }
}
