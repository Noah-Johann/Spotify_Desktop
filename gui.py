import colorsys
import requests
import threading
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPixmap
from time import sleep

# Set attribute before ANY QApplication creation
QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
# Defining qt app
qt_app = QApplication(sys.argv)

import config
import auth



class MainWindow(QMainWindow):
    # Setup the main window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DN40 Thing")
        self.setGeometry(100, 100, 800, 480)
        #self.setWindowIcon(Qt.WindowIcon.fromTheme("spotify"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: black")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create album art label
        config.art_label = QLabel()
        config.art_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(config.art_label)
        
# Update album art if available
def update_album_art():
    if config.album_art:
        config.art_label.setPixmap(config.album_art.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

def start_app():
    try:
        # Handle authentication
        print("Starting auth.py")

        #Checks for successful authentication
        config.spotify_client = auth.auth()
        print(config.spotify_client)
        
        # Opens login website if authentication failed
        if config.spotify_client == None:
            print("Resived authentication url, starting login website...")
            config.auth_web.setUrl(QUrl(config.auth_url))
            config.auth_web.setWindowTitle("Spotify Login")
            config.auth_web.resize(800, 480)
            config.auth_web.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            config.auth_web.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
            config.auth_web.show()
            print(config.display)

            #For Raspberry Pi
            #config.auth_web.showFullScreen()


        # Create main window 
        config.window = create_gui()
        
        # Start background thread for updates
        print("After create gui")
        threading.Thread(target=access_play_info, daemon=True).start()
        
        # Start event loop
        sys.exit(qt_app.exec())
        

        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


def create_gui():
    # Creates the play screen
    print("Creating GUI")
    config.window = MainWindow()
    config.window.show()
    return config.window


def get_play_info():
    # Get user info
    if config.display != 0:
        config.user = config.spotify_client.current_user()
        print(f"Logged in as: {config.user['display_name']}")
            
        # Get current playback
        config.playback = config.spotify_client.current_playback()
        if config.playback:
            config.track = config.playback['item']
            print(f"Now Playing: {config.track['name']} by {config.track['artists'][0]['name']}")
            print(f"Progress: {config.playback['progress_ms']}/{config.track['duration_ms']}ms")
            config.album_art = get_album_art(config.track)
            if config.initial == False:
                update_album_art()
            
        else:
            print("Nothing playing")

    #except Exception as e:
            #print(f"Error getting info: {e}")


def get_album_art(track):
    try:
        # Get album art URL (largest size)
        art_url = track['album']['images'][0]['url']
        
        # Download image
        response = requests.get(art_url)
        if response.status_code == 200:
            # Convert to QPixmap for display
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            return pixmap
    except Exception as e:
        print(f"Error getting album art: {e}")
    return None

def access_play_info():
    access = True       #Endless loop
    while access == True:
        get_play_info()
        sleep(1)