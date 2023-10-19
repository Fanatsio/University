using System.IO.Pipes;

class Server
{
    static void Main()
    {
        using (NamedPipeServerStream pipeServer = new NamedPipeServerStream("MyPipeServer", PipeDirection.InOut))
        {
            Console.WriteLine("Сервер ожидает подключения...");
            pipeServer.WaitForConnection();

            var dataQueue = new PriorityQueue<MyData>((x, y) => x.Priority.CompareTo(y.Priority));
            var receivedDataBuffer = new List<MyData>();

            CancellationTokenSource cts = new CancellationTokenSource();
            Console.CancelKeyPress += (s, e) =>
            {
                e.Cancel = true;
                cts.Cancel();
            };

            var processingTask = Task.Run(async() =>
            {
                while (!cts.Token.IsCancellationRequested)
                {
                    if (dataQueue.Count > 0)
                    {
                        MyData dataToSend = dataQueue.Dequeue();
                        byte[] sendData = SerializeData(dataToSend);

                        pipeServer.Write(sendData, 0, sendData.Length);
                        Console.WriteLine("Сервер отправил данные: {0}, {1}", dataToSend.Field1, dataToSend.Field2);
                    }

                    byte[] receiveData = new byte[1024 * 10];
                    int bytesRead = pipeServer.Read(receiveData, 0, receiveData.Length);

                    MyData receivedData = DeserializeData(receiveData, bytesRead);
                    receivedDataBuffer.Add(receivedData);
                }
            });

            while (!cts.Token.IsCancellationRequested)
            {
                MyData data = new MyData { Field1 = 42, Field2 = "Helloclient", Priority = 1 };
                dataQueue.Enqueue(data);

                MyData highPriorityData = new MyData { Field1 = 99, Field2 = "HighPriority", Priority = 1 };
                dataQueue.Enqueue(highPriorityData);

                Thread.Sleep(1000);
            }

            processingTask.Wait();
        }
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
            MyData result = new()
            {
                Field1 = reader.ReadInt32(),
                Field2 = reader.ReadString(),
                Priority = reader.ReadInt32()
            };
            return result;
        }
    }


    public class PriorityQueue<T>
    {
        private List<T> data;
        private Func<T, T, int> comparer;

        public PriorityQueue(Func<T, T, int> comparer)
        {
            this.data = new List<T>();
            this.comparer = comparer;
        }

        public int Count => data.Count;

        public void Enqueue(T item)
        {
            data.Add(item);
            int childIndex = data.Count - 1;
            while (childIndex > 0)
            {
                int parentIndex = (childIndex - 1) / 2;
                if (comparer(data[childIndex], data[parentIndex]) >= 0)
                    break;
                Swap(childIndex, parentIndex);
                childIndex = parentIndex;
            }
        }

        public T Dequeue()
        {
            if (data.Count == 0)
                throw new InvalidOperationException("Queue is empty.");
            int lastIndex = data.Count - 1;
            T frontItem = data[0];
            data[0] = data[lastIndex];
            data.RemoveAt(lastIndex);
            lastIndex--;
            int parentIndex = 0;
            while (true)
            {
                int leftChildIndex = 2 * parentIndex + 1;
                if (leftChildIndex > lastIndex)
                    break;
                int rightChildIndex = leftChildIndex + 1;
                if (rightChildIndex <= lastIndex && comparer(data[rightChildIndex], data[leftChildIndex]) < 0)
                    leftChildIndex = rightChildIndex;
                if (comparer(data[leftChildIndex], data[parentIndex]) >= 0)
                    break;
                Swap(leftChildIndex, parentIndex);
                parentIndex = leftChildIndex;
            }
            return frontItem;
        }

        private void Swap(int i, int j)
        {
            T temp = data[i];
            data[i] = data[j];
            data[j] = temp;
        }
    }
}
