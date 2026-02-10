import cv2
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":
    X_RES = 1616  # pixels
    Y_RES = 1216  # pixels
    
    #################### MODIFY THESE ########################
    DATASET = "img_sample_2026_02_02_19_09_42"
    IMG_DIR = f"../img_output/{DATASET}/"

    NUM_X = 10
    NUM_Y = 15

    
    X_DIST = 600
    Y_DIST = 540


    X_SKEW = -50
    Y_SKEW = 20
    um_p_pix = 1/1.47 # um/pixels <<<<<< Replace this equation with imagej scale value

    ###########################################

    x_start_all = 0
    y_start_all = 0
    if X_SKEW<0:
        y_start_all = -X_SKEW*NUM_X

    if Y_SKEW<0:
        x_start_all = -Y_SKEW*NUM_Y

    x_max = (NUM_X-1)*(X_DIST/um_p_pix)+NUM_Y*Y_SKEW+X_RES+x_start_all
    y_max = (NUM_Y-1)*(Y_DIST/um_p_pix)+NUM_X*X_SKEW+Y_RES+y_start_all

    stitched_img = np.zeros((int(y_max+y_start_all), int(x_max+x_start_all)))

    x_start = 0
    y_start = 0
    for i in range(NUM_X):
        for j in range(NUM_Y):
            x_start = int(i*(X_DIST/um_p_pix)+j*Y_SKEW+x_start_all)
            y_start = int(j*(Y_DIST/um_p_pix)+i*X_SKEW+y_start_all)
            img = cv2.imread(f"{IMG_DIR}img_{i}_{j}.png", cv2.IMREAD_GRAYSCALE)
            stitched_img[y_start:y_start+Y_RES, x_start:x_start+X_RES] = img[:,:]

    cv2.imwrite(f"../results/{DATASET}_stitched_img.png", stitched_img)
    plt.imshow(np.flip(stitched_img, axis=0), 'gray')
    plt.show()

