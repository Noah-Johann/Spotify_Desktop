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
import main

root=ctk.CTk()

#Window Setup
root.geometry("800x480")
root.title("Spotify Controller")



def startWindow():
    root.mainloop()
    print("window")

def login_screen():
    main.display=0

def playback_screen():
    main.display=1