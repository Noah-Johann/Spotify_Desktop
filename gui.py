from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk 
from tkinter import *
from PIL import Image, ImageTk
import colorsys
from PIL import Image
import numpy as np
import requests
from typing import Optional
import logging
import threading

import config
import auth



def create_window():
    # First handle authentication
    if config.display == 0:
        print("Starting authentication...")
        auth.login()  # Run auth first in main thread
        
    # Then create GUI
    root = ctk.CTk()
    root.geometry("800x480")
    root.title("Spotify Controller")
    ctk.set_appearance_mode("#000000")

    if config.display == 0:
        login_screen()
    if config.display == 1:
        playback_screen()

    root.mainloop()  # Run GUI mainloop in main thread

def login_screen():
    #root.configure(bg="#ffffff")
    print("loginscreen")

def playback_screen():
    config.display = 1



