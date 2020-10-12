from SDK.MainWindow import *

class instaLock(QThread):
    instaLockAppendText = QtCore.pyqtSignal(str)
    instaLockEnd = QtCore.pyqtSignal()

    def __init__(self, roleCall, instaLock, champion, banChampion):
        QThread.__init__(self)
        self.continue_run = True
        self.roleCall = roleCall
        self.instaLock = instaLock
        self.champion = champion
        self.banChampion = banChampion

    def run(self):
        while self.continue_run:
            if self.roleCall:
                # Give some time for the role call function to work
                time.sleep(1.5)

            # which type of picking do we need to execute?
            self.executePicks()
            self.executeBans()
            
            time.sleep(3)

    def executePicks(self):
        pickReady = pyautogui.locateOnScreen(resource_path("imgs/lock_in_disabled.png"), confidence = 0.9)
        if pickReady is not None:
            if self.searchAndSelectChampion(self.champion):
                if self.instaLock:
                    while True:
                        lockIn = pyautogui.locateOnScreen(resource_path("imgs/lock_in.png"), confidence = 0.9)
                        if lockIn is not None:
                            pyautogui.moveTo(lockIn)
                            pyautogui.click()
                            self.instaLockAppendText.emit(f"Selected \"{self.champion}\" and locked...")
                            self.instaLockEnd.emit()
                            break
                else:
                    self.instaLockAppendText.emit(f"Selected \"{self.champion}\"...")
                    self.instaLockEnd.emit()

    def executeBans(self):
        banReady = pyautogui.locateOnScreen(resource_path("imgs/ban_disabled.png"), confidence = 0.9)
        if banReady is not None:
            if self.searchAndSelectChampion(self.banChampion):
                while True:
                    lockIn = pyautogui.locateOnScreen(resource_path("imgs/ban.png"), confidence = 0.9)
                    if lockIn is not None:
                        pyautogui.moveTo(lockIn)
                        pyautogui.click()
                        self.instaLockAppendText.emit(f"Selected and banned \"{self.banChampion}\"...")
                        break

    def searchAndSelectChampion(self, championName):
        succeeded = False
        # Find the search box
        championSearch = pyautogui.locateOnScreen(resource_path("imgs/search.png"), confidence = 0.9)
        if championSearch is not None:
            pyautogui.moveTo(championSearch)
            pyautogui.move(10, 0)
            # Click to serch
            pyautogui.click()
            # Enter chamption name
            pyautogui.write(championName)

            # Click on the champion to select it
            topLane = pyautogui.locateOnScreen(resource_path("imgs/top.png"), confidence = 0.9)
            if topLane is not None:
                pyautogui.moveTo(topLane)
                pyautogui.move(20, 55)
                pyautogui.click()
                time.sleep(1)
                succeeded = True
            else:
                self.instaLockAppendText.emit(f"Unable to click on searched champion for some reason")
        else:
            self.instaLockAppendText.emit(f"Unable search for \"{championName}\" for some reason")


        return succeeded


    def stop(self):
        self.continue_run = False