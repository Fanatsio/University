namespace Project1.Library
{
    public class Ellipse<T> : Figure<T>, IDisposable where T : INumber<T>
    {
        readonly T _a;
        readonly T _b;

        public Ellipse(T a, T b) : base(nameof(Ellipse<T>), FigureType.SecondD)
        {
            if (a <= T.Zero || b <= T.Zero)
            {
                throw new ArgumentOutOfRangeException(nameof(a));
            }
            _a = a;
            _b = b;
        }

        public void Deconstruct(out T a, out T b)
        {
            a = _a;
            b = _b;
        }

        public override T CalculatePerimeter()
        {
            OnCalculatePerimeterEvent(EventArgs.Empty);
            T result = T.CreateChecked(4) * ((T.CreateChecked(double.Pi) * _a * _b + (_a + _b)) / (_a + _b));
            return T.CreateChecked(double.Round(double.CreateChecked(result), 3, MidpointRounding.ToZero));
        }

        public override T CalculateSquare()
        {
            OnCalculateSquareEvent(EventArgs.Empty);
            T result = T.CreateChecked(double.Pi) * _a * _b;
            return T.CreateChecked(Math.Round(double.CreateChecked(result), 3, MidpointRounding.ToZero));
        }

        public override T CalculateVolume()
        {
            OnCalculateVolumeEvent(EventArgs.Empty);
            throw new ArgumentOutOfRangeException();
        }

        public override async Task<T> CalculatePerimeterAsync(CancellationToken cancellationToken = default)
        {
            cancellationToken.ThrowIfCancellationRequested();
            T result = CalculatePerimeter();
            if (OnCalculatePerimeterAsyncEvent(EventArgs.Empty) is Task @event)
            {
                await @event;
            }
            return result;
        }

        public override async Task<T> CalculateSquareAsync(CancellationToken cancellationToken = default)
        {
            cancellationToken.ThrowIfCancellationRequested();
            T result = CalculateSquare();
            if (OnCalculateSquareAsyncEvent(EventArgs.Empty) is Task @event)
            {
                await @event;
            }
            return result;
        }

        public override async Task<T> CalculateVolumeAsync(CancellationToken cancellationToken = default)
        {
            cancellationToken.ThrowIfCancellationRequested();
            T result = CalculateVolume();
            if (OnCalculateVolumeAsyncEvent(EventArgs.Empty) is Task @event)
            {
                await @event;
            }
            return result;
        }

        public override void Save()
        {
            using StreamWriter writer = new(FileStream, leaveOpen: true);
            string str = @$"a = {_a}, b = {_b}, значит периметр равен: {CalculatePerimeter()}, площадь равна: {CalculateSquare()}";
            writer.Write(str);
            writer.Flush();
        }

        public override async Task SaveAsync(CancellationToken cancellationToken = default)
        {
            using StreamWriter writer = new(FileStream, leaveOpen: true);
            string str = @$"a = {_a}, b = {_b}, значит периметр равен: {CalculatePerimeter()}, Площадь равна: {CalculateSquare()}";
            await writer.WriteAsync(str);
            await writer.FlushAsync();
        }
    }
}