# © 2025 Noah Johann 
import threading

import gui
import config
import keys


if __name__ == "__main__":
    config.display = 0
    threading.Thread(target=keys.check_Button, daemon=True).start()
    gui.start_app()
 



__name__ = "main"
