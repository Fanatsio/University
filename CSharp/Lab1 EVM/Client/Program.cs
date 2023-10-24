using System.IO.Pipes;
using System.Runtime.CompilerServices;

public struct Data
{
    public int num1;
    public int num2;
}

class PipeClient
{
    static void Main()
    {
        using NamedPipeClientStream pipeClient = new NamedPipeClientStream(".", "channel", PipeDirection.InOut);
        pipeClient.Connect();
        Console.WriteLine("Клиент подключился к серверу");

        byte[] bytes = new byte[Unsafe.SizeOf<Data>()];
        pipeClient.Read(bytes, 0, bytes.Length);
        Data received_data = Unsafe.As<byte, Data>(ref bytes[0]);

        Console.WriteLine("Число1: " + received_data.num1);
        Console.WriteLine("Число2: " + received_data.num2);

        byte[] modified_bytes = new byte[Unsafe.SizeOf<Data>()];
        Unsafe.As<byte, Data>(ref modified_bytes[0]) = received_data;
        pipeClient.Write(modified_bytes, 0, modified_bytes.Length);
        Console.ReadKey();
    }
}