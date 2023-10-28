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
            CancellationTokenSource source = new();
            CancellationToken token = source.Token;

            using NamedPipeServerStream pipeServer = new("channel", PipeDirection.InOut);
            Console.WriteLine("Ожидание подключения клиента...");
            await pipeServer.WaitForConnectionAsync();
            string str = string.Empty;
            Console.WriteLine("Клиент подключен");

            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                source.Cancel();
            };

            await Task.WhenAll(SenderTask(token), ReceiverTask(pipeServer, token));
        }

        private static async Task SenderTask(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                Console.WriteLine("Введите num1: ", token);
                _ = int.TryParse(Console.ReadLine(), out int _num1);
                Console.WriteLine("Введите num2: ", token);
                _ = int.TryParse(Console.ReadLine(), out int _num2);
                Console.WriteLine("Введите приоритетность: ", token);
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
                await Task.Delay(1000, token);
            }
        }

        private static async Task ReceiverTask(NamedPipeServerStream pipeServer, CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                mutex.WaitOne();
                bool flag = dataQueue.TryDequeue(out Structure st, out int priority);
                mutex.ReleaseMutex();
                if (flag)
                {
                    byte[] dataBytes = SerializeData(st);
                    await pipeServer.WriteAsync(dataBytes, token);
                    st = DeserializeData(pipeServer);
                    Console.WriteLine($"num1 = {st.num1}; num2 = {st.num2}; приоритет= {st.pr}");
                }
                await Task.Delay(1000, token);
            }
        }

        static byte[] SerializeData(Structure st)
        {
            byte[] dataBytes = new byte[Unsafe.SizeOf<Structure>()];
            Unsafe.As<byte, Structure>(ref dataBytes[0]) = st;
            return dataBytes;
        }

        public static Structure DeserializeData(NamedPipeServerStream pipeServer)
        {
            byte[] receivedBytes = new byte[Unsafe.SizeOf<Structure>()];
            if (pipeServer.Read(receivedBytes, 0, receivedBytes.Length) == receivedBytes.Length)
            {
                return Unsafe.As<byte, Structure>(ref receivedBytes[0]);
            }
            return new Structure();
        }
    }
}
