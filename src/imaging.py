#This code shows front camera (I dont know why)

import cv2

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
        ret, img = self.cam.read()

        if not ret: 
            raise ValueError("Cannot read frame")

        if display:
            cv2.imshow('Captured Image', img)
            cv2.waitKey(0)
        return img
    def stream(self):
        while (True):
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

if __name__=="__main__":
    cam = infinity_cam(0+cv2.CAP_DSHOW)
    cam.stream()
    cam.cap_image(display=True)
