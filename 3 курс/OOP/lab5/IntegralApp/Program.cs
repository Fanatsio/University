using IntegralCalculatorLib;

namespace IntegralApp
{
    class Program
    {
        static void Main(string[] args)
        {
            double a = -Math.PI / 2, b = Math.PI / 2;
            int n = 1000; // Количество разбиений

            double result = IntegralCalculator.Calculate(a, b, n);

            Console.WriteLine($"Integral of 2*cos(x) from {a} to {b} is approximately: {result}");
        }
    }
}