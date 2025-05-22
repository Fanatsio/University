using System.IO.Pipes;
using System.Runtime.CompilerServices;

namespace Client
{
    public struct Data
    {
        public int num1;
        public int num2;
    }

    class PipeClient
    {
        static void Main()
        {
            using NamedPipeClientStream pipeClient = new(".", "channel", PipeDirection.InOut);
            Console.WriteLine("Подключение к серверу...");
            pipeClient.Connect();
            Console.WriteLine("Клиент подключился к серверу");

            Data received_data = DeserializeData(pipeClient);

            Console.WriteLine("Число1: " + received_data.num1);
            Console.WriteLine("Число2: " + received_data.num2);

            byte[] modified_bytes = SerializeData(received_data);
            pipeClient.Write(modified_bytes, 0, modified_bytes.Length);
            Console.WriteLine("Клиент отправил ответ серверу о получении сообщения");

            Console.ReadKey();
        }

        static byte[] SerializeData(Data received_data)
        {
            byte[] modified_bytes = new byte[Unsafe.SizeOf<Data>()];
            Unsafe.As<byte, Data>(ref modified_bytes[0]) = received_data;
            return modified_bytes;
        }

        public static Data DeserializeData(NamedPipeClientStream pipeClient)
        {
            byte[] bytes = new byte[Unsafe.SizeOf<Data>()];
            pipeClient.Read(bytes, 0, bytes.Length);
            return Unsafe.As<byte, Data>(ref bytes[0]);
        }
    }
}