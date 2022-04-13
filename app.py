
import json

from modules.browsing import SpotifyFront
from settings import *


def load_account_data() :
    with open(ACCOUNT_FILE, "r") as file :
        account_data = json.loads(file.read())
        file.close()
    return account_data['username'], account_data['password']


def main() :
    user, passw = load_account_data()
    sf = SpotifyFront(user, passw)
    

if __name__ == '__main__' :
    main()