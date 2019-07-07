import os, sys, logging
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append('..')
import load_libs
import PyQt5
import PyQt5.QtCore

app = PyQt5.QtWidgets.QApplication(sys.argv)


class Test_Widget(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        PyQt5.QtWidgets.QWidget.__init__(self, parent)
        self.resize(500, 500)
        self.b = PyQt5.QtWidgets.QPushButton('bt1', self)
        self.b.move(100,70)
        self.l = PyQt5.QtWidgets.QListWidget(self)
        self.l.resize(200, 200)
        self.l.move(100,100)
        self.b.clicked.connect(self.on_b_clicked_2)
        self.l.addItem('123')

    def on_b_clicked(self):
        self.l.addItem('123')

    def on_b_clicked_2(self):
        self.l.addItem('start timer')
        timer = PyQt5.QtCore.QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: print('timer.run'))
        timer.start(1000)

    def on_b_clicked_3(self):
        self.l.addItem('start timer')
        PyQt5.QtCore.QTimer.singleShot(100, lambda: print('timer.run'))

class Test_Mainwindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.resize(1000, 500)
        self.w1 = Test_Widget(self)
        self.w1.move(0,0)
        #self.w2 = Test_Widget(self)
        #self.w2.move(500,0)

form = Test_Mainwindow()
form.show()
sys.exit(app.exec_())
