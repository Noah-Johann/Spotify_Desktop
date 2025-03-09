from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import client

import config


auth_manager = SpotifyOAuth(
        client_id=client.clientID,
        client_secret=client.clientSecret,
        redirect_uri=config.redirect,
        scope="user-read-playback-state user-modify-playback-state user-read-playback-position user-library-read user-read-currently-playing user-read-recently-played",
)

def auth():
    tokencheck = check_token()    #Checks if token is valid

    if tokencheck == None:      #Means no token or token expired
        print("Tokencheck = None, starting login...")
        login()                   #Starts new login
        return None
    
    # Create Spotify client if it doesn't exist
    if config.spotify_client is None:
        config.spotify_client = Spotify(auth_manager=auth_manager)
        print("Created new Spotify client in auth function")
    
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
        # Try to refresh the token and check if it was successful
        if refresh_token():
            print("Token refreshed successfully in check_token")
            # Get the refreshed token info
            refreshed_token_info = auth_manager.cache_handler.get_cached_token()
            return refreshed_token_info
        else:
            print("Failed to refresh token in check_token")
            return None
    
def refresh_token():
    """
    Attempts to refresh the authentication token if one exists.
    Returns True if token was successfully refreshed, False otherwise.
    """
    try:
        token_info = auth_manager.cache_handler.get_cached_token()
        if token_info and auth_manager.is_token_expired(token_info):
            print("Token expired, attempting to refresh...")
            try:
                # The refresh_access_token method will update the cache automatically
                new_token = auth_manager.refresh_access_token(token_info['refresh_token'])
                print("Token refreshed successfully")
                
                # Update the Spotify client with the new token
                config.spotify_client = Spotify(auth_manager=auth_manager)
                config.display = 1
                return True
            except Exception as e:
                print(f"Error during token refresh: {e}")
                config.spotify_client = None
                return False
        elif token_info and not auth_manager.is_token_expired(token_info):
            print("Token is still valid, no refresh needed")
            # Ensure spotify_client is set even if token is valid
            if config.spotify_client is None:
                config.spotify_client = Spotify(auth_manager=auth_manager)
            config.display = 1
            return True
        else:
            print("No token available to refresh")
            config.spotify_client = None
            return False
    except Exception as e:
        print(f"Error refreshing token: {e}")
        config.spotify_client = None
        return False

