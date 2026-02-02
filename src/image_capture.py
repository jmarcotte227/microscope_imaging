import os
from imaging import infinity_cam
import cv2
import datetime
from stage import Stage

if __name__=="__main__":
    # IMG_W = 350
    # IMG_H = 350
    IMG_W = 400
    IMG_H = 350
    START_X = 0
    START_Y = 12000
    NUM_X = 3
    NUM_Y = 3
    OUT_DIR = "../img_output/"
    DISPLAY = True

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y_%m_%d_%H_%M_%S.%f')[:-7]
    logdata_dir=f'{OUT_DIR}img_sample_{formatted_time}/'
    os.makedirs(logdata_dir)

    # load stage info
    stage=Stage(port="COM5")
    stage.mmc.setTimeoutMs(10000)

    # load camera
    cam = infinity_cam(0+cv2.CAP_DSHOW)

    input("Enter to Home")
    stage.home()
    cam.stream()
    pos_x, pos_y = stage.mmc.getXYPosition()
    #exit()
    print(f"Position: {pos_x:.2f}, {pos_y:.2f}")
    #exit()
    stage.move(START_X, START_Y)

    x, y = stage.read_position()
    print(f"At ({x:.2f}, {y:.2f})")
    cam.stream()
    exit()
    img = cam.cap_image(display=True)
    input("At start, press enter to continue")

    # moving to points
    for i in range(NUM_X):
        for j in range(NUM_Y):
            print(f"Moving to ({START_X+i*IMG_W}, {START_Y+j*IMG_H})")
            stage.move(START_X+i*IMG_W, START_Y+j*IMG_H)
            img = cam.cap_image()
            img = cam.cap_image()
            cv2.imwrite(f'{logdata_dir}img_{i}_{j}.png', img)

        print(f"Moving to ({START_X+i*IMG_W}, {START_Y})")
        stage.move(START_X+i*IMG_W, START_Y)
