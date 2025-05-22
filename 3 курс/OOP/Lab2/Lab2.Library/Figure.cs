namespace Lab2.Library
{
    public abstract class Figure<T> : ISquare<T>, IPerimeter<T>, IVolume<T>, IDisposable where T : INumber<T>
    {
        protected Figure(string name, FigureType type)
        {
            Name = name;
            Type = type;
            FileStream = File.OpenWrite($"{name}.txt");
        }

        private bool disposedValue = false;
        public string Name { get; }
        public FigureType Type { get; }

        protected readonly Stream FileStream;

        public abstract void Save();
        public abstract Task SaveAsync(CancellationToken cancellationToken = default);

        public abstract T CalculatePerimeter();
        public abstract T CalculateSquare();
        public abstract T CalculateVolume();

        public abstract Task<T> CalculatePerimeterAsync(CancellationToken cancellationToken = default);
        public abstract Task<T> CalculateSquareAsync(CancellationToken cancellationToken = default);
        public abstract Task<T> CalculateVolumeAsync(CancellationToken cancellationToken = default);

        public event EventHandler<EventArgs>? CalculatePerimeterEvent;
        public event EventHandler<EventArgs>? CalculateSquareEvent;
        public event EventHandler<EventArgs>? CalculateVolumeEvent;

        protected virtual void OnCalculatePerimeterEvent(EventArgs args)
        {
            CalculatePerimeterEvent?.Invoke(this, args);
        }

        protected virtual void OnCalculateSquareEvent(EventArgs args)
        {
            CalculateSquareEvent?.Invoke(this, args);
        }

        protected virtual void OnCalculateVolumeEvent(EventArgs args)
        {
            CalculateVolumeEvent?.Invoke(this, args);
        }

        public event EventHandlerAsync<EventArgs>? CalculatePerimeterAsyncEvent;
        public event EventHandlerAsync<EventArgs>? CalculateSquareAsyncEvent;
        public event EventHandlerAsync<EventArgs>? CalculateVolumeAsyncEvent;

        protected virtual Task? OnCalculatePerimeterAsyncEvent(EventArgs args)
        {
            return CalculatePerimeterAsyncEvent?.Invoke(this, args);
        }

        protected virtual Task? OnCalculateSquareAsyncEvent(EventArgs args)
        {
            return CalculateSquareAsyncEvent?.Invoke(this, args);
        }

        protected virtual Task? OnCalculateVolumeAsyncEvent(EventArgs args)
        {
            return CalculateVolumeAsyncEvent?.Invoke(this, args);
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (disposedValue)
            {
                return;
            }
            if (disposing)
            {
                FileStream.Dispose();
            }
            disposedValue = true;
        }

        ~Figure()
        {
            Dispose(false);
        }
    }
}
public delegate Task EventHandlerAsync<TEventArgs>(object? sender, TEventArgs e);

