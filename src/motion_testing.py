import os
import pymmcore
from imaging import infinity_cam
import cv2
import time
import datetime
from glob import glob

if __name__=="__main__":

    START_X = 3800
    START_Y = 4000

    # load stage info
    mmc = pymmcore.CMMCore()
    mmc.setDeviceAdapterSearchPaths([r'../micro_manager_config'])
    mmc.loadSystemConfiguration(r"../micro_manager_config/jack.cfg")


    input("Enter to Home")
    mmc.home("XYStage")
    mmc.setXYPosition("XYStage", START_X, START_Y)
    mmc.waitForDevice("XYStage")
    while True:
        pos_x, pos_y = mmc.getXYPosition()
        print(f"Position: {pos_x:.2f}, {pos_y:.2f}", end="\r")
