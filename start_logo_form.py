
import load_libs
import sys
import PyQt5


class Start_LOGO_Form(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlags(PyQt5.QtCore.Qt.WindowStaysOnTopHint | PyQt5.QtCore.Qt.FramelessWindowHint)
        self.logolabel = PyQt5.QtWidgets.QLabel(self)
        img = PyQt5.QtGui.QPixmap('logo.png')
        self.resize(img.size())
        self.logolabel.setPixmap(img)
        self.setCentralWidget(self.logolabel)

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = Start_LOGO_Form()
    form.show()
    sys.exit(app.exec_())
