from click import pause
from gpiozero import RotaryEncoder, Button
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
#Aktuelle Anzeige
display=0           #0=Login; 1=Playback; 


#Buchstaben für die Tastatur
characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", ".", ",", "!", "?", "@", "_", " "]
selected_character = 0

#GPIO Pins
#button = Button(27)                                                 #Vorläufiger GPIO Pin für den Button
#rotary = RotaryEncoder(a=17, b= 18, max_steps=len(characters))      #Vorläufiger GPIO Pin für den Rotary Encoder

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

# Timer for updating playbar
timer = None
api_timer = None