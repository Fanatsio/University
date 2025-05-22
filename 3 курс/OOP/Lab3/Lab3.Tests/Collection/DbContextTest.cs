// ReSharper disable All

namespace Lab3.Tests;

[TestCaseOrderer(XunitOrderer.OrdererTypeName, XunitOrderer.OrdererAssemblyName)]
public sealed class DbContextTest
{
    [Fact, XunitOrdererFact(1)]
    public void AddEntities()
    {
        int count;

        try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }

        Assert.True(count > 0, "Кол-во добавляемых записей должно быть больше нуля.");
    }

    [Fact, XunitOrdererFact(2)]
    public void UpdateEntities()
    {
        int count;

        try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }

        Assert.True(count > 0, "Кол-во обновляемых записей должно быть больше нуля.");
    }

    [Fact, XunitOrdererFact(3)]
    public void ReadEntities()
    {
        int count;

        try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }

        Assert.True(count > 0, "Кол-во прочитанных записей должно быть больше нуля.");
    }

    [Fact, XunitOrdererFact(4)]
    public void RemoveEntities()
    {
        int count;

        try
        {
            count = DbContextTestHelper.AddEntities();
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }

        Assert.True(count > 0, "Кол-во удаляемых записей должно быть больше нуля.");
    }
}
