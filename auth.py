from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import client
import webview


def login():
    print(login)
    auth_manager = SpotifyOAuth(
        client_id="client.clientID",
        client_secret="client.clientSecret",
        redirect_uri="http://localhost:8888/callback",
        scope="user-read-playback-state user-modify-playback-state",
    )

    auth_url = auth_manager.get_authorize_url()
    
    def on_loaded(window):
        current_url = window.get_current_url()
        if "callback?code=" in current_url:
            auth_code = current_url.split("code=")[-1].split("&")[0]
            token_info = auth_manager.get_access_token(auth_code)
            print("Access Token:", token_info["access_token"])

            sp = Spotify(auth_manager=auth_manager)
            current_user = sp.me()
            print("Angemeldeter Benutzer:", current_user["display_name"])
            
            webview.destroy_window()

    webview.create_window("Spotify Login", auth_url, 800, 480, on_top=True, frameless=True)     #fullscreen=True, for Raspberry Pi
    webview.start()
    
    #print(sp.get_me())
    #print(sp.current_user())
    #print(sp.current_playback())
    print("Login")