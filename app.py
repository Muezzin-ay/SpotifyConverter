
import json

from modules.browsing import SpotifyFront
#from modules.ripping import get_url_using_name, Rip
from settings import *


def get_song_data() :
    user, passw = load_account_data()
    sf = SpotifyFront(user, passw)
    playlist_url = sf.choose_playlist()
    songs = sf.load_songs(playlist_url)

    for song in songs :
        print(song)
    
    return songs

def rip_songs(songs) :
    pass


def main() :
    songs = get_song_data()
    rip_songs(songs)
    

def load_account_data() :
    with open(ACCOUNT_FILE, "r") as file :
        account_data = json.loads(file.read())
        file.close()
    return account_data['username'], account_data['password']
    

if __name__ == '__main__' :
    #main()

    from yt_dlp import YoutubeDL
    yt = YoutubeDL(p))
    yt.download(["https://www.youtube.com/watch?v=pcnxkUbtJcE"])