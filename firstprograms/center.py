import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()
        #calls the UI initializiation
        self.initUI()

    def initUI(self):

        #resizes the window
        self.resize(250, 150)
        #calls the center function
        self.center()
        #sets the window title to Center
        self.setWindowTitle('Center')
        #shows the window
        self.show()

    def center(self):
        #get rectangle specifying the current window
        qr = self.frameGeometry()
        #get screen resolution
        cp = QDesktopWidget().availableGeometry().center()
        #set the center of the rectangle to the center of the screen
        qr.moveCenter(cp)
        #set the top left corner of our window to the top left corner of our centered rectangle
        self.move(qr.topLeft())


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
