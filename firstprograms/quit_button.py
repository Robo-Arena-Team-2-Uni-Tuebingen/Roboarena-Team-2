import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        # Create the push button qbtn with the label "Quit" as a child of the widget "Example"
        qbtn = QPushButton('Quit', self)
        # Connect the event of click on the "Quit"-Button qbtn with the method quit of QApplication which closes the window
        qbtn.clicked.connect(QApplication.instance().quit)
        # Set the size of the Quit-Button
        qbtn.resize(qbtn.sizeHint())
        # Set the position of the Button
        qbtn.move(50, 50)

        # Set the size and position of the window
        self.setGeometry(300, 300, 350, 250)
        # Names the window
        self.setWindowTitle('Quit button')
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()