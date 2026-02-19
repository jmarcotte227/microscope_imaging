import cv2
from glob import glob

if __name__=="__main__":
    DATASET = "img_sample_2026_02_19_14_10_21"
    IMG_DIR = f"../img_output/{DATASET}/"

    img_files = glob(f"{IMG_DIR}*")
    print(img_files)
    print(len(img_files))

    imgs = []
    for file in img_files:
        imgs.append(cv2.imread(file))

    stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)

    status, result = stitcher.stitch(imgs)

    if status == cv2.Stitcher_OK:
        cv2.imwrite(f"../results/{DATASET}_stitched_img.jpg", result)
        cv2.imshow("img", result)
        cv2.waitKey(0)
        print("Success")
