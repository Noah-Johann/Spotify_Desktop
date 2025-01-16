from gpiozero import RotaryEncoder, Button

#Aktuelle Anzeige
display=0           #0=Login; 1=Playback; 


#Buchstaben für die Tastatur
characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", ".", ",", "!", "?", "@", "_", " "]
selected_character = 0

#GPIO Pins
button = Button(27)                                                 #Vorläufiger GPIO Pin für den Button
rotary = RotaryEncoder(a=17, b= 18, max_steps=len(characters))      #Vorläufiger GPIO Pin für den Rotary Encoder