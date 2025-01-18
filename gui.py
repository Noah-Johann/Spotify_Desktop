from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk 
import colorsys
import numpy as np
import requests
from typing import Optional
import logging
import threading
import sys
from PyQt6.QtCore import Qt
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
        self.setStyleSheet("background-color: black")
        # Create central widget and layout
        #central_widget = QWidget()
        #self.setCentralWidget(central_widget)
        #layout = QVBoxLayout(central_widget)



def start_app():
    try:

        
        # Handle authentication
        print("Starting authentication...")

        #Checks for successful authentication
        spotify = auth.auth()
        
            
        config.spotify_client = spotify
        print("Resived authentication url, starting login website...")
        
        # Create main window after authentication
        window = create_gui()
        
        # Start event loop
        sys.exit(qt_app.exec())
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)



def create_gui():
    window = MainWindow()
    window.show()
    return window