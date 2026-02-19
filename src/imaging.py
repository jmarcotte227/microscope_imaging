import cv2
import numpy as np
import time

class infinity_cam():
    def __init__(self, device_id=0):
        try:
            self.cam = cv2.VideoCapture(device_id)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1616)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1216)
            self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception as e:
            print(e)

    def cap_image(self, display=False):
        _ = self.cam.read()
        ret, img = self.cam.read()

        if not ret: 
            raise ValueError("Cannot read frame")

        if display:
            cv2.imshow('Captured Image', img)
            cv2.waitKey(0)
            cv2.destroyWindow('Captured Image')
        return img
    def stream(self):
        while (True):
            _ = self.cam.read()
            success, frame = self.cam.read()
            if success:  # frame read successfully
                frame = cv2.flip(frame, 1)
                frame = cv2.flip(frame, 0)
                height, width = frame.shape[:2]
                center = (width // 2, height // 2)
                cv2.drawMarker(frame, center, (0, 255, 0), markerType=cv2.MARKER_CROSS,
               markerSize=50, thickness=2)
                cv2.imshow('show', frame)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break
        cv2.destroyWindow('show')

def autofocus(camera, stage, foc_inc = 250):
    # capture first couple images to determine direction
    img = camera.cap_image()
    prev_lap = compute_laplacian(img)
    stage.move_z_rel(foc_inc)

    img = camera.cap_image()
    lap = compute_laplacian(img)

    if lap > prev_lap:
        foc_dir = 1
    else:
        foc_dir = -1

    print("Focusing...")
    prev_lap = lap
    while True:
        stage.move_z_rel(foc_inc*foc_dir)
        img = camera.cap_image()
        lap = compute_laplacian(img)
        print(f"Laplace: {lap}", end='\r')

        if prev_lap > lap:
            if foc_inc <10:
                stage.move_z_rel(foc_inc*foc_dir*-1)
                break
            foc_dir = -1*foc_dir
            foc_inc /= 3
            
        prev_lap = lap
        time.sleep(0.1)
        print("Focused")

def compute_laplacian(img):
    img = cv2.GaussianBlur(img, (7, 7), 0)
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    return np.var(laplacian)


if __name__=="__main__":
    cam = infinity_cam(0+cv2.CAP_DSHOW)
    cam.stream()
    cam.cap_image(display=True)
