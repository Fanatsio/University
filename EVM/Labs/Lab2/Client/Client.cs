using System.IO.Pipes;
using System.Runtime.CompilerServices;

namespace Client
{
    public struct Structure
    {
        public int num1;
        public int num2;
        public int priority;
    }

    class Client
    {
        static void Main()
        {
            using NamedPipeClientStream Client = new(".", "channel", PipeDirection.InOut);
            Console.WriteLine("Подключение к серверу...");
            Client.Connect();
            Console.WriteLine("Клиент подключился к серверу");
            while (true)
            {
                Structure receivedData = DeserializeData(Client);
                Console.WriteLine($"Полученные данные: num1 = {receivedData.num1}, num2 = {receivedData.num2}, приоритет = {receivedData.priority}");
                if(Client.IsConnected)
                {
                    byte[] modified_bytes = SerializeData(receivedData);
                    Client.Write(modified_bytes, 0, modified_bytes.Length);
                } else
                {
                    break;
                }
            }
        }

        static byte[] SerializeData(Structure receivedData)
        {
            int size = Unsafe.SizeOf<Structure>();
            byte[] modified_bytes = new byte[size];
            Unsafe.As<byte, Structure>(ref modified_bytes[0]) = receivedData;
            return modified_bytes;
        }

        public static Structure DeserializeData(NamedPipeClientStream Client)
        {
            int size = Unsafe.SizeOf<Structure>();
            byte[] bytes = new byte[size];
            Client.Read(bytes, 0, bytes.Length);
            return Unsafe.As<byte, Structure>(ref bytes[0]);
        }
    }
}