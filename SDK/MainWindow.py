from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QSlider
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QKeySequence, QPalette, QColor
import time, pyautogui, keyboard, os, sys, threading
import shelve


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from SDK.AutoAccept import *
from SDK.RoleCall import *
from SDK.Instalock import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.width = 300

        self.setObjectName("MainWindow")
        self.setFixedSize(self.width, 410)
        self.setWindowTitle("League Tool")
        self.setWindowIcon(QtGui.QIcon(resource_path("imgs/icon.png")))
        self.persistance = shelve.open("settings", writeback=True)
        self.SetupUI()

    def SetupUI(self):
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralWidget)

        # Client Label
        self.clientLabel = QtWidgets.QLabel(self.centralWidget)
        self.clientLabel.setGeometry(QtCore.QRect(10, 10, self.width-20, 21))
        self.clientLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.clientLabel.setObjectName("clientLabel")

        # Auto-Accept Checkbox
        self.aaCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.aaCheckBox.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.aaCheckBox.setObjectName("aaCheckBox")

        # Auto-Role Call
        self.arCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.arCheckBox.setGeometry(QtCore.QRect(10, 60, 101, 31))
        self.arCheckBox.setObjectName("arCheckBox")

        # Instalock Select
        self.instaCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.instaCheckBox.setGeometry(QtCore.QRect(self.width/2, 30, 111, 31))
        self.instaCheckBox.setObjectName("instaCheckBox")

        # Non-Instalock Select
        self.nonInstaCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.nonInstaCheckBox.setGeometry(QtCore.QRect(self.width/2, 60, 111, 31))
        self.nonInstaCheckBox.setObjectName("nonInstaCheckBox")

        # Pick-A-Role Label
        self.roleLabel = QtWidgets.QLabel(self.centralWidget)
        self.roleLabel.setGeometry(QtCore.QRect(10, 110, 47, 13))
        self.roleLabel.setObjectName("roleLabel")

        # Pick-A-Role TextBox
        self.roleTextBox = QtWidgets.QLineEdit(self.centralWidget)
        self.roleTextBox.setGeometry(QtCore.QRect(10, 130, self.width-20, 20))
        self.roleTextBox.setPlaceholderText("Text that you would like to say upon loading into a lobby")
        self.roleTextBox.setObjectName("roleTextBox")

        # Ban-A-Champion Label
        self.banChampionLabel = QtWidgets.QLabel(self.centralWidget)
        self.banChampionLabel.setGeometry(QtCore.QRect(10, 160, 200, 13))
        self.banChampionLabel.setObjectName("banChampionLabel")

        # Ban-A-Champion TextBox
        self.banChampionTextBox = QtWidgets.QLineEdit(self.centralWidget)
        self.banChampionTextBox.setGeometry(QtCore.QRect(10, 180, self.width-20, 20))
        self.banChampionTextBox.setPlaceholderText("Champion that you would like to ban")
        self.banChampionTextBox.setObjectName("banChampionTextBox")

        # Pick-A-Champion Label
        self.championLabel = QtWidgets.QLabel(self.centralWidget)
        self.championLabel.setGeometry(QtCore.QRect(10, 210, 60, 13))
        self.championLabel.setObjectName("championLabel")

        # Pick-A-Champion TextBox
        self.championTextBox = QtWidgets.QLineEdit(self.centralWidget)
        self.championTextBox.setGeometry(QtCore.QRect(10, 230, self.width-20, 20))
        self.championTextBox.setPlaceholderText("Champion that you would like to try and play")
        self.championTextBox.setObjectName("championTextBox")

        # Logging
        self.loggingBox = QtWidgets.QTextBrowser(self.centralWidget)
        self.loggingBox.setGeometry(QtCore.QRect(10, 270, self.width-20, 131))
        self.loggingBox.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.loggingBox.setObjectName("loggingBox")

        # Clear Logs Button
        self.clearLogs = QtWidgets.QPushButton(self.centralWidget)
        self.clearLogs.setGeometry(QtCore.QRect(10, 410, self.width-20, 23))
        self.clearLogs.setObjectName("clearLogs")

        # ForceStop Text
        self.forceStopText = QtWidgets.QLabel(self.centralWidget)
        self.forceStopText.setGeometry(QtCore.QRect((self.width/2)-55, 90, 111, 31))
        self.forceStopText.setAlignment(QtCore.Qt.AlignCenter)
        self.forceStopText.setObjectName("forceStopText")

        # Events
        self.arCheckBox.stateChanged.connect(self.arCheckBoxChanged)
        self.aaCheckBox.stateChanged.connect(self.aaCheckBoxChanged)
        self.instaCheckBox.stateChanged.connect(self.instaCheckBoxChanged)
        self.nonInstaCheckBox.stateChanged.connect(self.nonInstaCheckBoxChanged)
        self.roleTextBox.textChanged.connect(self.roleTextChanged)
        self.banChampionTextBox.textChanged.connect(self.banChampionTextChanged)
        self.championTextBox.textChanged.connect(self.championTextChanged)
        self.clearLogs.clicked.connect(lambda: self.loggingBox.clear())

        # Timers
        self.ignoredScheduleServiceRefreshes = 0
        self.scheduledServiceRefreshThread = "unset"

        # Keyboard events
        keyboard.on_press(self.HookKeyboard)

        # Persistence
        self.setupPersistance()

        # UI related
        self.retranslateUI()
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def closeEvent(self, event):
        self.persistance.close()

    def retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.clientLabel.setText(_translate("MainWindow", "Make sure LeagueClient is opened!"))
        self.aaCheckBox.setText(_translate("MainWindow", "Auto-Accept"))
        self.arCheckBox.setText(_translate("MainWindow", "Auto-Role Call"))
        self.instaCheckBox.setText(_translate("MainWindow", "Insta-Lock"))
        self.nonInstaCheckBox.setText(_translate("MainWindow", "Non Insta-Lock"))
        self.forceStopText.setText(_translate("MainWindow", "F1 to force stop!"))
        self.roleLabel.setText(_translate("MainWindow", "Role:"))
        self.banChampionLabel.setText(_translate("MainWindow", "Ban Champion:"))
        self.championLabel.setText(_translate("MainWindow", "Champion:"))
        self.clearLogs.setText(_translate("MainWindow", "Clear Logs"))

    def setupPersistance(self):
        if('roleTextBox' not in self.persistance):
            self.persistance['roleTextBox'] = ""
        self.roleTextBox.setText(self.persistance['roleTextBox'])

        if('banChampionTextBox' not in self.persistance):
            self.persistance['banChampionTextBox'] = ""
        self.banChampionTextBox.setText(self.persistance['banChampionTextBox'])

        if('championTextBox' not in self.persistance):
            self.persistance['championTextBox'] = ""
        self.championTextBox.setText(self.persistance['championTextBox'])

        if('aaCheckBox' not in self.persistance):
            self.persistance['aaCheckBox'] = True
        self.aaCheckBox.setChecked(self.persistance['aaCheckBox'])
        
        if('arCheckBox' not in self.persistance):
            self.persistance['arCheckBox'] = False
        self.arCheckBox.setChecked(self.persistance['arCheckBox'])
        
        if('instaCheckBox' not in self.persistance):
            self.persistance['instaCheckBox'] = False
        self.instaCheckBox.setChecked(self.persistance['instaCheckBox'])

        if('nonInstaCheckBox' not in self.persistance):
            self.persistance['nonInstaCheckBox'] = False
        self.nonInstaCheckBox.setChecked(self.persistance['nonInstaCheckBox'])
        
        self.persistance.sync()

    def arCheckBoxChanged(self, state):
        checked = state == QtCore.Qt.Checked
        if checked:
            self.roleCallThread = autoRoleCall(role=self.roleTextBox.text())
            self.roleCallThread.start()
            self.loggingBox.append(f"Role-Call thread started with string: \"{self.roleTextBox.text()}\"")
            self.roleCallThread.roleCallAppendText.connect(self.loggingBox.append)
            # For now, don't automatically disable
            # self.roleCallThread.roleCallEnd.connect(lambda: self.arCheckBox.setChecked(False))
        else:
            self.loggingBox.append("Role-Call thread stopped.")
            self.roleCallThread.stop()
            self.roleCallThread.quit()

        self.persistance['arCheckBox'] = checked
        self.persistance.sync()

    def aaCheckBoxChanged(self, state):
        checked = state == QtCore.Qt.Checked
        if checked:
            self.autoAcceptThread = autoAccept()
            self.autoAcceptThread.start()
            self.loggingBox.append("Auto-Accept thread started.")
            self.autoAcceptThread.autoAcceptAppendText.connect(self.loggingBox.append)
        else:
            self.loggingBox.append("Auto-Accept thread stopped.")
            self.autoAcceptThread.stop()
            self.autoAcceptThread.quit()

        self.persistance['aaCheckBox'] = checked
        self.persistance.sync()

    def instaCheckBoxChanged(self, state):
        checked = state == QtCore.Qt.Checked
        if checked:
            if self.nonInstaCheckBox.isChecked():
                self.nonInstaCheckBox.setChecked(False)
            
            if self.arCheckBox.isChecked():
                self.instaLockThread = instaLock(roleCall = True, instaLock = True, champion = self.championTextBox.text(), banChampion = self.banChampionTextBox.text())
            else:
                self.instaLockThread = instaLock(roleCall = False, instaLock = True, champion = self.championTextBox.text(), banChampion = self.banChampionTextBox.text())

            self.instaLockThread.start()
            self.loggingBox.append(f"Insta-Lock thread started with string: \"{self.championTextBox.text()}\"")
            self.instaLockThread.instaLockAppendText.connect(self.loggingBox.append)
            # For now, don't automatically disable
            # self.instaLockThread.instaLockEnd.connect(lambda: self.instaCheckBox.setChecked(False))
        else:
            self.loggingBox.append("Insta-Lock thread stopped.")
            self.instaLockThread.stop()
            self.instaLockThread.quit()
            
        self.persistance['instaCheckBox'] = checked
        self.persistance.sync()

    def nonInstaCheckBoxChanged(self, state):
        checked = state == QtCore.Qt.Checked
        if checked:
            if self.instaCheckBox.isChecked():
                self.instaCheckBox.setChecked(False)

            if self.arCheckBox.isChecked():
                self.nonInstaLockThread = instaLock(roleCall = True, instaLock = False, champion = self.championTextBox.text(), banChampion = self.banChampionTextBox.text())
            else:
                self.nonInstaLockThread = instaLock(roleCall = False, instaLock = False, champion = self.championTextBox.text(), banChampion = self.banChampionTextBox.text())

            self.nonInstaLockThread.start()
            self.loggingBox.append(f"Non Insta-Lock thread started with string: \"{self.championTextBox.text()}\"")
            self.nonInstaLockThread.instaLockAppendText.connect(self.loggingBox.append)
            # For now, don't automatically disable
            # self.nonInstaLockThread.instaLockEnd.connect(lambda: self.nonInstaCheckBox.setChecked(False))
        else:
            self.loggingBox.append("Non Insta-Lock thread stopped.")
            self.nonInstaLockThread.stop()
            self.nonInstaLockThread.quit()
            
        self.persistance['nonInstaCheckBox'] = checked
        self.persistance.sync()


    def roleTextChanged(self, text):            
        self.persistance['roleTextBox'] = text
        self.persistance.sync()
        self.scheduleServiceRefresh()
    
    def banChampionTextChanged(self, text):            
        self.persistance['banChampionTextBox'] = text
        self.persistance.sync()
        self.scheduleServiceRefresh()

    def championTextChanged(self, text):            
        self.persistance['championTextBox'] = text
        self.persistance.sync()
        self.scheduleServiceRefresh()
    
    def scheduleServiceRefresh(self):
        if(self.ignoredScheduleServiceRefreshes > 2):
            if(not isinstance(self.scheduledServiceRefreshThread, str)):
                self.scheduledServiceRefreshThread.stop()
            self.scheduledServiceRefreshThread = QtCore.QTimer()
            self.scheduledServiceRefreshThread.setInterval(3000)
            self.scheduledServiceRefreshThread.timeout.connect(self.restartLockServices)
            self.scheduledServiceRefreshThread.start()
        else:
            self.ignoredScheduleServiceRefreshes += 1

    def restartLockServices(self):
        if(self.arCheckBox.isChecked()):    
            self.arCheckBoxChanged(None)
            self.arCheckBoxChanged(QtCore.Qt.Checked)

        if(self.nonInstaCheckBox.isChecked()):
            self.nonInstaCheckBoxChanged(None)
            self.nonInstaCheckBoxChanged(QtCore.Qt.Checked)

        if(self.instaCheckBox.isChecked()):
            self.instaCheckBoxChanged(None)
            self.instaCheckBoxChanged(QtCore.Qt.Checked)

        self.scheduledServiceRefreshThread.stop()
        self.loggingBox.append("Service restarted to text changes")

    def HookKeyboard(self, key):
        if key.name == "f1":
            self.aaCheckBox.setCheckState(False)
            self.arCheckBox.setCheckState(False)
            self.instaCheckBox.setCheckState(False)
            self.nonInstaCheckBox.setCheckState(False)