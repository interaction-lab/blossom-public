import argparse, sys

sys.path.append("..")
print(sys.path)

from blossompy import Blossom
# from main import Blossom
from time import sleep
import simpleaudio as sa
from PyQt5 import QtCore, QtGui, QtWidgets

bl = Blossom(sequence_dir='../blossompy/src/sequences', name="woody")

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        bl.connect()  # safe init and connects to blossom and puts blossom in reset position
        bl.load_sequences()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(689, 150)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 30, 481, 51))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 100, 481, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 380, 481, 51))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 445, 231, 81))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 445, 231, 81))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(110, 540, 231, 81))
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(360, 540, 231, 81))
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(110, 640, 141, 131))
        self.pushButton_8.setObjectName("pushButton_8")

        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(280, 640, 141, 131))
        self.pushButton_9.setObjectName("pushButton_9")

        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(450, 640, 141, 131))
        self.pushButton_10.setObjectName("pushButton_10")

        # buttons added after original creation

        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(110, 170, 481, 51))
        self.pushButton_11.setObjectName("pushButton_11")

        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(110, 240, 481, 51))
        self.pushButton_12.setObjectName("pushButton_12")

        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(110, 310, 481, 51))
        self.pushButton_13.setObjectName("pushButton_13")

        # end of buttons added after original creation

        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_14.setGeometry(QtCore.QRect(110, 800, 141, 131))
        self.pushButton_14.setObjectName("pushButton_14")

        self.pushButton_15 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_15.setGeometry(QtCore.QRect(280, 800, 141, 131))
        self.pushButton_15.setObjectName("pushButton_15")

        self.pushButton_16 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_16.setGeometry(QtCore.QRect(450, 800, 141, 131))
        self.pushButton_16.setObjectName("pushButton_16")

        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 22))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.pushButton.setText(_translate("MainWindow", "Reset"))
        self.pushButton.clicked.connect(self.reset_clicked)
        self.pushButton_2.setText(_translate("MainWindow", "1_Play Introduction"))
        self.pushButton_2.clicked.connect(self.intro_nameasking_clicked)
        self.pushButton_3.setText(_translate("MainWindow", "5_Personalization_BecomingFriends"))
        self.pushButton_3.clicked.connect(self.personalization_becomingfriends_clicked)
        self.pushButton_5.setText(_translate("MainWindow", "6_Personalization_answer"))
        self.pushButton_5.clicked.connect(self.personalization_becomingfriends_answer_clicked)
        self.pushButton_4.setText(_translate("Ma    inWindow", "7_Personalization_DressingBlossom"))
        self.pushButton_4.clicked.connect(self.personalization_dressingblossom_clicked)
        self.pushButton_6.setText(_translate("MainWindow", "8_DressingBlossom_Done"))
        self.pushButton_6.clicked.connect(self.personalization_dressingblossom_done_clicked)
        self.pushButton_7.setText(_translate("MainWindow", "9_Breathing_Exercise_Intro_p1"))
        self.pushButton_7.clicked.connect(self.Breathing_Exercise_Intro_p1_clicked)

        self.pushButton_8.setText(_translate("MainWindow", "10_Exercise_Intro_p2"))
        self.pushButton_8.clicked.connect(self.breathing_exercise_intro_p2_clicked)
        self.pushButton_9.setText(_translate("MainWindow", "11_Exercise_Yes"))
        self.pushButton_9.clicked.connect(self.breathing_exercise_yes_clicked)
        self.pushButton_10.setText(_translate("MainWindow", "12_Exercise_1"))
        self.pushButton_10.clicked.connect(self.breathing_exercise_1_clicked)

        # buttons added after original creation

        self.pushButton_11.setText(_translate("MainWindow", "2_intro_makefriends"))
        self.pushButton_11.clicked.connect(self.intro_makefriends_clicked)
        self.pushButton_12.setText(_translate("MainWindow", "3_Introduction_MakeFriends_Yes"))
        self.pushButton_12.clicked.connect(self.intro_makefriends_yes_clicked)
        self.pushButton_13.setText(_translate("MainWindow", "4_Introduction_MakeFriends_No"))
        self.pushButton_13.clicked.connect(self.intro_makefriends_no_clicked)

        # end of buttons added after original creation

        self.pushButton_14.setText(_translate("MainWindow", "13_Breathing_2"))
        self.pushButton_14.clicked.connect(self.breathing_exercise_2_clicked)
        self.pushButton_15.setText(_translate("MainWindow", "14_Breathing_3"))
        self.pushButton_15.clicked.connect(self.breathing_exercise_3_clicked)
        self.pushButton_16.setText(_translate("MainWindow", "15_Breathing_End"))
        self.pushButton_16.clicked.connect(self.breathing_exercise_end_clicked)

    def reset_clicked(self):
        # self.pushButton.setText("clicked")
        # add function calls here!
        # do we want to still show "clicked"?
        # play sequence "reset"
        MainWindow.close()
        bl.do_sequence("reset")

    def intro_nameasking_clicked(self):
        # self.pushButton_2.setText("clicked")
        # play "breathing - intro" (in breathing demos)
        filename = "../blossompy/media/amazon_demo/Introduction_NameAsking.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Introduction_NameAsking")


    # buttons added after original creation

    def intro_makefriends_clicked(self):
        filename = "../blossompy/media/amazon_demo/Introduction_MakeFriends.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Introduction_MakeFriends")

    def intro_makefriends_yes_clicked(self):
        filename = "../blossompy/media/amazon_demo/Introduction_MakeFriends_Yes.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Introduction_MakeFriends_Yes")

    def intro_makefriends_no_clicked(self):
        filename = "../blossompy/media/amazon_demo/Introduction_MakeFriends_No.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Introduction_MakeFriends_No")

    # end of buttons added after original creation

    def personalization_becomingfriends_clicked(self):
        filename = "../blossompy/media/amazon_demo/Personalization_BecomingFriends.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Personalization_BecomingFriends")

    def personalization_dressingblossom_clicked(self):
        filename = "../blossompy/media/amazon_demo/Personalization_DressingBlossom.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Personalization_DressingBlossom")

    def personalization_becomingfriends_answer_clicked(self):
        filename = "../blossompy/media/amazon_demo/Personalization_BecomingFriends_Answer.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Personalization_BecomingFriends_Answer")

    def personalization_dressingblossom_done_clicked(self):
        filename = "../blossompy/media/amazon_demo/Personalization_DressingBlossom_Done.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Personalization_DressingBlossom_Done")

    def Breathing_Exercise_Intro_p1_clicked(self):
        filename = "../blossompy/media/amazon_demo/Breathing_Exercise_Intro_p1.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Breathing_Exercise_Intro_p1")

    def breathing_exercise_intro_p2_clicked(self):
        filename = "../blossompy/media/amazon_demo/Breathing_Exercise_Intro_p2.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Breathing_Exercise_Intro_p2")

    def breathing_exercise_yes_clicked(self):
        filename = "../blossompy/media/amazon_demo/Breathing_Exercise_Yes.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Breathing_Exercise_Yes")

    def breathing_exercise_1_clicked(self):
        filename = "../blossompy/media/amazon_demo/Breathing_Exercise_1.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Breathing_Exercise_1")

    def breathing_exercise_2_clicked(self):
        filename = "../blossompy/media/amazon_demo/Breathing_Exercise_2.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Breathing_Exercise_2")

    def breathing_exercise_3_clicked(self):
        filename = "../blossompy/media/amazon_demo/Breathing_Exercise_3.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Breathing_Exercise_3")

    def breathing_exercise_end_clicked(self):
        filename = "../blossompy/media/amazon_demo/Breathing_Exercise_End.wav"
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        bl.do_sequence("amazon_demo/Breathing_Exercise_End")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
<<<<<<< HEAD
    MainWindow.showFullScreen()
    # MainWindow.show()
=======
    # MainWindow.show()
    MainWindow.showFullScreen()
>>>>>>> 61637cc242380acf8c60769492be6996c13786a3
    sys.exit(app.exec_())
