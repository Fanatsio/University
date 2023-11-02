namespace Project1.Library
{
    public interface IPerimeter<T> where T : INumber<T>
    {
        T CalculatePerimeter();
        Task<T> CalculatePerimeterAsync(CancellationToken cancellationToken = default);
    }
}