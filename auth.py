from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import client

import config


auth_manager = SpotifyOAuth(
        client_id=client.clientID,
        client_secret=client.clientSecret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-read-playback-state user-modify-playback-state",
)

def auth():
    tokencheck = check_token()    #Checks if token is valid

    if tokencheck == None:      #Means no token or token expired
        print("Tokencheck = None, starting login...")
        login()                   #Starts new login
        return None
    # Create Spotify client
    config.spotify_client = Spotify(auth_manager=auth_manager)
    print(config.spotify_client)

    return config.spotify_client

   
    

def login():
    print("Starting def login...")
    print("Getting auth URL...")
    # Creates auth URL
    config.auth_url = auth_manager.get_authorize_url()
    
    # Setup URL change handler
    def handle_url_change(url):
        url_str = url.toString()
        # Check if redirect URL is in redirect URL
        if config.redirect in url_str and 'code=' in url_str:
            # Extract code from redirect URL
            code = url_str.split('code=')[1].split('&')[0]
            
            # Get token
            token_info = auth_manager.get_access_token(code)
            print("Access Token received")
            
            
            # Close auth window
            config.display = 1
            config.auth_web.close()
            config.spotify_client = Spotify(auth_manager=auth_manager)
            
    
    # Connect URL change signal
    config.auth_web.urlChanged.connect(handle_url_change)
    print("Auth url change connected")
    
    print(f"Auth URL: {config.auth_url}")


def check_token():
    token_info = auth_manager.cache_handler.get_cached_token()
    if token_info and not auth_manager.is_token_expired(token_info):
        print("Using cached token")
        config.display = 1
        return token_info
    else:
        print("No cached token or token expired")
        return None
