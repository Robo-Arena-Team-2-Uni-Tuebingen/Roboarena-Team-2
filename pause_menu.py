from PyQt5.QtGui import QFont, QCursor, QKeyEvent
from PyQt5.QtCore import Qt, QRect, QEvent, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider

class PauseMenu(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, 350, 550))
        self.setObjectName("PauseMenu")
        
        self.label = QLabel(self)
        self.label.setGeometry(QRect(115, 40, 121, 51))
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
        self.resume_button.setGeometry(QRect(75, 150, 200, 60))
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
        self.quit_button.setGeometry(QRect(75, 300, 200, 60))
        font = QFont()
        font.setPointSize(18)
        self.quit_button.setFont(font)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.setText("Quit")

        # slider to adjust the volume when in-game sounds get added
        self.horizontalSlider = QSlider(self)
        self.horizontalSlider.setGeometry(QRect(170, 480, 160, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

    # emulate pressing the ESC key
    def emulate_esc(self):

            # Create a key event
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Escape, Qt.NoModifier)

            # Send the key event to the widget
            QCoreApplication.postEvent(self, event)
