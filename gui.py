import colorsys
import numpy as np
import requests
from typing import Optional
import logging
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
        # Create central widget and layout
        #central_widget = QWidget()
        #self.setCentralWidget(central_widget)
        #layout = QVBoxLayout(central_widget)
        print(config.display)
        #while config.display == 1:
           # get_play_info()
        
        
                
        

def start_app():
    try:
        # Handle authentication
        print("Starting authentication...")

        #Checks for successful authentication
        spotify = auth.auth()
        print(spotify)
        
        if spotify == None:
            print("Resived authentication url, starting login website...")
            config.auth_web.setUrl(QUrl(config.auth_url))
            config.auth_web.setWindowTitle("Spotify Login")
            config.auth_web.resize(800, 480)
            config.auth_web.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            config.auth_web.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
            config.auth_web.show()

            #For Raspberry Pi
            #config.auth_web.showFullScreen()


        # Set up Spotify client
        config.spotify_client = spotify

        
        threading.Thread(target=access_play_info, daemon=True).start()
        
        # Create main window 
        config.window = create_gui()


        #get_play_info()
        
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
    try:
        user = config.spotify_client.current_user()
        print(f"Logged in as: {user['display_name']}")
            
        # Get current playback
        playback = config.spotify_client.current_playback()
        if playback:
            track = playback['item']
            print(f"Now Playing: {track['name']} by {track['artists'][0]['name']}")
            print(f"Progress: {playback['progress_ms']}/{track['duration_ms']}ms")
                
            # Get and display album art
            #album_art = get_album_art(track)
            #if album_art:
                #art_label = QLabel()
                #art_label.setPixmap(album_art.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                #art_label.move(50, 50)  # Position the artwork
                #art_label.show()
                
        else:
            print("Nothing playing")

    except Exception as e:
            print(f"Error getting info: {e}")


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
    while config.display == 1:
        get_play_info()
        sleep(1)