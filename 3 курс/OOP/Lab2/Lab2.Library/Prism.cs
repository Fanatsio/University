namespace Lab2.Library
{
    public class Prism<T> : Figure<T> where T : INumber<T>
    {
        readonly T _a;
        readonly T _h;

        public Prism(T a, T h) : base(nameof(Prism<T>), FigureType.ThreeD)
        {
            if (a <= T.Zero || h <= T.Zero)
            {
                throw new ArgumentOutOfRangeException();
            }
            _a = a;
            _h = h;
        }

        public void Deconstruct(out T a, out T h)
        {
            a = _a;
            h = _h;
        }

        public override T CalculatePerimeter()
        {
            OnCalculatePerimeterEvent(EventArgs.Empty);
            T result = T.CreateChecked(6) * _a + T.CreateChecked(3) *_h;
            return T.CreateChecked(double.Round(double.CreateChecked(result), 3, MidpointRounding.ToZero));
        }

        public override T CalculateSquare()
        {
            OnCalculateSquareEvent(EventArgs.Empty);
            T result = T.CreateChecked(3) * _a * _h + (T.CreateChecked(Math.Sqrt(3)) * _a * _a) / (T.CreateChecked(2));
            return T.CreateChecked(Math.Round(double.CreateChecked(result), 3, MidpointRounding.ToZero));
        }

        public override T CalculateVolume()
        {
            OnCalculateVolumeEvent(EventArgs.Empty);
            T result = (T.CreateChecked(Math.Sqrt(3)) * _a * _a) / (T.CreateChecked(4)) * _h;
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
            string str = @$"a = {_a}, h = {_h}, значит объем элипсоида равен {CalculateVolume()}";
            writer.Write(str);
            writer.Flush();
        }

        public override async Task SaveAsync(CancellationToken cancellationToken = default)
        {
            using StreamWriter writer = new(FileStream, leaveOpen: true);
            string str = @$"a = {_a}, h = {_h}, значит объем элипсоида равен {CalculateVolume()}";
            await writer.WriteAsync(str);
            await writer.FlushAsync();
        }
    }
}