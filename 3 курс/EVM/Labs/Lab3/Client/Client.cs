using System.IO.Pipes;
using System.Runtime.CompilerServices;

namespace Client
{
    public struct Structure
    {
        public int a;
        public int b;
        public double result;
    }

    class Client
    {
        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                using NamedPipeClientStream Client = new(".", args[0], PipeDirection.InOut);
                Client.Connect();
                while (true)
                {
                    Structure receivedData = DeserializeData(Client);
                    Console.WriteLine($"Received data: a = {receivedData.a}, b = {receivedData.b}");

                    int a = receivedData.a;
                    int b = receivedData.b;
                    int n = 10000;

                    receivedData.result = Integral(a, b, n);
                    Console.WriteLine(receivedData.result);

                    byte[] modified_bytes = SerializeData(receivedData);
                    Client.Write(modified_bytes, 0, modified_bytes.Length);
                }
            }
        }

        static byte[] SerializeData(Structure receivedData)
        {
            byte[] modified_bytes = new byte[Unsafe.SizeOf<Structure>()];
            Unsafe.As<byte, Structure>(ref modified_bytes[0]) = receivedData;
            return modified_bytes;
        }

        public static Structure DeserializeData(NamedPipeClientStream Client)
        {
            byte[] bytes = new byte[Unsafe.SizeOf<Structure>()];
            Client.Read(bytes, 0, bytes.Length);
            return Unsafe.As<byte, Structure>(ref bytes[0]);
        }

        static double Function(double x)
        {
            return 3 * x * x * x;
        }

        static double Integral(int a, int b, int n)
        {
            double h = (b - a) / Convert.ToDouble(n);
            double result = 0.5 * (Function(a) + Function(b));

            for (int i = 1; i < n; i++)
            {

                double x = a + i * h;
                result += Function(x);
            }

            result *= h;
            Console.WriteLine(result);
            return result;
        }
    }
}