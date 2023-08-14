from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

class Stats(QWidget):
   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(960, 0, 240, 960))
        self.setObjectName("stats")

        self.background = QLabel(self)
        self.background.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.background.setStyleSheet("background-color: rgb(165, 165, 165);")
        
        self.timer_label = QLabel(self)
        self.timer_label.setGeometry(QRect(120, 0, 120, 60))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(24)
        self.timer_label.setFont(font)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setObjectName("timer")
        self.timer_label.setText("00:00")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_counter = 0
        self.is_running = False
        self.control_timer()

        self.hp_label = QLabel(self)
        self.hp_label.setGeometry(QRect(10, 80, 50, 25))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(18)
        self.hp_label.setFont(font)
        self.hp_label.setObjectName("hp_label")
        self.hp_label.setText("HP:")

        self.points_label = QLabel(self)
        self.points_label.setGeometry(QRect(10, 125, 100, 25))
        self.points_label.setFont(font)
        self.points_label.setObjectName("points_label")
        self.points_label.setText("Points:")

        self.kills_label = QLabel(self)
        self.kills_label.setGeometry(QRect(10, 170, 90, 25))
        self.kills_label.setFont(font)
        self.kills_label.setObjectName("kills_label")
        self.kills_label.setText("Kills:")
        
        self.weapon_label = QLabel(self)
        self.weapon_label.setGeometry(QRect(10, 215, 100, 25))
        self.weapon_label.setFont(font)
        self.weapon_label.setObjectName("weapon_label")
        self.weapon_label.setText("Weapon:")
        
        self.effects_label = QLabel(self)
        self.effects_label.setGeometry(QRect(10, 260, 110, 25))
        self.effects_label.setFont(font)
        self.effects_label.setObjectName("effects_label")
        self.effects_label.setText("Effects:")

        self.hp = QLabel(self)
        self.hp.setGeometry(QRect(0, 100, 240, 25))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(18)
        self.hp.setFont(font)
        self.hp.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.hp.setObjectName("hp")
        self.hp.setText("100/100")

        self.points = QLabel(self)
        self.points.setGeometry(QRect(100, 145, 130, 25))
        self.points.setFont(font)
        self.points.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.points.setObjectName("points")
        self.points.setText("0")

        self.kills = QLabel(self)
        self.kills.setGeometry(QRect(130, 190, 100, 25))
        self.kills.setFont(font)
        self.kills.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.kills.setObjectName("kills")
        self.kills.setText("0")

        self.weapon = QLabel(self)
        self.weapon.setGeometry(QRect(50, 235, 180, 25))
        self.weapon.setFont(font)
        self.weapon.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.weapon.setObjectName("weapon")
        self.weapon.setText("Dual Pistol")
        
        self.effect_1 = QLabel(self)
        self.effect_1.setGeometry(QRect(90, 280, 140, 25))
        font = QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(18)
        self.effect_1.setFont(font)
        self.effect_1.setAccessibleName("")
        self.effect_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.effect_1.setObjectName("effect_1")

        self.effect_2 = QLabel(self)
        self.effect_2.setGeometry(QRect(90, 300, 140, 25))
        self.effect_2.setFont(font)
        self.effect_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.effect_2.setObjectName("effect_2")

        self.effect_3 = QLabel(self)
        self.effect_3.setGeometry(QRect(90, 320, 140, 25))
        self.effect_3.setFont(font)
        self.effect_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.effect_3.setObjectName("effect_3")
        
        self.effect_4 = QLabel(self)
        self.effect_4.setGeometry(QRect(90, 340, 140, 25))
        self.effect_4.setFont(font)
        self.effect_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.effect_4.setObjectName("effect_4")
        
        self.effect_5 = QLabel(self)
        self.effect_5.setGeometry(QRect(90, 360, 140, 25))
        self.effect_5.setFont(font)
        self.effect_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.effect_5.setObjectName("effect_5")

    def control_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)  # Timer will trigger every 1000 ms (1 second)
        else:
            self.is_running = False
            self.timer.stop()
        
    def update_timer(self):
        self.time_counter += 1
        minutes = self.time_counter // 60
        seconds = self.time_counter % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def update_kills(self, kills):
        self.kills.setText(kills.__str__())

    def update_points(self, points):
        self.points.setText(points.__str__())

    def update_health(self, health, max_health):
        self.hp.setText(f"{health}/{max_health}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    stats = Stats()
    stats.show()
    sys.exit(app.exec_())
