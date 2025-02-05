import colorsys
import requests
import threading
import sys
from PyQt6.QtCore import Qt, QUrl, QBuffer, QByteArray, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from PyQt6.QtGui import QPixmap, QColor, QPainter, QBitmap
from time import sleep
from PIL import Image
import io

# Set attribute 
QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
# Defining qt app
qt_app = QApplication(sys.argv)

# Only import config and auth AFTER QApplication is created!!!
import config
import auth

# Define main window
class MainWindow(QMainWindow):
    # Inizialisierung des Fensters
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DN40 Thing")
        self.setGeometry(100, 100, 800, 480)
        #self.setWindowIcon(Qt.WindowIcon.fromTheme("spotify"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: black")
        
    # Create Album Artwork
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
                
        config.art_label = QLabel(central_widget)
        
        config.art_label.setFixedSize(290, 290)
        config.art_label.move(30, 90)
        
        # Create Mask for border radius
        mask = QBitmap(290, 290)
        mask.fill(Qt.GlobalColor.white)
        painter = QPainter(mask)
        painter.setBrush(Qt.GlobalColor.black)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawRoundedRect(0, 0, 290, 290, 10, 10)  # Die Hälfte der Breite/Höhe für ein rundes Bild
        painter.end()
        config.art_label.setMask(mask)

    # Create playbar
        config.progressBar = QProgressBar(self)
        config.progressBar.setFixedWidth(740)
        config.progressBar.move(30, 400)
        config.progressBar.show()

def start_app():
    try:
        # Handle authentication
        print("Starting auth.py")

        #Checks for successful authentication
        config.spotify_client = auth.auth() #opens the def auth() from auth.py
        print(config.spotify_client)
        
        # Opens login website if authentication failed
        if config.spotify_client == None:
            print("Spotify_client == None, resived authentication url, starting login website...")
            config.auth_web.setUrl(QUrl(config.auth_url))
            config.auth_web.setWindowTitle("Spotify Login")
            config.auth_web.resize(800, 480)
            config.auth_web.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            config.auth_web.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
            config.auth_web.show()
            print(config.display)

            #For Raspberry Pi
            #config.auth_web.showFullScreen()


        # Create main window 
        config.window = create_gui()
        
        # Start background thread for updates
        print("After create gui")

        # Start background thread for resiving play info
        threading.Thread(target=access_play_info, daemon=True).start()
        
        # Start event loop
        sys.exit(qt_app.exec())
        

        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


def create_gui():
    # Creates the play screen
    print("Creating GUI")
    config.window = MainWindow()
    config.window.show()
    return config.window


def get_play_info():
    if config.display != 0:     #If display is not set to 0 (Authentication)

        # Get user info
        if config.user != config.spotify_client.current_user(): #If user is not the same as the current user
            config.user = config.spotify_client.current_user()
            print(f"Logged in as: {config.user['display_name']}")
            
        # Get current playback
        config.playback = config.spotify_client.current_playback()  # Resives the current playback from spotify api

        if config.playback and config.playback['item']:  # Check if there's a track (not an ad)
            config.track = config.playback['item']
            print(f"Now Playing: {config.track['name']} by {config.track['artists'][0]['name']}")
            print(f"Progress: {config.playback['progress_ms']}/{config.track['duration_ms']}ms")

            # Set playbar variables
            config.current_progress = config.playback['progress_ms']
            config.song_duration = config.track['duration_ms']
            
            update_playbar()

            if config.old_track == None or config.track['name'] != config.old_track['name']:
                config.old_track = config.track
                config.album_art = get_album_art(config.track)
                update_album_art()
                get_color()
        else:
            print("Nothing playing or advertisement playing")

    #except Exception as e:
            #print(f"Error getting info: {e}")


def get_album_art(track):
    try:
        # Get album art URL (largest size)
        print("Getting album art")
        art_url = track['album']['images'][0]['url']
        
        # Download image
        response = requests.get(art_url)
        if response.status_code == 200:
            # Convert to QPixmap for display
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            return pixmap
    except Exception as e:
        print(f"Error getting album art: {e}")
    return None


# Update album art if available
def update_album_art():
    if config.album_art:
        config.art_label.setPixmap(config.album_art.scaled(290, 290, Qt.AspectRatioMode.KeepAspectRatio))
        


def access_play_info():
    access = True       #Endless loop
    while access == True:
        try:
            get_play_info()
            sleep(1)
        except requests.exceptions.ReadTimeout:
            print("Request timed out. Retrying in 3 seconds...")
        except Exception as e:
            print(f"Unexpected error: {e}")
    

def get_color():
    if config.album_art:
        try:
            # Convert QPixmap to bytes using QBuffer
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.OpenModeFlag.WriteOnly)
            config.album_art.save(buffer, "PNG")
            
            # Open image with PIL
            img = Image.open(io.BytesIO(byte_array.data()))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get the size of the image
            width, height = img.size
            
            # Sample pixels from the edges
            edge_pixels = []
            
            # Sample from all edges
            for x in range(0, width, 10):  # Top and bottom edges
                edge_pixels.extend([
                    img.getpixel((x, 0)),             # Top edge
                    img.getpixel((x, height - 1))     # Bottom edge
                ])
            
            for y in range(0, height, 10):  # Left and right edges
                edge_pixels.extend([
                    img.getpixel((0, y)),             # Left edge
                    img.getpixel((width - 1, y))      # Right edge
                ])
            
            # Calculate average color from edges
            avg_r = sum(pixel[0] for pixel in edge_pixels) // len(edge_pixels)
            avg_g = sum(pixel[1] for pixel in edge_pixels) // len(edge_pixels)
            avg_b = sum(pixel[2] for pixel in edge_pixels) // len(edge_pixels)
            
            # Create a darker version for better contrast
            background_color = QColor(
                int(avg_r * 0.3),  # Making it quite dark for better contrast
                int(avg_g * 0.3),
                int(avg_b * 0.3)
            )
            
            # Create gradient CSS
            gradient_style = (
                "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,"
                f"stop:0 rgb({avg_r}, {avg_g}, {avg_b}),"
                f"stop:1 rgb({background_color.red()}, {background_color.green()}, {background_color.blue()}))"
            )
            
            # Set window background
            if config.window:
                config.window.setStyleSheet(gradient_style)
            
            # Clean up
            buffer.close()
                
        except Exception as e:
            print(f"Error getting dominant color: {e}")
            # Fallback to black background
            if config.window:
                config.window.setStyleSheet("background-color: black")

def update_playbar():
    config.progressBar.setMinimum(0)
    config.progressBar.setMaximum(config.song_duration)
    config.progressBar.setValue(config.current_progress)
    config.progressBar.update()
