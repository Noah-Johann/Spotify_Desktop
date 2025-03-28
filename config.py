from click import pause
from gpiozero import RotaryEncoder, Button
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
#Aktuelle Anzeige
display=0           #0=Login; 1=Playback; 

#GPIO Pins
#button = Button(27)                                                 #Vorläufiger GPIO Pin für den Button
#rotary = RotaryEncoder(a=17, b= 18, max_steps=20))      #Vorläufiger GPIO Pin für den Rotary Encoder

# Redirect URL for spotify OAuth
redirect = "http://localhost:8888/callback"


auth_web = QWebEngineView()
auth_url = None
spotify_client = None

window = None
# Logged in spotify user
user=None

current_track = None
previous_track = None
track_id = None

# Playback information
playback=None
track=None
episode=None
episode_id=None
playing_type=None

# Album artwork
album_art=None
art_label=None
# Check for album art refresh
old_track = None

# Play state of song
is_playing = False

#Playbar
progressBar = None
song_duration = 0
current_progress = 0

# Playstate
play = None
noplay = None

# Text
titel = None
artist = None
album = None
titelfont = 45

# Timer for updating playbar
timer = None
api_timer = None