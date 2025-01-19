from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import client
from urllib.parse import urlparse, parse_qs

import config


auth_manager = SpotifyOAuth(
        client_id=client.clientID,
        client_secret=client.clientSecret,
        redirect_uri=config.redirect,
        scope="user-read-playback-state user-modify-playback-state",
)

def auth():
    tokencheck = check_token()
    print(tokencheck)

    if tokencheck == None:
        print("Starting login...")
        login()
        return None
    # Create Spotify client
    config.spotify_client = Spotify(auth_manager=auth_manager)
    print(Spotify(auth_manager=auth_manager))
    print(config.spotify_client)
    #config.spotify_client = Spotify(auth_manager=auth_manager)

    return config.spotify_client

   
    

def login():
    print("Starting login...")
    print("Getting auth URL...")
    config.auth_url = auth_manager.get_authorize_url()
    
    # Setup URL change handler
    def handle_url_change(url):
        url_str = url.toString()
        # Check if redirect URL is in URL
        if config.redirect in url_str and 'code=' in url_str:
            # Extract code from URL
            code = url_str.split('code=')[1].split('&')[0]
            
            # Get token
            token_info = auth_manager.get_access_token(code)
            print("Access Token received")
            
            
            
            # Close auth window
            config.display = 1
            config.auth_web.close()
    
    # Connect URL change signal
    config.auth_web.urlChanged.connect(handle_url_change)
    
    print(f"Auth URL: {config.auth_url}")

    
    
    






def check_token():
    token_info = auth_manager.cache_handler.get_cached_token()
    if token_info and not auth_manager.is_token_expired(token_info):
        print("Using cached token")
        return token_info
    else:
        print("No cached token or token expired")
        return None
