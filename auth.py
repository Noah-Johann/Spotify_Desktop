from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def login():
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    redirect_uri = "http://localhost:5000/callback"
    scope="user-read-playback-state user-modify-playback-state"

    sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-read-playback-state user-modify-playback-state"))
