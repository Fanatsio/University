namespace Lab4.Library
{
    internal interface ICatalogService
    {
        int AddSong(Song nameSong);
        int AddArtist(Artist artist);

        int UpdateSong(int Id, string updatedSong);
        int UpdateArtist(int Id, string updatedArtist);

        Song ReadSong(int songId);
        Artist ReadArtist(int artistId);

        //int RemoveSong(string songName);
        int RemoveArtist(string nameArtist);
        int RemoveSong(int songName);
    }
}
