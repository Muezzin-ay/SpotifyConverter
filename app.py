
import json

from modules.browsing import SpotifyFront
from settings import *


def get_song_data() :
    user, passw = load_account_data()
    sf = SpotifyFront(user, passw)
    playlist_url = sf.choose_playlist()
    song_data = sf.load_songs(playlist_url)

    for song in song_data :
        print(song)


def main() :
    get_song_data()


def load_account_data() :
    with open(ACCOUNT_FILE, "r") as file :
        account_data = json.loads(file.read())
        file.close()
    return account_data['username'], account_data['password']
    

if __name__ == '__main__' :
    main()