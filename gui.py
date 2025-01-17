from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk 
import colorsys
import numpy as np
import requests
from typing import Optional
import logging
import threading
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

import config
import auth

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Controller")
        self.setGeometry(100, 100, 800, 480)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

def create_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app, window

def start_app():
    try:
        # Handle authentication first
        if config.display == 0:
            print("Starting authentication...")
            spotify = auth.login()
            if not spotify:
                print("Authentication failed")
                return
            config.spotify_client = spotify
            print("Authentication successful")
            
        
        # Create GUI in a separate step
        app, window = create_gui()
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)



