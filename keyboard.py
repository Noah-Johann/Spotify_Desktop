from gpiozero import RotaryEncoder, Button
from signal import pause

button = Button(27)    #Vorläufiger GPIO Pin für den Button
rotary = RotaryEncoder(a=17, b= 18, max_steps=36)


