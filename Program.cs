using System.IO.Pipes;
using System.Runtime.InteropServices;

class Program
{
    static void Main()
    {
        using (NamedPipeClientStream pipeClient = new NamedPipeClientStream(".", "MyPipeServer", PipeDirection.InOut))
        {
            Console.WriteLine("Клиент пытается подключиться к серверу...");
            pipeClient.Connect();

            try
            {
                byte[] receiveData = new byte[1024 * 10];

                int bytesRead = pipeClient.Read(receiveData, 0, receiveData.Length);

                MyData receivedData = DeserializeData(receiveData, bytesRead);
                Console.WriteLine("Клиент получил данные от сервера: {0}, {1}", receivedData.Field1, receivedData.Field2);

                MyData response = new MyData { Field1 = 123, Field2 = "Привет, сервер!" };
                byte[] sendData = SerializeData(response);
                pipeClient.Write(sendData, 0, sendData.Length);
                Console.WriteLine("Клиент отправил ответ серверу: {0}, {1}", response.Field1, response.Field2);
                System.Threading.Thread.Sleep(50000);
            }
            finally
            {
                pipeClient.Close();
            }
        }
    }

    public struct MyData
    {
        public int Field1;
        public string Field2;
    }

    static byte[] SerializeData(MyData data)
    {
        using (MemoryStream stream = new MemoryStream())
        using (BinaryWriter writer = new BinaryWriter(stream))
        {
            writer.Write(data.Field1);
            writer.Write(data.Field2);
            return stream.ToArray();
        }
    }

    public static MyData DeserializeData(byte[] data, int bytesRead)
    {
        if (bytesRead != Marshal.SizeOf(typeof(MyData)))
        {
            throw new ArgumentException($"Неверное количество считанных байтов ({bytesRead}), ожидалось {Marshal.SizeOf(typeof(MyData))} для десериализации.");
        }

        using (MemoryStream stream = new MemoryStream(data))
        using (BinaryReader reader = new BinaryReader(stream))
        {
            MyData result;
            result.Field1 = reader.ReadInt32();
            result.Field2 = reader.ReadString();
            return result;
        }
    }
}
