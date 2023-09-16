﻿using System.IO.Pipes;

class Server
{
    static void Main()
    {
        using (NamedPipeServerStream pipeServer = new NamedPipeServerStream("MyPipeServer", PipeDirection.InOut))
        {
            Console.WriteLine("Сервер ожидает подключения...");
            pipeServer.WaitForConnection();

            try
            {
                MyData dataToSend = new MyData {Field1 = 42, Field2 = "Helloclient"};

                byte[] sendData = SerializeData(dataToSend);

                pipeServer.Write(sendData, 0, sendData.Length);
                Console.WriteLine("Сервер отправил данные: {0}", dataToSend);

                byte[] receiveData = new byte[1024 * 10];
                int bytesRead = pipeServer.Read(receiveData, 0, receiveData.Length);

                MyData receivedData = DeserializeData(receiveData, bytesRead);
                Console.WriteLine("Сервер получил ответ от клиента: {0}", receivedData);
            }
            finally
            {
                pipeServer.Close();
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
