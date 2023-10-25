using System.IO.Pipes;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;


public struct Structure
{
    public int num1;
    public int num2;
    public int pr;
}

class PipeServer
{
    private static PriorityQueue<Structure, int> dataQueue = new PriorityQueue<Structure, int>();
    private static Mutex mutex = new Mutex();

    private static Task Main()
    {
        CancellationTokenSource source = new CancellationTokenSource();
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
                    int _num1, _num2, _priority;
                    Console.Write("Введите num1: ");
                    int.TryParse(Console.ReadLine(), out _num1);
                    Console.Write("Введите num2: ");
                    int.TryParse(Console.ReadLine(), out _num2);
                    Console.Write("Введите приоритетность: ");
                    if (!int.TryParse(Console.ReadLine(), out _priority))
                    {
                        _priority = 0;
                    }
                    Structure data = new Structure
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
            });
        }

        Task ReceiverTask(NamedPipeServerStream pipeServer, CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                Structure st;
                int priority;
                mutex.WaitOne();
                bool flag = dataQueue.TryDequeue(out st, out priority);
                mutex.ReleaseMutex();
                if (flag)
                {
                    byte[] dataBytes = new byte[Unsafe.SizeOf<Structure>()];
                    Unsafe.As<byte, Structure>(ref dataBytes[0]) = st;
                    pipeServer.Write(dataBytes, 0, dataBytes.Length);
                    byte[] receivedBytes = new byte[Unsafe.SizeOf<Structure>()];
                    if (pipeServer.Read(receivedBytes, 0, receivedBytes.Length) == receivedBytes.Length)
                    {
                        st = Unsafe.As<byte, Structure>(ref receivedBytes[0]);
                    }
                    str += $"num1 = {st.num1}; num2 = {st.num2}; приоритет= {st.pr}";
                }
            }
            return Task.CompletedTask;
        }
    }
}
