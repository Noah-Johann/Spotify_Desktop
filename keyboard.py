from gpiozero import RotaryEncoder, Button
from signal import pause
import gui
import main

#Buchstaben für die Tastatur
characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", ".", ",", "!", "?", "@", "_", " "]
selected_character = 0

button = Button(27)                                                 #Vorläufiger GPIO Pin für den Button
rotary = RotaryEncoder(a=17, b= 18, max_steps=len(characters))      #Vorläufiger GPIO Pin für den Rotary Encoder

print(len(characters))

def buttonpress(self):
    if main.display==0:
        #select character
        print("placeholder")                                         #Problem mit der Auswahl des Buchstabens im Webbrowser
        #selected_character.update_letters()
    else:
        #pause playback 
        print("placeholder")
        
    print(characters[selected_character])

def change_character_plus():
    selected_character += 1
    if selected_character > len(characters):
        selected_character = len(characters)  
    if selected_character < 0:
        selected_character = 0
    
    print(characters[selected_character])

def change_character_minus():
    selected_character -= 1
    if selected_character >= len(characters):
        selected_character = len(characters)  
    if selected_character < 0:
        selected_character = 0

    print(characters[selected_character])

button.when_pressed = buttonpress
rotary.when_rotated = change_character_plus         #Weg finden um Rotierungsrichtung einzubinden



pause()