from Playlist import Playlist

class FirstFit:
    #First-Fit Algorithm
    
    def __init__(self):
        super().__init__()
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.ms = 0
        self.length = ""

    def print_length(self):
        return self.length

    def First_Fit(self, artist_songs, time_desired):

        #establish priority queue to hold the playlists and the duration of the playlist
        import heapq
        playlist_pq = []
        playlist_groups = []

        for song in artist_songs:
            entered_inside_playlist = False

            #iterate through the playlists in our playlist groups
            for playlist in playlist_groups:

                #if the playlist with the addition of the new song is less than the desired time, then continue
                if song.duration_ms + playlist.duration <= time_desired:
                    #add song to playlist, increment the playlist time length, and set true that the song was entered
                    playlist.songs.append(song)
                    playlist.duration += song.duration_ms
                    entered_inside_playlist = True
                    break

            if ~entered_inside_playlist:
                if song.duration_ms <= time_desired:

                    #make new playlist
                    playlist = Playlist(song, song.duration_ms)

                    #add the playlist to the list of playlists
                    playlist_groups.append(playlist)


        #find the playlist closest to the time desired
        #multiply the playlist duration time by -1 to make it a max heap
        for playlist in playlist_groups:
            heapq.heappush(playlist_pq, (-1 * playlist.duration, len(playlist.songs), id(playlist), playlist))

        self.hour = int(playlist_pq[0][3].duration / (60*60*1000))
        self.mins = int((playlist_pq[0][3].duration / (60*1000)) % 60)
        self.sec = int((playlist_pq[0][3].duration / 1000) % 60)
        self.ms = (playlist_pq[0][3].duration) % 1000

        if self.hour == 1:
            self.length += "\n" + "Playlist is " + str(self.hour) + " hour "
        elif self.hour > 1:
            self.length += "Playlist is " + str(self.hour) + " hours "
        
        if self.mins == 1:
            self.length += str(self.mins) +  " minute "
        elif self.mins > 1:
            self.length += str(self.mins) +  " minutes "

        if self.sec == 1:
            self.length += str(self.sec) + " second "
        elif self.sec > 1:
            self.length += str(self.sec) + " seconds "

        if self.sec == 1:
            self.length += " and " + str(self.ms) + " millisecond long!"
        else:
            self.length += " and " + str(self.ms) + " milliseconds long!"

        self.length += "\n\n" + "Playlist has " + str(len(playlist_pq[0][3].songs)) + " songs!" + "\n"

        #print songs
        # for song in playlist_pq[0][3].songs:
        #     print(song.name)

        return playlist_pq[0][3].songs
