import numpy as np
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

class Bullet():
	def __init__(self, x , y, width, height):
		self.xpos 	= xpos
		self.ypos 	= ypos
		self.width 	= width
		self.height = height
		self.speed 	= 50
		self.damage = 10
