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

        private static Task Main()
        {
            CancellationTokenSource source = new();
            CancellationToken token = source.Token;
            using NamedPipeServerStream pipeServer = new("channel", PipeDirection.InOut);
            Console.WriteLine("Ожидание подключения клиента...");
            pipeServer.WaitForConnection();
            string str = string.Empty;
            Console.WriteLine("Клиент подключен");

            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                source.Cancel();
            };

            return Task.WhenAll(SenderTask(pipeServer, token), ReceiverTask(pipeServer, token));

            Task SenderTask(NamedPipeServerStream pipeServer, CancellationToken token)
            {
                return Task.Run(() =>
                {
                    while (!token.IsCancellationRequested)
                    {
                        Console.Write("Введите num1: ");
                        _ = int.TryParse(Console.ReadLine(), out int _num1);
                        Console.Write("Введите num2: ");
                        _ = int.TryParse(Console.ReadLine(), out int _num2);
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
                }, token);
            }

            Task ReceiverTask(NamedPipeServerStream pipeServer, CancellationToken token)
            {
                while (!token.IsCancellationRequested)
                {
                    mutex.WaitOne();
                    bool flag = dataQueue.TryDequeue(out Structure st, out int priority);
                    mutex.ReleaseMutex();
                    if (flag)
                    {

                        byte[] dataBytes = SerializeData(st);
                        pipeServer.Write(dataBytes, 0, dataBytes.Length);
                        st = DeserializeData(pipeServer);
                        str += $"num1 = {st.num1}; num2 = {st.num2}; приоритет= {st.pr}";
                    }
                }
                return Task.CompletedTask;
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
            return Unsafe.As<byte, Structure>(ref receivedBytes[0]);
        }
    }
}