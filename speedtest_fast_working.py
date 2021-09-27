from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os
# os.system("Pyrcc5 tpr.qrc -o tpr.py")
import tpr
import pyspeedtest
WINDOW_SIZE = 0
progressbarvalue = 0
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi("speedtest_better_ui.ui", self)
        #Removing default title bar
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.show()
        self.progressBar.setValue(0)
        self.dial.setValue(0)
        self.closeB.clicked.connect(lambda: self.close())
        self.minimizeB.clicked.connect(lambda: self.showMinimized())
        self.changesizeB.clicked.connect(lambda: self.restore_or_maximize_window())

        self.test.clicked.connect(self.timerconf)

        ##############################################################
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        ##############################################################
        self.main_header.mouseMoveEvent = moveWindow
#----------########################----------------#
    def restore_or_maximize_window(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
        else:
            WINDOW_SIZE = 0
            self.showNormal()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
# ----------########################----------------#


    def timerconf(self):
        global dialval
        dialval = self.dial.value()
        self.dial_value.setText(str(dialval))
        self.progressBar.setMaximum(dialval)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.appProg)
        self.timer.start(0)

    def speedtest(self):
        print("in")
        st = pyspeedtest.SpeedTest("www.google.com")
        print("af 1")
        a = st.download()/1000000
        a = format(a, '.3f')
        print(a)
        self.downtext.setText(a)
        self.downtext.adjustSize()
        print("af 2")

    def appProg(self):
        global progressbarvalue
        self.progressBar.setValue(progressbarvalue)
        print("appProg")
        self.speedtest()
        if progressbarvalue > dialval:
            self.timer.stop()
            self.close()
        else:
            pass

        progressbarvalue += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())