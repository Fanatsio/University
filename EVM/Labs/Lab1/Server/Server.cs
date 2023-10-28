using System.IO.Pipes;
using System.Runtime.CompilerServices;

namespace Server
{
    public struct Data
    {
        public int num1;
        public int num2;
    }

    class PipeServer
    {
        static void Main()
        {
            using NamedPipeServerStream pipeServer = new("channel", PipeDirection.InOut);
            Console.WriteLine("Ожидается подключения клиента к серверу");
            pipeServer.WaitForConnection();
            Console.WriteLine("Клиент подключен");

            StreamWriter sw = new(pipeServer)
            {
                AutoFlush = true
            };

            Console.Write("Введите первое число: ");
            int num_1 = int.Parse(Console.ReadLine());
            Console.Write("Введите второе число: ");
            int num_2 = int.Parse(Console.ReadLine());


            Data msg = new()
            {
                num1 = num_1,
                num2 = num_2
            };

            byte[] bytes = SerializeData(msg);
            sw.BaseStream.Write(bytes, 0, bytes.Length);

            Data received_data = DeserializeData(sw);
            Console.WriteLine($"Полученные данные: первое число = {received_data.num1}, второе число = {received_data.num2}");

            Console.ReadKey();
        }

        static byte[] SerializeData(Data msg)
        {
            byte[] bytes = new byte[Unsafe.SizeOf<Data>()];
            Unsafe.As<byte, Data>(ref bytes[0]) = msg;
            return bytes;
        }

        public static Data DeserializeData(StreamWriter sw)
        {
            byte[] received_bytes = new byte[Unsafe.SizeOf<Data>()];
            sw.BaseStream.Read(received_bytes, 0, received_bytes.Length);
            return Unsafe.As<byte, Data>(ref received_bytes[0]);
        }
    }
}