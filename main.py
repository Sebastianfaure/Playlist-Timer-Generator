#open data
import csv
#now get data from csv file
from Song import Song

class mainClass :
    def __init__(self):
        super().__init__()
        self.input_artist = set([])
        self.myMap = {}

    def setValues(self, input_artist_set, input_td_hours, input_td_min, input_td_sec):
        self.input_artist = input_artist_set
        self.time_desired_hours = input_td_hours
        self.time_desired_min = input_td_min
        self.time_desired_sec = input_td_sec
        self.first_playlist_songs = []
        self.best_playlist_songs = []

    def randomValues(self):
        
        #random_playlist_desired = False

        #random_playlist = input("Random Playlist? ")

        import random
        self.makeMap()

        #find random 
        #random_playlist_desired = True
        number_of_artists = random.randint(3, 15)
        for i in range(0, number_of_artists):
            self.input_artist.add(random.choice(list(self.myMap.keys())))
    
        self.time_desired_hours = random.randint(0, 3)

        time_to_choose = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

        self.time_desired_min = random.choice(time_to_choose)
        self.time_desired_sec = random.choice(time_to_choose)

    def makeMap(self):
    
        #create map that stores artists as keys with a list of their songs as their values 
        #myMap = {}

        #extract all data from the spotify dataset
        with open('data.csv', 'r', encoding='UTF8') as spotify_data_file:
            #skip first line
            next(spotify_data_file)

            #store the file data as lists
            #file_lines is a csv reader object
            #each line is its own list
            file_lines = csv.reader(spotify_data_file, delimiter=',')

            for line in file_lines:
                #remove unnecessary characters from the artist string, e.g, "['']"
                line[3] = line[3].replace("[", "").replace("]", "").replace("'", "")
                #make list from the number of artists per song
                artist_list = line[3].split(", ")
                #create song object
                song = Song(artist_list, int(line[5]), line[8], line[14])

                #iterate through artists and add artists to map
                for artist in artist_list:
                    if artist not in self.myMap:
                        self.myMap[artist] = [song]
                    else:
                        self.myMap[artist].append(song)

    def generate(self, first_fit, best_fit):
        self.makeMap()

        all_songs = []

        for artist in self.input_artist:
            #if artist not in self.myMap:
                #print("Sorry, we cannot find", artist)
            #else:
            print("-")
            for song in self.myMap[artist]:
                all_songs.append(song)

        #convert the minutes and seconds to milliseconds
        self.time_desired_hours = int(self.time_desired_hours)
        self.time_desired_min = int(self.time_desired_min)
        self.time_desired_sec = int(self.time_desired_sec)
        self.time_desired_sec *= 1000
        self.time_desired_min *= 60*1000
        self.time_desired_hours *= 60*60*1000
        self.time_desired_ms = self.time_desired_hours + self.time_desired_min + self.time_desired_sec

        #shuffle the selection of songs in the list for sponteneity
        import random
        random.shuffle(all_songs)

        #To time algorithms
        import time

        self.playlist_songs = []

        toPrint = ""

        if first_fit & best_fit:
            import FirstFit
            toPrint += "First-Fit Algorithm:" + "\n" + "\n"

            first_playlist = FirstFit.FirstFit()
            start = time.time()
            self.first_playlist_songs = first_playlist.First_Fit(all_songs, self.time_desired_ms)
            end = time.time()

            for x in self.first_playlist_songs:
                toPrint += x.name + "\n"

            toPrint += "\n" + first_playlist.print_length()
            toPrint += "\n" + "The First-Fit Algorithm took:" + str(end - start) + "seconds to execute" + "\n" + "\n"

            import BestFit
            toPrint += "Best-Fit Algorithm:" + "\n" + "\n"

            best_playlist = BestFit.BestFit()
            start = time.time()
            self.best_playlist_songs = best_playlist.Best_Fit(all_songs, self.time_desired_ms)
            end = time.time()

            for x in self.best_playlist_songs:
                toPrint += x.name + "\n"

            toPrint += "\n" + best_playlist.print_length()
            toPrint += "\n" + "The Best-Fit Algorithm took:" + str(end - start) + "seconds to execute" + "\n" + "\n"
        elif best_fit:
            import BestFit
            toPrint += "Best-Fit Algorithm:" + "\n" + "\n"

            best_playlist = BestFit.BestFit()
            start = time.time()
            self.best_playlist_songs = best_playlist.Best_Fit(all_songs, self.time_desired_ms)
            end = time.time()

            for x in self.best_playlist_songs:
                toPrint += x.name + "\n"

            toPrint += "\n" + best_playlist.print_length()
            toPrint += "\n" + "The Best-Fit Algorithm took:" + str(end - start) + "seconds to execute" + "\n" + "\n"
        else : # first_fit
            import FirstFit
            toPrint += "First-Fit Algorithm:" + "\n" + "\n"

            first_playlist = FirstFit.FirstFit()
            start = time.time()
            self.first_playlist_songs = first_playlist.First_Fit(all_songs, self.time_desired_ms)
            end = time.time()

            for x in self.first_playlist_songs:
                toPrint += x.name + "\n"

            toPrint += "\n" + first_playlist.print_length()
            toPrint += "\n" + "The First-Fit Algorithm took:" + str(end - start) + "seconds to execute" + "\n" + "\n"
        
        return toPrint


    def make_first_playlist(self, playlist_name):
        print("Make first playlist called")
        from spotify import SpotifyPlaylist
            
        #make spotify playlist object
        #playlist_name = input("What would you like to name your playlist? ")
        spotify_playlist = SpotifyPlaylist()
        print("spofity playlist made")
        playlist_id = spotify_playlist.add_song_to_playlist(self.first_playlist_songs, playlist_name)

        #open playlist online
        import webbrowser
        webbrowser.open('https://open.spotify.com/playlist/' + playlist_id, new=1)

        print("All Done!")

    def make_best_playlist(self, playlist_name):

        from spotify import SpotifyPlaylist
            
        #make spotify playlist object
        #playlist_name = input("What would you like to name your playlist? ")
        spotify_playlist = SpotifyPlaylist()

        playlist_id = spotify_playlist.add_song_to_playlist(self.best_playlist_songs, playlist_name)

        #open playlist online
        import webbrowser
        webbrowser.open('https://open.spotify.com/playlist/' + playlist_id, new=1)

        print("All Done!")
