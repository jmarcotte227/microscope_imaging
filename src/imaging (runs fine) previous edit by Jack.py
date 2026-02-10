import cv2

class infinity_cam():
    def __init__(self, device_id=0, flip=True):
        try:
            self.cam = cv2.VideoCapture(device_id)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1616)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1216)
            self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.flip = flip
        except Exception as e:
            print(e)

    def cap_image(self, display=False):
        ret, img = self.cam.read()
        # flip image
        if self.flip:
            img = cv2.flip(img, -1)

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
                if self.flip:
                    frame = cv2.flip(frame, -1)
                cv2.imshow('show', frame)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break


if __name__=="__main__":
    print("here")
    cam = infinity_cam(0+cv2.CAP_DSHOW)
    print("Now here")
    cam.stream()
    cam.cap_image(display=True)
