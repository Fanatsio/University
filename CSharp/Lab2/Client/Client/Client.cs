using System.IO.Pipes;

class Program
{
    static void Main()
    {
        using (NamedPipeClientStream pipeClient = new NamedPipeClientStream(".", "MyPipeServer", PipeDirection.InOut))
        {
            try
            {
                Console.WriteLine("Клиент пытается подключиться к серверу...");
                pipeClient.Connect();
                Console.WriteLine("Клиент успешно подключен к серверу.");

                while (true)
                {
                    byte[] receiveData = new byte[1024 * 10];
                    int bytesRead = pipeClient.Read(receiveData, 0, receiveData.Length);

                    MyData receivedData = DeserializeData(receiveData, bytesRead);
                    Console.WriteLine("Клиент получил данные от сервера: {0}, {1}", receivedData.Field1, receivedData.Field2);

                    MyData response = new MyData { Field1 = receivedData.Field1 * 2, Field2 = "Привет, сервер!" };
                    byte[] sendData = SerializeData(response);
                    pipeClient.Write(sendData, 0, sendData.Length);
                    Console.WriteLine("Клиент отправил данные серверу: {0}, {1}", response.Field1, response.Field2);
                }

                pipeClient.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Ошибка при подключении или обмене данными: " + ex.Message);
            }
        }

        Console.ReadLine();
    }

    public class MyData
    {
        public int Field1;
        public required string Field2;
        public int Priority;
    }

    static byte[] SerializeData(MyData data)
    {
        using (MemoryStream stream = new MemoryStream())
        using (BinaryWriter writer = new BinaryWriter(stream))
        {
            writer.Write(data.Field1);
            writer.Write(data.Field2);
            writer.Write(data.Priority);
            return stream.ToArray();
        }
    }

    public static MyData DeserializeData(byte[] data, int bytesRead)
    {
        using (MemoryStream stream = new MemoryStream(data, 0, bytesRead))
        using (BinaryReader reader = new BinaryReader(stream))
        {
            MyData result = new MyData
            {
                Field1 = reader.ReadInt32(),
                Field2 = reader.ReadString(),
                Priority = reader.ReadInt32()
            };
            return result;
        }
    }
}
