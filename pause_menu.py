from PyQt5.QtGui import QFont, QCursor, QKeyEvent, QPixmap
from PyQt5.QtCore import Qt, QRect, QEvent, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider

class PauseMenu(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(960, 0, 240, 550))
        self.setObjectName("PauseMenu")
        
        self.label = QLabel(self)
        self.label.setGeometry(QRect(60, 40, 121, 51))
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Pause")

        # button to resume the game, like pressing ESC
        self.resume_button = QPushButton(self)
        self.resume_button.setGeometry(QRect(20, 150, 200, 60))
        font = QFont()
        font.setPointSize(18)
        self.resume_button.setFont(font)
        self.resume_button.setCursor(QCursor(Qt.ArrowCursor))
        self.resume_button.setObjectName("resume_button")
        self.resume_button.setText("Resume")
        self.resume_button.clicked.connect(self.emulate_esc)

        # quit_button to quit the game
        # now quits the whole window, later return to the main menu 
        self.quit_button = QPushButton(self)
        self.quit_button.setGeometry(QRect(20, 300, 200, 60))
        font = QFont()
        font.setPointSize(18)
        self.quit_button.setFont(font)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.setText("Quit")

        # icon for volume
        self.volume_icon = QLabel(self)
        self.volume_icon.setGeometry(QRect(65, 471, 40, 40))
        self.volume_icon.setScaledContents(True)
        volume_icon_image = QPixmap("backgrounds/volume-icon.png")  # Load the image
        self.volume_icon.setPixmap(volume_icon_image)

        # slider to adjust the volume when in-game sounds get added
        self.volume_slider = QSlider(self)
        self.volume_slider.setGeometry(QRect(115, 480, 160, 22))
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setRange(0, 100)

    # emulate pressing the ESC key
    def emulate_esc(self):

            # Create a key event
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Escape, Qt.NoModifier)

            # Send the key event to the widget
            QCoreApplication.postEvent(self, event)
