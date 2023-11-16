namespace Project1.Library
{
    public class Ellipsoid<T> : Figure<T> where T : INumber<T>
    {
        private T _a;
        private T _b;
        private T _c;

        public Ellipsoid(T a, T b, T c) : base(nameof(Ellipsoid<T>), FigureType.ThreeD)
        {
            if (a <= T.Zero || b <= T.Zero || c <= T.Zero)
            {
                throw new ArgumentOutOfRangeException();
            }
            _a = a;
            _b = b;
            _c = c;
        }

        public void Deconstruct(out T a, out T b, out T c)
        {
            a = _a;
            b = _b;
            c = _c;
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
            T result = T.CreateChecked(4/3) * T.CreateChecked(double.Pi) * _a * _b * _c;
            return T.CreateChecked(Math.Round(double.CreateChecked(result), 3, MidpointRounding.ToZero));
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
            string str = @$"a = {_a}, b = {_b}, значит объем элипсоида равен {CalculateVolume()}";
            writer.Write(str);
            writer.Flush();
        }

        public override async Task SaveAsync(CancellationToken cancellationToken = default)
        {
            using StreamWriter writer = new(FileStream, leaveOpen: true);
            string str = @$"a = {_a}, b = {_b}, значит объем элипсоида равен {CalculateVolume()}";
            await writer.WriteAsync(str);
            await writer.FlushAsync();
        }
    }
}