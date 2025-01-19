from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk 
import colorsys
import numpy as np
import requests
from typing import Optional
import logging
import threading
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

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
            else:
                print("Nothing playing")
                
        except Exception as e:
            print(f"Error getting info: {e}")

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


        config.spotify_client = spotify

        

        #For Raspberry Pi
        #config.auth_web.showFullScreen()

        # Create main window after authentication
        config.window = create_gui()
        
        # Start event loop
        sys.exit(qt_app.exec())
        

        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)



def create_gui():
    config.window = MainWindow()
    config.window.show()
    return config.window