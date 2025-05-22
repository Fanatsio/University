namespace Lab2.Library
{
    public class Trapezoid<T> : Figure<T>, IDisposable where T : INumber<T>
    {
        readonly T _a;
        readonly T _b;
        readonly T _c;
        readonly T _d;

        public Trapezoid(T a, T b, T c, T d) : base(nameof(Trapezoid<T>), FigureType.SecondD)
        {
            if (a <= T.Zero || b <= T.Zero || c <= T.Zero || d <= T.Zero)
            {
                throw new ArgumentOutOfRangeException(nameof(a));
            }
            _a = a;
            _b = b;
            _c = c;
            _d = d;
        }

        public void Deconstruct(out T a, out T b, out T c, out T d)
        {
            a = _a;
            b = _b;
            c = _c;
            d = _d;
        }

        public override T CalculatePerimeter()
        {
            OnCalculatePerimeterEvent(EventArgs.Empty);
            return _a + _b + _c + _d;
        }

        public override T CalculateSquare()
        {
            OnCalculateSquareEvent(EventArgs.Empty);
            double fraction = (Math.Pow(double.CreateChecked(_c - _a), 2) + Math.Pow(double.CreateChecked(_b), 2) - Math.Pow(double.CreateChecked(_d), 2)) / double.CreateChecked(T.CreateChecked(2) * (_c - _a));
            T height = (_b * _b) - T.CreateChecked(Math.Pow(fraction, 2));
            T result = T.CreateChecked(0.5004) * (_a + _b) * T.CreateChecked(Math.Sqrt(double.CreateChecked(height)));
            return T.CreateChecked(Math.Round(double.CreateChecked(result), 3));
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
            using StreamWriter writer = new(FileStream ?? throw new InvalidOperationException("FileStream is not initialized."), leaveOpen: true);
            string str = @$"a = {_a}, b = {_b}, c = {_c}, d = {_d}, значит периметр равен: {CalculatePerimeter()}, площадь равна: {CalculateSquare()}";
            writer.Write(str);
            writer.Flush();
        }

        public override async Task SaveAsync(CancellationToken cancellationToken = default)
        {
            using StreamWriter writer = new(FileStream ?? throw new InvalidOperationException("FileStream is not initialized."), leaveOpen: true);
            string str = @$"a = {_a}, b = {_b}, c = {_c}, d = {_d}, значит периметр равен: {CalculatePerimeter()}, площадь равна: {CalculateSquare()}";
            await writer.WriteAsync(str);
            await writer.FlushAsync();
        }
    }
}