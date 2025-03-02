from operator import ge
import requests
import threading
import sys
from PyQt6.QtCore import Qt, QUrl, QBuffer, QByteArray, QTimer, QMetaObject, Q_ARG, pyqtSlot, QFile
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from PyQt6.QtGui import QPixmap, QColor, QPainter, QBitmap, QPalette, QIcon
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
        
        # Set app icon
        icon_path = "assets/appicon.png"
        if QFile.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon file not found: {icon_path}")
        
        # Needed for Linux/X11 to set icon for task manager
        self.setProperty("_q_styleSheetWidgetType", "QMainWindow")
        qt_app.setWindowIcon(QIcon(icon_path))
        
        # Set frameless flag after setting icon
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

    # Create progress bar
        config.progressBar = QProgressBar(self)
        config.progressBar.setFixedWidth(740)
        config.progressBar.setFixedHeight(8) 
        config.progressBar.move(30, 400)
        config.progressBar.setTextVisible(False)
        config.progressBar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 30);
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: rgb(255, 255, 255);
                border-radius: 4px;
            }
        """)
        config.progressBar.show()

        # Initialize progress bar values
        config.progressBar.setMinimum(0)
        config.progressBar.setMaximum(100000)

        # Timer for updating playbar
        config.timer = QTimer(self)
        config.timer.timeout.connect(update_playbar)
        config.timer.start(33)  

    # Create spotify logo
        config.spotify_logo = QSvgWidget("assets/spotify_logo.svg", self)
        config.spotify_logo.setFixedSize(132, 36)
        config.spotify_logo.move(35, 30)
        config.spotify_logo.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        config.spotify_logo.setStyleSheet("background-color: transparent")

    # Create playstatus SVG
        config.play = QSvgWidget("assets/Play.svg", self)
        config.play.setFixedSize(60, 60)
        config.play.move(350, 295)
        config.play.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        config.play.setStyleSheet("background-color: transparent") 
        
        config.noplay = QSvgWidget("assets/Pause.svg", self)
        config.noplay.setFixedSize(60, 60)
        config.noplay.move(350, 295)
        config.noplay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        config.noplay.setStyleSheet("background-color: transparent")  

    # Create song info texts
        config.titel = QLabel(self)
        config.titel.setFixedSize(400, 60)
        config.titel.move(350, 160)
        config.titel.setStyleSheet("color: white; font-size: 45px; font-weight: bold; background-color: transparent")
        config.titel.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        config.artist = QLabel(self)
        config.artist.setFixedSize(400, 40)
        config.artist.move(350, 230)
        config.artist.setStyleSheet("color: white; font-size: 30px; background-color: transparent; padding-bottom: 5px;")
        config.artist.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        config.album = QLabel(self)
        config.album.setFixedSize(400, 30)
        config.album.move(350, 125)        
        config.album.setStyleSheet("color: rgba(255, 255, 255, 205); font-size: 20px; background-color: transparent")
        config.album.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


    @pyqtSlot()         # For invoking methods in the main thread
    def update_album_art(self):
        if config.album_art:
            config.art_label.setPixmap(config.album_art.scaled(290, 290, Qt.AspectRatioMode.KeepAspectRatio))
    
    @pyqtSlot()
    def get_color(self):
        if config.album_art:
            print("Getting color")
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
                self.setStyleSheet(gradient_style)
                
                # Clean up
                buffer.close()
                    
            except Exception as e:
                print(f"Error getting dominant color: {e}")
                # Fallback to black background
                self.setStyleSheet("background-color: black")

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
        print("Create GUI")
        config.window = MainWindow()
        config.window.show()
        
        print("After create gui")

        # Start background thread for resiving play info
        threading.Thread(target=access_play_info, daemon=True).start()
        
        # Start event loop
        sys.exit(qt_app.exec())
        

        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


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

            config.is_playing = config.playback['is_playing']
            print(config.is_playing)

            # Update GUI elements in the main thread
            QMetaObject.invokeMethod(config.progressBar, "setValue", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(int, config.current_progress))
            
            QMetaObject.invokeMethod(config.titel, "setText", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(str, config.track['name']))
            
            QMetaObject.invokeMethod(config.artist, "setText", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(str, config.track['artists'][0]['name']))
            
            QMetaObject.invokeMethod(config.album, "setText", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(str, config.track['album']['name']))

            if config.is_playing == False:
                QMetaObject.invokeMethod(config.play, "show", Qt.ConnectionType.QueuedConnection)
                QMetaObject.invokeMethod(config.noplay, "hide", Qt.ConnectionType.QueuedConnection)
            else:
                QMetaObject.invokeMethod(config.play, "hide", Qt.ConnectionType.QueuedConnection)
                QMetaObject.invokeMethod(config.noplay, "show", Qt.ConnectionType.QueuedConnection)
            
            if config.old_track == None or config.track['name'] != config.old_track['name']:
                config.old_track = config.track
                config.album_art = get_album_art(config.track)
                
                QMetaObject.invokeMethod(config.window, "update_album_art", 
                                       Qt.ConnectionType.QueuedConnection)
                QMetaObject.invokeMethod(config.window, "get_color", 
                                       Qt.ConnectionType.QueuedConnection)

                QMetaObject.invokeMethod(config.progressBar, "setMinimum", 
                                       Qt.ConnectionType.QueuedConnection,
                                       Q_ARG(int, 0))
                QMetaObject.invokeMethod(config.progressBar, "setMaximum", 
                                       Qt.ConnectionType.QueuedConnection,
                                       Q_ARG(int, config.song_duration))

        else:
            print("Nothing playing or advertisement playing")
            QMetaObject.invokeMethod(config.play, "show", Qt.ConnectionType.QueuedConnection)
            QMetaObject.invokeMethod(config.noplay, "hide", Qt.ConnectionType.QueuedConnection)
            QMetaObject.invokeMethod(config.progressBar, "setValue", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(int, 0))
            QMetaObject.invokeMethod(config.titel, "setText", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(str, "Nothing playing"))
            QMetaObject.invokeMethod(config.artist, "setText", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(str, "-"))
            QMetaObject.invokeMethod(config.album, "setText", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(str, "-"))
            
            config.current_progress = 0
            config.song_duration = 0
            config.album_art = QPixmap(290, 290)
            config.album_art.fill(QColor(0x18, 0x71, 0x87))
            
            QMetaObject.invokeMethod(config.window, "update_album_art", 
                                   Qt.ConnectionType.QueuedConnection)
            QMetaObject.invokeMethod(config.window, "get_color", 
                                   Qt.ConnectionType.QueuedConnection)


def get_album_art(track):
    try:
        # Get album art URL 
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
    

def update_playbar():
    if config.is_playing == True:
        ms_per_update = 33  # = timer interval
        
        # Only current progress if it's less than song duration
        config.current_progress = min(config.current_progress + ms_per_update, config.song_duration)
        config.progressBar.setValue(config.current_progress)
        config.progressBar.update() 


