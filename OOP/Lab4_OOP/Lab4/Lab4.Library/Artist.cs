namespace Lab4.Library
{
    public class Artist
    {
        public ICollection<Song>? Songs { get; set; }
        public int Id { get; set; }
        public string? NameArtist { get; set; }

    }
}
