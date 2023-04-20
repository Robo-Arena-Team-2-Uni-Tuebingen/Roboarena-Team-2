import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Set size and position of the window
        self.setGeometry(300, 300, 250, 150)
        # Names the window
        self.setWindowTitle('Message box')
        self.show()

    # Modify and reimplement the closeEvent handler
    def closeEvent(self, event):

        # Create an message box with following parameters:
        # The related widget, title of the message, the message itself, 
        # the combination of shown buttons (here "Yes" and "No") and the default button 
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        # Event handler for the Messagebox
        # if the "Yes" button gets clicked the window will be closed
        if reply == QMessageBox.Yes:

            event.accept()
        # if the "No" button or x mark get clicked the message box will be closed and the window remains open
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()