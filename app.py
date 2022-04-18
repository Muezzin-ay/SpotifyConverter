
from concurrent.futures import thread
import json

from modules.browsing import PageDriver, SpotifyFront
from modules.ripping import get_url_using_name, Rip
from modules.ripping import *
from settings import *


def get_song_data() :
    sf = SpotifyFront(load_account_data())
    pl_links = sf.get_playlist_links()
    #sf.get_song_count(pl_links[0])
    playlist = sf.get_playlist(pl_links[0])
    for song in playlist :
        print(song)
    
    return playlist


def rip_songs(songs) :
    for song in songs:
        get_url = get_url_using_name(song)
        yt_search_url = get_url.create_youtube_url()
        #get_url.threading_(3,get_url.start_selenium, yt_search_url)
        youtube_url = get_url.start_selenium(yt_search_url)
        rip = Rip()
        rip.download_url_list(youtube_url,song.get_information()[0])



def main() :
    songs = get_song_data()
    rip_songs(songs)
    

def load_account_data() :
    with open(ACCOUNT_FILE, "r") as file :
        account_data = json.loads(file.read())
        file.close()
    return account_data['username'], account_data['password']
    

if __name__ == '__main__' :
    main()