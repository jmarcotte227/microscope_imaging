import pymmcore
from pathlib import Path
import time

class Stage:
    def __init__(self, port="COM5") -> None:
        self.speed = 3000
        self.home_speed = 50
        self.mmc = pymmcore.CMMCore()
        # find file searchpath
        script_dir = Path(__file__).parent.absolute()
        self.mmc.setDeviceAdapterSearchPaths([f"{script_dir}/../micro_manager_config"])
        self.mmc.loadDevice(port, "SerialManager", port)
        self.mmc.loadDevice("LudlController", "Ludl", "LudlController")
        self.mmc.loadDevice("XYStage", "Ludl", "XYStage")
        self.mmc.setProperty(port, "AnswerTimeout", "2000.0") 
        self.mmc.setProperty(port, "BaudRate", "9600")
        self.mmc.setProperty(port, "DelayBetweenCharsMs", "11.0")
        self.mmc.setProperty(port, "StopBits", "2")


        # 2. Initialize the Controller Hub first
        self.mmc.setProperty("LudlController", "Port", port)

        # Force synchronicity for startup
        self.mmc.initializeAllDevices()
        self.busy_hold()

        self.mmc.setProperty("XYStage", "Speed", f"{self.speed}")
        print("Stage Initialized")


    def move(self, x,y, blocking=True):
        self.mmc.setXYPosition("XYStage", x, y)
        if blocking:
            self.busy_hold()

    def home(self):
        self.mmc.home("XYStage")
        self.move(500,500)
        self.mmc.setProperty("XYStage", "Speed", f"{self.home_speed}")
        self.mmc.home("XYStage")
        self.busy_hold()
        self.mmc.setOriginXY("XYStage")
        self.mmc.setProperty("XYStage", "Speed", f"{self.speed}")

    def read_position(self):
        return self.mmc.getXYPosition("XYStage")

    def busy_hold(self):
        while self.mmc.deviceBusy("XYStage"):
            time.sleep(0)

if __name__=="__main__":
    stage = Stage()
    stage.home()
    i=0
    while True:
        print(stage.read_position())

