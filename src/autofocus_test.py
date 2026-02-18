import cv2
import numpy as np
from imaging import infinity_cam, autofocus
from stage import Stage

if __name__=="__main__":
    cam = infinity_cam(device_id=1)
    cam.stream()

    stage = Stage("COM7")
    autofocus(cam, stage)

    print("Complete!")
    cam.cap_image(display=True)
