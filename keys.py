from gpiozero import RotaryEncoder, Button
from signal import pause
import pyautogui
import time

import config


print(len(config.characters))

    
def select_char():
    #send character to spotify
    send_char_to_spotify(config.characters[config.selected_character])
    print("placeholder")  
    print(config.characters[config.selected_character])


def pause_playback():
    if config.spotify_client:
        current_playback = config.spotify_client.current_playback()
        if current_playback and current_playback['is_playing']:
            config.spotify_client.pause_playback()
        else:
            config.spotify_client.start_playback()


def change_character_plus():
    #change character to next one
    selected_character += 1
    if selected_character > len(config.characters):
        selected_character = len(config.characters)  
    if selected_character < 0:
        selected_character = 0
    
    print(config.characters[config.selected_character])


def change_volume_plus():
    if config.spotify_client:
        config.spotify_client.volume() = config.spotify_client.volume() + 5


def change_character_minus():
    #change character to previous one
    selected_character -= 1
    if selected_character >= len(config.characters):
        selected_character = len(config.characters)  
    if selected_character < 0:
        selected_character = 0

    print(config.characters[config.selected_character])


def change_volume_minus():
    if config.spotify_client:
        config.spotify_client.volume() = config.spotify_client.volume() - 5 
        

def send_char_to_spotify(selected_char):
    # Warte kurz, damit die Spotify-Seite richtig geladen ist
    time.sleep(2)
    pyautogui.write(config.characters[config.selected_character])



if config.rotary.when_rotated_clockwise:
    if config.display == 0:
        change_character_plus()

    elif config.display == 1:
        print("Louder")


if config.rotary.when_rotated_counterclockwise:
    if config.display == 0:
        change_character_minus()

    elif config.display == 1:
        print("Quieter")


if config.button.when_pressed:
    if config.display == 0:
        select_char()
    
    elif config.display == 1:
        pause_playback()

pause()