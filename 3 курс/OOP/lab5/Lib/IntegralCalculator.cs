// IntegralCalculator.cs
using System.Runtime.InteropServices;

namespace IntegralCalculatorLib;

public class IntegralCalculator
{
    // Импорт функции из нативной библиотеки
    [DllImport("libintegral", CallingConvention = CallingConvention.Cdecl,EntryPoint ="integrate",SetLastError =true)]
    private static extern double Integrate(double a, double b, int n);

    public static double Calculate(double a, double b, int n)
    {
        return Integrate(a, b, n);
    }
}
