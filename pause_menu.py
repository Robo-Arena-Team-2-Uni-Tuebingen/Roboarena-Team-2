import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel

class PauseMenu(QWidget):
    
    def __init__(self, parent=None):
        super(PauseMenu, self).__init__(parent)
        self.widget_name = "Pause"

        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.widget_name))
        self.setLayout(layout)
        
  