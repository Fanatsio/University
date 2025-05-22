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
            if (!int.TryParse(Console.ReadLine(), out int _num1))
            {
                _num1 = 0;
            }
            Console.Write("Введите второе число: ");
            if (!int.TryParse(Console.ReadLine(), out int _num2))
            {
                _num2 = 0;
            }

            Data msg = new()
            {
                num1 = _num1,
                num2 = _num2
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