import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        #set own geometry
        self.setGeometry(300, 300, 300, 220)
        #set window title
        self.setWindowTitle('Icon')
        #set icon (didn't work on windows, unknown why)
        self.setWindowIcon(QIcon('web.png'))
        #show window
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
