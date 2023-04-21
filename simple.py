import sys
from PyQt5.QtWidgets import QApplication, QWidget

# Create an instance of the QApplication
app = QApplication(sys.argv)

# Create a new window
window = QWidget()
window.setWindowTitle('My Window')
window.setGeometry(100, 100, 300, 200)  # x, y, width, height

# Show the window
window.show()

# Run the event loop
sys.exit(app.exec_())
