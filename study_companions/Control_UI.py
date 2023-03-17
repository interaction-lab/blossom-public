# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from log_session import SessionLogger
from IdleBehaviors import BlossomController
from record_thread import VideoRecorder


class Window(QMainWindow):

	def __init__(self):
		super().__init__()

		# setting title
		self.setWindowTitle("Python ")

		# setting geometry
		self.setGeometry(0, 0, 800, 480)

		# initiallize logger
		self.logger = SessionLogger()

		# initialize blossom controller
		self.bc = BlossomController()

		#initialize video recording
		self.vr = VideoRecorder()

		# calling method
		self.UiComponents()

		# showing all the widgets
		self.showFullScreen()

	# method for widgets
	def UiComponents(self):

		# variables
		# count variable
		self.count = 1500

		# start flag
		self.start = False
		self.paused = False

		# creating label to show minutes and seconds
		self.minutes_label = QLabel("25", self)
		self.colon_label = QLabel(":", self)
		self.seconds_label = QLabel("00", self)

		# setting geometry of label
		self.minutes_label.setGeometry(250, 100, 125, 100)
		self.colon_label.setGeometry(375, 90, 50, 100)
		self.seconds_label.setGeometry(405, 100, 125, 100)

		# setting font to the label
		self.minutes_label.setFont(QFont("Mono", 100))
		self.colon_label.setFont(QFont("Mono", 100))
		self.seconds_label.setFont(QFont("Mono", 100))

		# # setting alignment to the label
		self.minutes_label.setAlignment(QtCore.Qt.AlignRight)
		self.colon_label.setAlignment(QtCore.Qt.AlignCenter)
		self.seconds_label.setAlignment(QtCore.Qt.AlignLeft)
		self.minutes_label.setAlignment(QtCore.Qt.AlignTop)
		self.colon_label.setAlignment(QtCore.Qt.AlignTop)
		self.seconds_label.setAlignment(QtCore.Qt.AlignTop)

		# creating start button
		self.start_button = QPushButton("Start Session", self)

		# setting geometry to the button
		self.start_button.setGeometry(100, 375, 250, 50)

		# adding action to the button
		self.start_button.clicked.connect(self.start_action)

		# creating pause button
		self.pause_button = QPushButton("Pause Session", self)

		# setting geometry to the button
		self.pause_button.setGeometry(450, 300, 250, 50)

		# adding action to the button
		self.pause_button.clicked.connect(self.pause_action)

		# creating reset button
		self.reset_button = QPushButton("End Session Early", self)

		# setting geometry to the button
		self.reset_button.setGeometry(450, 375, 250, 50)

		# adding action to the button
		self.reset_button.clicked.connect(self.reset_action)

		# disabling pause and reset buttons at creation
		self.pause_button.setEnabled(False)
		self.reset_button.setEnabled(False)

		# creating a timer object
		timer = QTimer(self)

		# adding action to timer
		timer.timeout.connect(self.showTime)

		# update the timer every tenth second
		timer.start(1000)

	# method called by timer
	def showTime(self):

		# checking if flag is true
		if self.start:
			# incrementing the counter
			self.count -= 1
			self.bc.countdown()

			# timer is completed
			if self.count == 0:

				# making flag false
				self.start = False

				# setting text to the label
				self.label.setText("Completed !!!! ")

				# upload files
				self.bc.reset()
				self.logger.store_log()

		if self.start:
			# getting text from count
			minutes = str(int(self.count / 60))
			seconds = str(self.count % 60)
			if (self.count % 60) < 10:
				seconds = "0" + seconds

			# showing text
			self.minutes_label.setText(minutes)
			self.seconds_label.setText(seconds)

	def start_action(self):
		# making flag true
		self.start = True

		# start recording
		self.vr.start_recording()

		# disable start button
		self.start_button.setEnabled(False)

		# enable pause and reset buttons
		self.pause_button.setEnabled(True)
		self.reset_button.setEnabled(True)

		# count = 0
		if self.count == 0:
			self.start = False

		# log start event
		self.logger.log_event("start")

	def pause_action(self):
		# if paused flag is false, we are not currently paused and should start the pause
		if not self.paused:
			# making flag false
			self.start = False
			self.paused = True

			# stop recording
			self.vr.stop_recording()
			
			# change button text to resume
			self.pause_button.setText("Resume Session")
			
			# log pause event
			self.logger.log_event("pause")
		# if paused flag is true, we are already paused and should resume the session
		else:
			# reset start and paused flags
			self.start = True
			self.paused = False

			# start recording
			self.vr.start_recording()

			# change button text to resume
			self.pause_button.setText("Pause Session")

			# log resume event
			self.logger.log_event("resume")

	def reset_action(self):

		# making flag false
		self.start = False
		self.paused = False

		# set button text to pause
		self.pause_button.setText("Pause Session")

		# setting count value to 0
		self.count = 1500

		# setting label text
		self.minutes_label.setText("25")
		self.seconds_label.setText("00")

		# log start event
		self.logger.log_event("reset")
		
		# enable start button
		self.start_button.setEnabled(True)
		
		# disable pause and reset button
		self.pause_button.setEnabled(False)
		self.reset_button.setEnabled(False)

		# upload video
		self.logger.store_log()
		self.bc.disconnect()

	def moveBlossom(self):
		if self.start:
			self.bc.countdown()



# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())

