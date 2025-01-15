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
        self.letter_selector.current_idx = (self.letter_selector.current_idx + 1) % len(self.letter_selector.letters)
        selected_character.update_letters()
    else:
        #pause playback 
        print("placeholder")
        
    print(characters[selected_character])

def change_character_plus():
    selected_character += 1
    if selected_character >= len(characters):
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


"""

def on_rotate_clockwise(self):
        if self.is_login_screen:
            self.letter_selector.current_idx = (self.letter_selector.current_idx + 1) % len(self.letter_selector.letters)
            self.letter_selector.update_letters()
        else:
            try:
                current = self.sp.current_playback()
                if current and current.get('device'):
                    current_volume = current['device'].get('volume_percent', 0)
                    self.sp.volume(min(100, current_volume + 5))
            except Exception as e:
                self.logger.error(f"Error adjusting volume: {e}")
    
def on_rotate_counterclockwise(self):
    if self.is_login_screen:
        self.letter_selector.current_idx = (self.letter_selector.current_idx - 1) % len(self.letter_selector.letters)
        self.letter_selector.update_letters()
    else:
        current_volume = self.sp.current_playback()['device']['volume_percent']
        self.sp.volume(max(0, current_volume - 5))
    
def buttonpress(self):
    if self.is_login_screen:
        self.password_display.insert("end", self.letter_selector.letters[self.letter_selector.current_idx])
    else:
        if self.sp.current_playback()['is_playing']:
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

"""



pause()