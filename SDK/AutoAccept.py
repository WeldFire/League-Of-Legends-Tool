from SDK.MainWindow import *

class autoAccept(QThread):
    autoAcceptAppendText = QtCore.pyqtSignal(str)
    autoAcceptEnd = QtCore.pyqtSignal()
    def __init__(self):
        QThread.__init__(self)
        self.continue_run = True

    def run(self):
        while self.continue_run:
            autoAcceptBox = pyautogui.locateOnScreen(resource_path("imgs/accept.png"), confidence = 0.9)
            if autoAcceptBox is not None:
                _location_ = pyautogui.center(autoAcceptBox)
                pyautogui.moveTo(_location_)
                pyautogui.click()
                
                pyautogui.moveTo(_location_.x, _location_.y-50)
                self.autoAcceptAppendText.emit("Clicked accept...")
                self.autoAcceptEnd.emit()
            time.sleep(1)

    def stop(self):
        self.continue_run = False
