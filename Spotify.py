#Got much insight in making playlists with the Spotify API from https://www.youtube.com/watch?v=7J_qcttfnJA
import os
# os.system("py -m pip install requests")
import requests
import json
from Song import Song


#import webbrowser
#webbrowser.open("https://developer.spotify.com/console/post-playlists/?user_id=jvaq8vk1kgpamtbe1n1bab3uk")

#spotify_token = input("Authorization Token: ")
spotify_token = "BQC5Wa6Z8GrWvhGN9fQ_Sw5Gp4aYwEs7HPeUlmLr07TIgVYU543tHhFOrzEuHQMB6jCA8EwLMi7cOX4VeA7_n8pYMG3AtOwlGz7N5Q4a-D9G_cBNGP-smyvnJppw1lICL2bbm_EcTvwTz9XBfZfrGrWBJaL83nrtiM5D-GqbTHHJx1Sbj51amXWsBEwdT6tVREAHKaozqIzXkDiBtD_u_eT3wxfEqu0"
spotify_user_id = "jvaq8vk1kgpamtbe1n1bab3uk"


class SpotifyPlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    #search for the song on spotify
    def create_playlist(self, playlist_name):
        request_body = json.dumps({
            "name": playlist_name,
            "description": "Enjoy!",
            "public": True

        })
        
        #https://api.spotify.com/v1/users/jvaq8vk1kgpamtbe1n1bab3uk/playlists
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data = request_body.encode('utf-8'), ###
            headers = {
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.spotify_token)
            }
        )

        response_json = response.json()

        #playlist id
        return response_json["id"]


    #add song to into the new Spotify playlist
    def add_song_to_playlist(self, all_songs, playlist_name):

        #get all song uri's
        uris = []
        for song in all_songs:
            uris.append("spotify:track:" + song.id)

        #create playlist        
        playlist_id = self.create_playlist(playlist_name)

        #add songs to playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data = request_data,
            headers = {
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.spotify_token)
            }
        )

        return playlist_id
