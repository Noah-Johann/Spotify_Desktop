from gpiozero import RotaryEncoder, Button
from signal import pause
import pyautogui
import time

import config


print(len(config.characters))

def buttonpress(self):
    if config.display==0:
        send_char_to_spotify(config.characters[config.selected_character])
        print("placeholder")      
                                           #Problem mit der Auswahl des Buchstabens im Webbrowser
    else:
        #pause playback 
        print("placeholder")
        
    print(config.characters[config.selected_character])

def change_character_plus():
    selected_character += 1
    if selected_character > len(config.characters):
        selected_character = len(config.characters)  
    if selected_character < 0:
        selected_character = 0
    
    print(config.characters[config.selected_character])

def change_character_minus():
    selected_character -= 1
    if selected_character >= len(config.characters):
        selected_character = len(config.characters)  
    if selected_character < 0:
        selected_character = 0

    print(config.characters[config.selected_character])

config.button.when_pressed = buttonpress
config.rotary.when_rotated(clockwise=change_character_plus(), counterclockwise=change_character_minus())

def send_char_to_spotify(selected_char):
    # Warte kurz, damit die Spotify-Seite richtig geladen ist
    time.sleep(2)
    pyautogui.write(config.characters[config.selected_character])

pause()