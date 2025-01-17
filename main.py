# © 2025 Noah Johann 
import threading

import gui
import auth
import config



__name__ = "__main__"

def check_login_status():
    try:
        with open('.cache') as cache_file:
            #Cache file exists = Logged in
            print("Logged in")
            config.display = 1  # Switch to playback screen
            return True
    except FileNotFoundError:
        #No File = Not logged in
        print("Not logged in")
        config.display = 0  # Switch to login screen
        return False




if __name__ == "__main__":
    
    
    check_login_status()
    gui.create_window()

    if config.display == 0:
        print("zero")
        gui.login_screen()
        auth.login()

        if config.button.is_pressed:
            auth.login()

    if config.display == 1:
        gui.playback_screen()

   # gui.startWindow()

