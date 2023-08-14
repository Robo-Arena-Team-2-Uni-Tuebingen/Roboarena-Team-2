import sys
from PyQt5.QtGui import QFont, QCursor, QKeyEvent
from PyQt5.QtCore import Qt, QRect, QEvent, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QSizePolicy

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
        
        self.background_label = QLabel(self)
        self.background_label.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.background_label.setStyleSheet("background-image: url('backgrounds/scifi-arena.jpg'); background-repeat: no-repeat; background-position: center;")
        self.background_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(QRect(300, 100, 600, 80))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.logo_label.setFont(font)
        self.logo_label.setTextFormat(Qt.AutoText)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setObjectName("logo_label")
        self.logo_label.setText("RoboArena")
        self.logo_label.setStyleSheet("color: #ea1603")

        self.player_label = QLabel(self)
        self.player_label.setGeometry(QRect(300, 280, 130, 60))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(28)
        font.setWeight(50)
        self.player_label.setFont(font)
        self.player_label.setStyleSheet("color: #ea1603")
        self.player_label.setObjectName("player_label")
        self.player_label.setText("Player")
        
        self.player_number = QSpinBox(self)
        self.player_number.setGeometry(QRect(440, 280, 80, 60))
        self.player_number.setFont(font)
        self.player_number.setStyleSheet("background-color: #9e9c89;\n"
									       "color: #ea1603;")
        self.player_number.setAlignment(Qt.AlignCenter)
        self.player_number.setMinimum(1)
        self.player_number.setMaximum(2)
        self.player_number.setObjectName("player_number")

        self.arena_label = QLabel(self)
        self.arena_label.setGeometry(QRect(770, 280, 120, 60))
        self.arena_label.setFont(font)
        self.arena_label.setStyleSheet("color: #ea1603")
        self.arena_label.setObjectName("arena_label")
        self.arena_label.setText("Arena")
        
        self.arena_number = QSpinBox(self)
        self.arena_number.setGeometry(QRect(680, 280, 80, 61))
        self.arena_number.setFont(font)
        self.arena_number.setStyleSheet("background-color: #9e9c89;\n"
									       "color: #ea1603;")
        self.arena_number.setAlignment(Qt.AlignCenter)
        self.arena_number.setMinimum(1)
        self.arena_number.setMaximum(5)
        self.arena_number.setObjectName("arena_number")
        
        self.play_button = QPushButton(self)
        self.play_button.setGeometry(QRect(460, 430, 280, 60))
        font = QFont()
        font.setPointSize(24)
        font.setStrikeOut(False)
        self.play_button.setFont(font)
        self.play_button.setStyleSheet("background-color: #9e9c89;\n"
									   "color: #ea1603;")
        self.play_button.setObjectName("play_button")
        self.play_button.setText("Play")
        
        self.settings_button = QPushButton(self)
        self.settings_button.setGeometry(QRect(460, 555, 280, 60))
        self.settings_button.setFont(font)
        self.settings_button.setStyleSheet("background-color: #9e9c89;\n"
									       "color: #ea1603;")
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setText("Settings")
        
        self.quit_button = QPushButton(self)
        self.quit_button.setGeometry(QRect(460, 680, 280, 60))
        self.quit_button.setFont(font)
        self.quit_button.setStyleSheet("background-color: #9e9c89;\n"
									   "color: #ea1603;")
        self.quit_button.setObjectName("quit_button")
        self.quit_button.setText("Quit")
        self.quit_button.clicked.connect(QApplication.instance().quit)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = GameMenu()
    widget.show()
    sys.exit(app.exec_())