from gpiozero import RotaryEncoder, Button
from signal import pause

import config
import gui


def pause_playback():
    if config.spotify_client:
        current_playback = config.spotify_client.current_playback()
        if current_playback and current_playback['is_playing']:
            config.spotify_client.pause_playback()
        else:
            config.spotify_client.start_playback()

def change_volume_plus():
    if config.spotify_client:
        config.spotify_client.volume() == config.spotify_client.volume() + 5

def change_volume_minus():
    if config.spotify_client:
        config.spotify_client.volume() == config.spotify_client.volume() - 5 

def check_Button():
    if config.rotary.when_rotated_clockwise:
        change_volume_plus()
        print("Louder")
        gui.get_play_info()


    if config.rotary.when_rotated_counterclockwise:
        change_volume_minus()
        print("Quieter")
        gui.get_play_info()


    if config.button.when_pressed:
        pause_playback()
        pause_playback()
        gui.get_play_info()
            

