using System.IO.Pipes;
using System.Runtime.CompilerServices;

namespace Server
{
    public struct Structure
    {
        public int num1;
        public int num2;
        public int pr;
    }

    class PipeServer
    {
        private static readonly PriorityQueue<Structure, int> dataQueue = new();
        private static readonly Mutex mutex = new();

        static async Task Main()
        {
            using NamedPipeServerStream pipeServer = new("channel", PipeDirection.InOut);
            Console.WriteLine("Ожидание подключения клиента...");
            await pipeServer.WaitForConnectionAsync();
            Console.WriteLine("Клиент подключен");

            CancellationTokenSource senderSource = new();
            CancellationToken senderToken = senderSource.Token;

            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                if (!eventArgs.Cancel)
                {
                    eventArgs.Cancel = true;
                    senderSource.Cancel();
                }
            };

            await Task.WhenAll(SenderTask(senderToken), ReceiverTask(pipeServer, senderToken));
        }

        static void CreateQueue()
        {
            Console.Write("Введите num1: ");
            if (!int.TryParse(Console.ReadLine(), out int _num1))
            {
                _num1 = 0;
            }
            Console.Write("Введите num2: ");
            if (!int.TryParse(Console.ReadLine(), out int _num2))
            {
                _num2 = 0;
            }
            Console.Write("Введите приоритетность: ");
            if (!int.TryParse(Console.ReadLine(), out int _priority))
            {
                _priority = 0;
            }
            Structure data = new()
            {
                num1 = _num1,
                num2 = _num2,
                pr = _priority
            };
            mutex.WaitOne();
            dataQueue.Enqueue(data, _priority);
            Console.WriteLine(dataQueue.Count);
            mutex.ReleaseMutex();
        }

        private static async Task SenderTask(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                CreateQueue();
                await Task.Delay(100);
            }
        }

        private static async Task ReceiverTask(NamedPipeServerStream pipeServer, CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                mutex.WaitOne();
                bool flag = dataQueue.TryDequeue(out Structure st, out _);
                mutex.ReleaseMutex();
                if (flag)
                {
                    byte[] dataBytes = SerializeData(st);
                    await pipeServer.WriteAsync(dataBytes);
                    st = DeserializeData(pipeServer);
                    Console.WriteLine($"Клиент получил: num1 = {st.num1}; num2 = {st.num2}; приоритет = {st.pr}");
                }
            }
            await Task.Delay(100);
        }

        static byte[] SerializeData(Structure st)
        {
            int size = Unsafe.SizeOf<Structure>();
            byte[] dataBytes = new byte[size];
            Unsafe.As<byte, Structure>(ref dataBytes[0]) = st;
            return dataBytes;
        }

        public static Structure DeserializeData(NamedPipeServerStream pipeServer)
        {
            int size = Unsafe.SizeOf<Structure>();
            byte[] bytes = new byte[size];
            pipeServer.Read(bytes, 0, bytes.Length);
            return Unsafe.As<byte, Structure>(ref bytes[0]);
        }
    }
}
