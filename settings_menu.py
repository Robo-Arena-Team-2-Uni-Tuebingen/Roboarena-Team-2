import sys
from configparser import ConfigParser
from PyQt5.QtGui import QFont, QCursor, QKeyEvent, QPixmap
from PyQt5.QtCore import Qt, QRect, QEvent, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QSizePolicy, QSlider

class GameMenu(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("GameMenu")
        self.resize(1200, 960)

        self.setupUi()

    def setupUi(self):
        font = QFont()
        font.setStrikeOut(False)
        self.setFont(font)
        self.setAutoFillBackground(True)
        self.setWindowTitle("Game Menu")      
        
        self.setupBackground()
        self.setupLogoLabel() 
        self.setupMusicLabel()
        self.setupMusicButton()
        self.setupVolumeLabel()
        self.setupVolumeSlider()
        
    def setupBackground(self):
        self.background_label = QLabel(self)
        self.background_label.setGeometry(QRect(0, 0, self.width(), self.height()))
        #self.background_label.setScaledContents(True)
        background_label_image = QPixmap("backgrounds/setting_gears.jpg")  # Load the image
        self.background_label.setPixmap(background_label_image)

    def resizeEvent(self, event):
        self.background_label.setGeometry(QRect(0, 0, self.width(), self.height()))
    
    def setupLogoLabel(self):
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(QRect(300, 100, 600, 80))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(60)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.logo_label.setFont(font)
        self.logo_label.setTextFormat(Qt.AutoText)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setObjectName("logo_label")
        self.logo_label.setText("Settings")
        self.logo_label.setStyleSheet("color: white")

    def setupMusicLabel(self):
        self.music_label = QLabel(self)
        self.music_label.setGeometry(QRect(350, 270, 160, 40))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.music_label.setFont(font)
        self.music_label.setTextFormat(Qt.AutoText)
        #self.music_label.setAlignment(Qt.AlignCenter)
        self.music_label.setObjectName("music_label")
        self.music_label.setText("Music")
        self.music_label.setStyleSheet("color: white")

    def setupMusicButton(self):
        self.music_button = QPushButton(self)
        self.music_button.setGeometry(QRect(740, 270, 60, 40))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.music_button.setFont(font)
        self.music_button.setObjectName("music_button")
        self.music_button.setText("On")
        self.music_button.setStyleSheet("color: #00FF00; background-color: transparent;")

    def setupVolumeLabel(self):
        self.music_label = QLabel(self)
        self.music_label.setGeometry(QRect(350, 330, 170, 40))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.music_label.setFont(font)
        self.music_label.setTextFormat(Qt.AutoText)
        #self.music_label.setAlignment(Qt.AlignCenter)
        self.music_label.setObjectName("volume_label")
        self.music_label.setText("Volume")
        self.music_label.setStyleSheet("color: white")
        
    def setupVolumeSlider(self):
        self.volume_slider = QSlider(self)
        self.volume_slider.setGeometry(QRect(630, 330, 280, 40))
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setRange(0, 100)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = GameMenu()
    widget.show()
    sys.exit(app.exec_())