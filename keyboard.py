from gpiozero import RotaryEncoder, Button
from signal import pause

#Buchstaben für die Tastatur
characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", ".", ",", "!", "?", "@", "_", " "]
selected_character = 0

button = Button(27)    #Vorläufiger GPIO Pin für den Button
rotary = RotaryEncoder(a=17, b= 18, max_steps=len(characters))

print(len(characters))

def confirm_character():
    print(characters[selected_character])

def change_character():
    selected_character += 1
    if selected_character >= len(characters):
        selected_character = 0  


button.when_pressed = confirm_character
rotary.when_rotated = change_character

pause()