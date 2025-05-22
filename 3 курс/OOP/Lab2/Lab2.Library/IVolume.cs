namespace Lab2.Library
{
    public interface IVolume<T> where T : INumber<T>
    {
        T CalculateVolume();
        Task<T> CalculateVolumeAsync(CancellationToken cancellationToken = default);
    }
}