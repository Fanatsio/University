namespace Lab4.Library
{
    public class Song
    {
        public ICollection<Artist>? Artists { get; set; }
        public int id { get; set; }
        public string? nameSong { get; set; }

    }
}
