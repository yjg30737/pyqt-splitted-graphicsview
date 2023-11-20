import os, sys

from findPathWidget import FindPathWidget
from imageView import SplittedImageView

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QHBoxLayout, QWidget, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QCoreApplication, QThread
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        findPathWidget1 = FindPathWidget()
        findPathWidget1.getLineEdit().setPlaceholderText('Set Image File to Left...')
        findPathWidget1.added.connect(self.__addLeft)

        findPathWidget2 = FindPathWidget()
        findPathWidget2.getLineEdit().setPlaceholderText('Set Image File to Right...')
        findPathWidget2.added.connect(self.__addRight)

        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)

        lay = QHBoxLayout()
        lay.addWidget(findPathWidget1)
        lay.addWidget(sep)
        lay.addWidget(findPathWidget2)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__imageView = SplittedImageView(self)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(self.__imageView)

        mainWidget = QWidget(self)
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)

    def __addLeft(self, filename):
        self.__imageView.setFilenameToLeft(filename)

    def __addRight(self, filename):
        self.__imageView.setFilenameToRight(filename)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())