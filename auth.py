from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import client
from flask import Flask, request
from urllib.parse import urlparse, parse_qs
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import sys

import config


auth_manager = SpotifyOAuth(
        client_id=client.clientID,
        client_secret=client.clientSecret,
        redirect_uri=config.redirect,
        scope="user-read-playback-state user-modify-playback-state",
)

def auth():
    token = check_token()

    if token == None:
        print("Starting login...")
        login()

    return config.spotify_client

   
    

def login():
    print("Starting login...")
    print("Getting auth URL...")
    config.auth_url = auth_manager.get_authorize_url()
    config.spotify_client = Spotify(auth_manager=auth_manager)

    print(f"Auth URL: {config.auth_url}")

    
    
    






def check_token():
    token_info = auth_manager.cache_handler.get_cached_token()
    if token_info and not auth_manager.is_token_expired(token_info):
        print("Using cached token")
        return Spotify(auth_manager=auth_manager)
    else:
        print("No cached token or token expired")
        return None
