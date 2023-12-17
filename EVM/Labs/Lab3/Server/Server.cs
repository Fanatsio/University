using System.Diagnostics;
using System.IO.Pipes;
using System.Runtime.CompilerServices;

namespace Server
{
    public struct Structure
    {
        public int a;
        public int b;
        public double result;
    }

    class PipeServer
    {
        private static readonly PriorityQueue<Structure, int> dataQueue = new();
        private static readonly Mutex mutex = new();
        private static readonly Mutex mutFile = new();
        private static int count = 0;
        private static readonly string path = "D:\\EVM\\Labs\\Lab3\\Client\\bin\\Debug\\net7.0\\Client.exe";

        private static async Task Main()
        {
            CancellationTokenSource source = new();
            CancellationToken token = source.Token;
            StreamWriter file = new("output.txt", true);

            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                eventArgs.Cancel = true;
                source.Cancel();
            };

            try
            {
                await Task.WhenAll(SenderTask(token), ReceiverTask(token)); ;
            }
            catch (Exception error)
            {
                Console.WriteLine(error.Message);
            }
            finally
            {
                file.Close();
            }

            Task SenderTask(CancellationToken token)
            {
                return Task.Run(() =>
                {
                    while (!token.IsCancellationRequested)
                    {
                        int _n, _m, _priority;
                        Console.Write("Enter a, b, priority: ");
                        string? res = Console.ReadLine();
                        if (res == null)
                        {
                            Console.WriteLine("Invalid input");
                        }
                        else
                        {
                            string[] parse = res.Split(' ');
                            if (parse.Length == 2)
                            {
                                _n = int.Parse(parse[0]);
                                _m = int.Parse(parse[1]);
                                _priority = 0;
                            }
                            else
                            {
                                _n = int.Parse(parse[0]);
                                _m = int.Parse(parse[1]);
                                _priority = int.Parse(parse[2]);
                            }
                            Structure data = new()
                            {
                                a = _n,
                                b = _m,
                            };
                            mutex.WaitOne();
                            dataQueue.Enqueue(data, _priority);
                            mutex.ReleaseMutex();
                        }
                    }
                }, token);
            }

            Task ReceiverTask(CancellationToken token)
            {
                return Task.Run(() =>
                {
                    while (!token.IsCancellationRequested)
                    {
                        mutex.WaitOne();
                        bool flag = dataQueue.TryDequeue(out Structure st, out int pr);
                        mutex.ReleaseMutex();
                        if (flag)
                        {
                            ClientConnect(st, token);
                        }
                    }
                }, token);
            }

            async void ClientConnect(Structure st, CancellationToken token)
            {
                try
                {
                    NamedPipeServerStream pipeServer = new($"channel{count}", PipeDirection.InOut);
                    Console.WriteLine("Waiting for client connection...");
                    Process myProcess = new();
                    myProcess.StartInfo.UseShellExecute = false;
                    myProcess.StartInfo.FileName = path;
                    myProcess.StartInfo.Arguments = $"channel{count}";
                    myProcess.StartInfo.CreateNoWindow = true;
                    myProcess.Start();
                    await pipeServer.WaitForConnectionAsync(token);
                    Console.WriteLine("Client connected");

                    byte[] dataBytes = SerializeData(st);
                    await pipeServer.WriteAsync(dataBytes, token);

                    byte[] receivedBytes = new byte[Unsafe.SizeOf<Structure>()];
                    if (await pipeServer.ReadAsync(receivedBytes, token) == receivedBytes.Length)
                    {
                        st = Unsafe.As<byte, Structure>(ref receivedBytes[0]);
                    }

                    mutFile.WaitOne();
                    file.WriteLine($"a = {st.a}; b = {st.b}; priority = {0}; result = {st.result}");
                    Console.WriteLine($"a = {st.a}; b = {st.b}; priority = {0}; result = {st.result}");
                    mutFile.ReleaseMutex();

                    pipeServer.Close();
                    count++;
                    await myProcess.WaitForExitAsync(token);
                }
                catch (Exception) { }
            }
        }

        static byte[] SerializeData(Structure st)
        {
            byte[] dataBytes = new byte[Unsafe.SizeOf<Structure>()];
            Unsafe.As<byte, Structure>(ref dataBytes[0]) = st;
            return dataBytes;
        }
    }
}