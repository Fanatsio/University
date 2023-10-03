namespace Lab2
{
    internal class Program
    {
        class Figure
        {
            float CalculatePerimeter(float x, float y)
            {
                return x * y;
            }

            float CalculateSquare(float x, float y)
            {
                return x * y;
            }

            float CalculateVolume(float x, float y)
            {
                return x * y;
            }

            static async Task<int> CalculatePerimeterAsync(int number)
            {
                await Task.Delay(1000); // Имитируем долгую операцию (1 секунда задержки)
                int Perimeter = number + number;
                return Perimeter;
            }

            static async Task<int> CalculateSquareAsync(int number)
            {
                await Task.Delay(1000); // Имитируем долгую операцию (1 секунда задержки)
                int square = number * number;
                return square;
            }

            static async Task<int> CalculateVolumeAsync(int number)
            {
                await Task.Delay(1000); // Имитируем долгую операцию (1 секунда задержки)
                int Volume = number * number * number;
                return Volume;
            }
        }

        class Triangle : Figure
        {

        }

        interface INumber
        {
            int Value { get; } 
        }

        interface IPerimeter
        {
            float CalculatePerimeter();
            Task<int> CalculatePerimeterAsync();
        }

        interface ISquare
        {
            float CalculateSquare();
            Task<int> CalculateSquareAsync();
        }

        interface IVolume
        {
            float CalculateVolume();
            Task<int> CalculateVolumeAsync();
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
        }
    }
}