#Best-Fit
from Playlist import Playlist

#Best-Fit Algorithm
class BestFit:
    
    def __init__(self):
        super().__init__()
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.ms = 0
        self.length = ""

    def print_length(self):
        return self.length

    def Best_Fit(self,artist_songs, time_desired):
        import heapq
        playlist_heap = []
        temp_storage = []

        for song in artist_songs:
            entered_inside_playlist = False

            #iterate through the playlists in the heap
            while playlist_heap:

                #remove smallest empty bin size
                best_bin = heapq.heappop(playlist_heap)

                #keep track of the popped playlists
                temp_storage.append(best_bin)

                #if the new song duration is less than or equal to the empty bin space, then continue
                if song.duration_ms <= best_bin[0]:
                    #add song to playlist, increment the playlist time length, and set true that the song was entered
                    best_bin[3].songs.append(song)
                    best_bin[3].duration += song.duration_ms
                    entered_inside_playlist = True

                    #decrement the empty bin space and increment number of songs in playlist
                    updated_best_bin = (best_bin[0] - song.duration_ms, best_bin[1] + 1, id(best_bin[3]), best_bin[3])

                    #replace the selected bin with the updated bin
                    temp_storage[len(temp_storage) - 1] = updated_best_bin
                    break


            if ~entered_inside_playlist:
                if song.duration_ms <= time_desired:

                    #create new playlist
                    playlist = Playlist(song, song.duration_ms)

                    #stores the playlist as a tuple with the empty bin space as the key, the number of songs in playlist as the next value
                    #the playlist id as the next, and the playlist as the last
                    heapq.heappush(playlist_heap,  (time_desired - song.duration_ms, 1, id(playlist), playlist))

            if temp_storage:
                #add the playlist back to the heap
                for playlist_tuples in temp_storage:
                    heapq.heappush(playlist_heap, playlist_tuples)

                #clear the list
                temp_storage.clear()

        if playlist_heap:
            self.hour = int(playlist_heap[0][3].duration / (60*60*1000))
            self.mins = int((playlist_heap[0][3].duration / (60*1000)) % 60)
            self.sec = int((playlist_heap[0][3].duration / 1000) % 60)
            self.ms = (playlist_heap[0][3].duration) % 1000

           

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

            self.length += "\n\n" + "Playlist has " + str(len(playlist_heap[0][3].songs)) + " songs!" + "\n"
  
        #else:
            #print("no playlists made")

        return playlist_heap[0][3].songs
