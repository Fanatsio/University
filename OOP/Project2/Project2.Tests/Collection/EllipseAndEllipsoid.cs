// ReSharper disable All

namespace Project2.Tests;

[TestCaseOrderer(XunitOrderer.OrdererTypeName, XunitOrderer.OrdererAssemblyName)]
public sealed class EllipseAndEllipsoid
{
    [InlineData(false, new double[] { double.NaN, -2 })]
    [InlineData(false, new double[] { 12.566, 2 })]
    [InlineData(true, new double[] { double.NaN, -2, -10 })]
    [InlineData(true, new double[] { 8, 2, 10 })]
    [Theory, XunitOrdererFact(1)]
    public static void CalculatePerimeter(bool is3DFigure, double[] testData)
    {
        double result;
        uint counter = 0;

        try
        {
            result = FigureTestHelper.CalculatePerimeter(is3DFigure, testData[1..], ref counter);
        }
        catch (InvalidOperationException)
        {
            return;
        }
        catch (ArgumentOutOfRangeException)
        {
            return;
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }

        Assert.True(counter > 0, "Значение счётчика должно быть больше нуля.");

        Assert.Equal(testData[0], result);
    }

    [InlineData(false, new double[] { double.NaN, -2 })]
    [InlineData(false, new double[] { 12.566, 2 })]
    [InlineData(true, new double[] { double.NaN, -2, -10 })]
    [InlineData(true, new double[] { 44.199, 2, 10 })]
    [Theory, XunitOrdererFact(2)]
    public static void CalculateSquare(bool is3DFigure, double[] testData)
    {
        double result;
        uint counter = 0;

        try
        {
            result = FigureTestHelper.CalculateSquare(is3DFigure, testData[1..], ref counter);
        }
        catch (InvalidOperationException)
        {
            return;
        }
        catch (ArgumentOutOfRangeException)
        {
            return;
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }

        Assert.True(counter > 0, "Значение счётчика должно быть больше нуля.");

        Assert.Equal(testData[0], result);
    }

    [InlineData(false, new double[] { double.NaN, -2 })]
    [InlineData(false, new double[] { double.NaN, 2 })]
    [InlineData(true, new double[] { double.NaN, -2, -10 })]
    [InlineData(true, new double[] { 13.333, 2, 10 })]
    [Theory, XunitOrdererFact(3)]
    public static void CalculateVolume(bool is3DFigure, double[] testData)
    {
        double result;
        uint counter = 0;

        try
        {
            result = FigureTestHelper.CalculateVolume(is3DFigure, testData[1..], ref counter);
        }
        catch (InvalidOperationException)
        {
            return;
        }
        catch (ArgumentOutOfRangeException)
        {
            return;
        }
        catch (Exception error)
        {
            Assert.Fail($"Внимательно читаем сообщение об ошибке. Сообщение: «{error.Message}»");

            return;
        }

        Assert.True(counter > 0, "Значение счётчика должно быть больше нуля.");

        Assert.Equal(testData[0], result);
    }
}
