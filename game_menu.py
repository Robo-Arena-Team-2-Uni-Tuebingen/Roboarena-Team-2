import sys
from PyQt5.QtGui import QFont, QCursor, QKeyEvent, QPalette, QBrush, QImage
from PyQt5.QtCore import Qt, QRect, QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QSizePolicy

class GameMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("GameMenu")
        self.resize(1200, 1000)

        self.setupUi()

    def setupUi(self):
        font = QFont()
        font.setStrikeOut(False)
        self.setFont(font)
        self.setAutoFillBackground(True)
        self.setWindowTitle("Game Menu")      
        
        self.setup_background()
        self.setup_player_number()
        self.setup_player_label()
        self.setup_arena_number()
        self.setup_arena_label()
        self.setup_quit_button()
        self.setup_play_button()
        self.setup_settings_button()
        self.setup_logo_label()        
        
    def setup_background(self):
        self.background_label = QLabel(self)
        self.background_label.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.background_label.setStyleSheet("background-image: url('backgrounds/scifi-arena.jpg'); background-repeat: no-repeat; background-position: center;")
        self.background_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        self.background_label.setGeometry(QRect(0, 0, self.width(), self.height()))

    def setup_logo_label(self):
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
        self.logo_label.setText("Robo Arena")

    def setup_player_label(self):
        self.player_label = QLabel(self)
        self.player_label.setGeometry(QRect(320, 280, 120, 60))
        font = QFont()
        font.setPointSize(24)
        font.setStrikeOut(False)
        self.player_label.setFont(font)
        self.player_label.setObjectName("player_label")
        self.player_label.setText("Player")
        
    def setup_player_number(self):
        self.player_number = QSpinBox(self)
        self.player_number.setGeometry(QRect(440, 280, 80, 60))
        font = QFont()
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.player_number.setFont(font)
        self.player_number.setAutoFillBackground(False)
        self.player_number.setAlignment(Qt.AlignCenter)
        self.player_number.setMinimum(1)
        self.player_number.setMaximum(2)
        self.player_number.setObjectName("player_number")

    def setup_arena_label(self):
        self.arena_label = QLabel(self)
        self.arena_label.setGeometry(QRect(680, 280, 120, 60))
        font = QFont()
        font.setPointSize(24)
        font.setStrikeOut(False)
        self.arena_label.setFont(font)
        self.arena_label.setObjectName("arena_label")
        self.arena_label.setText("Arena")
        
    def setup_arena_number(self):
        self.arena_number = QSpinBox(self)
        self.arena_number.setGeometry(QRect(800, 280, 80, 61))
        font = QFont()
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.arena_number.setFont(font)
        self.arena_number.setAutoFillBackground(False)
        self.arena_number.setAlignment(Qt.AlignCenter)
        self.arena_number.setMinimum(1)
        self.arena_number.setMaximum(5)
        self.arena_number.setObjectName("arena_number")
        
    def setup_play_button(self):
        self.play_button = QPushButton(self)
        self.play_button.setGeometry(QRect(460, 430, 280, 60))
        font = QFont()
        font.setPointSize(24)
        font.setStrikeOut(False)
        self.play_button.setFont(font)
        self.play_button.setObjectName("play_button")
        self.play_button.setText("Play")
        
    def setup_settings_button(self):
        self.settings_button = QPushButton(self)
        self.settings_button.setGeometry(QRect(460, 555, 280, 60))
        font = QFont()
        font.setPointSize(24)
        font.setStrikeOut(False)
        self.settings_button.setFont(font)
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setText("Settings")
        
    def setup_quit_button(self):
        self.quit_button = QPushButton(self)
        self.quit_button.setGeometry(QRect(460, 680, 280, 60))
        font = QFont()
        font.setPointSize(24)
        font.setStrikeOut(False)
        self.quit_button.setFont(font)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.setText("Quit")
        self.quit_button.clicked.connect(QApplication.instance().quit)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = GameMenu()
    widget.show()
    sys.exit(app.exec_())