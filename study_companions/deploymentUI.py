import argparse, sys
import tracking_file

sys.path.append("..")
print(sys.path)
from blossompy import Blossom
from time import sleep
import simpleaudio as sa
from PyQt6 import QtCore, QtGui, QtWidgets
import time



def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())
    
def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

DURATION_INT = 1500
    
  
  
class Ui_MainWindow(object):
  
  #  def __init__(self):
  #      super().__init__()

 
     
        
 #   def startTimer(self):
 #       self.time_left_int = DURATION_INT

 #       self.myTimer.timeout.connect(self.timerTimeout)
  #      self.myTimer.start(1000)

 #   def timerTimeout(self):
 #       self.time_left_int -= 1
#
 #      if self.time_left_int == 0:
 #           self.time_left_int = DURATION_INT

 #       self.update_gui()
        
 #   def update_gui(self):
 #       minsec = secs_to_minsec(self.time_left_int)
 #       self.timerLabel.setText(minsec)
        

    def setupUi(self, MainWindow):
    #    bl.connect()  # safe init and connects to blossom and puts blossom in reset position
    #    bl.load_sequences()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(689, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 240, 230, 65))
        self.pushButton.setObjectName("Start")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 240, 230, 65))
        self.pushButton_2.setObjectName("Pause")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 325, 230, 65))
        self.pushButton_3.setObjectName("End")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 325, 230, 65))
        self.pushButton_4.setObjectName("Unpause")

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.pushButton.setText(_translate("MainWindow", "Start"))
        #self.pushButton.clicked.connect(self.start_clicked)
        self.pushButton_2.setText(_translate("MainWindow", "Stop"))
        #self.pushButton_2.clicked.connect(self.stop_clicked)
        self.pushButton_3.setText(_translate("MainWindow", "Pause"))
       # self.pushButton_3.clicked.connect(self.pause_clicked)
        self.pushButton_4.setText(_translate("MainWindow", "Unpause"))
       # self.pushButton_4.clicked.connect(self.unpause_clicked)
  

    def start_clicked(self):
       start()
       if self.start_button_pressed:
            QtWidgets.QMessageBox.warning(self, "Error", "The 'Start' button has already been pressed.")
       self.start_pressed = True

    def pause_clicked(self):
        pause()
        self.pause_pressed = False

    def continue_clicked(self):
        cont()
        self.pause_pressed = False

    def end_clicked(self):
        end()
        self.start_pressed = False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    self.start_pressed = False
    self.pause_pressed = False