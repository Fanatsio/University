using Microsoft.EntityFrameworkCore;

namespace Lab4.Library
{
    internal class CatalogService : ICatalogService
    {
        private readonly IDbContextFactory<CatalogContext> _contextFactory;

        public CatalogService(IDbContextFactory<CatalogContext> contextFactory)
        {
            _contextFactory = contextFactory;
        }

        public int AddSong(Song song)
        {
            using var context = _contextFactory.CreateDbContext();
            context.Songs.Add(song);
            return context.SaveChanges();
        }

        public int AddArtist(Artist artist)
        {
            using var context = _contextFactory.CreateDbContext();
            context.Artists.Add(artist);
            return context.SaveChanges();
        }

        public int UpdateSong(int Id, string updatedSong)
        {
            using var context = _contextFactory.CreateDbContext();
            var song = context.Songs.Find(Id);
            if (song != null)
            {
                song.nameSong = updatedSong;
                context.Songs.Update(song);
                return context.SaveChanges();
            }
            return 0;
        }

        public int UpdateArtist(int Id, string updatedArtist)
        {
            using var context = _contextFactory.CreateDbContext();
            var artist = context.Artists.Find(Id);
            if (artist != null)
            {
                artist.NameArtist = updatedArtist;
                context.Artists.Update(artist);
                return context.SaveChanges();
            }
            return 0;
        }

        public Song ReadSong(int Id)
        {
            using var context = _contextFactory.CreateDbContext();
            return context.Songs.Find(Id);
        }

        public Artist ReadArtist(int Id)
        {
            using var context = _contextFactory.CreateDbContext();
            return context.Artists.Find(Id);
        }


        public int RemoveSong(int songName)
        {
            using var context = _contextFactory.CreateDbContext();
            var song = context.Songs.Find(songName);
            if (song != null)
            {
                context.Songs.Remove(song);
                return context.SaveChanges();
            }
            return 0;
        }

        public int RemoveArtist(string nameArtist)
        {
            using var context = _contextFactory.CreateDbContext();
            var artist = context.Artists.Find(nameArtist);
            if (artist != null)
            {
                context.Artists.Remove(artist);
                return context.SaveChanges();
            }
            return 0;
        }
    }
}
