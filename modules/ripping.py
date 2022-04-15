
#from browsing import Song


import yt_dlp



class get_url_using_name():

    def __init__(self):
        name = "Dua Lipa New Rules Lyrics"
        self.name = name

    def find_by_artist_url(self):
        pass
    
        
    def create_youtube_url(self):
        url_attachment = self.name.replace(" ","+")
        prefix = "https://www.youtube.com/results?search_query="
        youtube_url = prefix+url_attachment
        print(f"youtube_url:{youtube_url}")

        self.youtube_url = youtube_url
        


class Rip():
    def download_opus(self):
        #dummy_song = Song("DummyName", "DummyInterpreter", "DummyUrl")
        print("hello world")   

    def start(self):
        self.download_opus()


g1 = get_url_using_name()
g1.create_youtube_url()
g1.find_by_artist_url()