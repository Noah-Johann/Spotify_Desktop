from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import client
import webview
from flask import Flask, request
from urllib.parse import urlparse, parse_qs
import threading


def login():
    print(login)
    #Setup
    auth_manager = SpotifyOAuth(
        client_id=client.clientID,
        client_secret=client.clientSecret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-read-playback-state user-modify-playback-state",
    )
    
    # Check for cached token first
    token_info = auth_manager.cache_handler.get_cached_token()
    if token_info and not auth_manager.is_token_expired(token_info):
        print("Using cached token")
        return Spotify(auth_manager=auth_manager)

    #Starting if no token is found
    spotify_client = None
    window = None
    app = Flask(__name__)
    
    #HTTP Server
    @app.route('/callback')
    def callback():
        nonlocal spotify_client, window
        try:
            code = request.args.get('code')
            if code:
                token_info = auth_manager.get_access_token(code)
                print("Access Token:", token_info['access_token'])
                print("Login successful")
                
                # Create Spotify client
                spotify_client = Spotify(auth_manager=auth_manager)
                if window:
                    window.destroy()
                return 'Login successful! You can close this window.'
            return 'No code received', 400
        except Exception as e:
            print(f"Callback error: {e}")
            return f'Error: {str(e)}', 500

    # Only start webview if we need new token
    auth_url = auth_manager.get_authorize_url()
    print(f"Opening auth URL: {auth_url}")
    
    

    print(auth_url)

    #Starts Webserver
    threading.Thread(target=lambda: app.run(port=8888, debug=False), daemon=True).start()
    
    # Open login window
    window = webview.create_window("Spotify Login", auth_url, fullscreen=True, on_top=True, frameless=True)
    webview.start()

    
    #print(sp.get_me())
    #print(sp.current_user())
    #print(sp.current_playback())
    print("Login")

    return spotify_client  # Return the Spotify client for use elsewhere

    print(sp.get.me())