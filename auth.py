from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import client


def login():
    client_id = client.clientID
    client_secret = client.clientSecret
    redirect_uri = "http://localhost:5000/callback"
    scope="user-read-playback-state user-modify-playback-state"

    sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-read-playback-state user-modify-playback-state"))
