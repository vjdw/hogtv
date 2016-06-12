#!/usr/bin/python

import sys
import io
import time
import cv2
import numpy as np
from skimage.measure import structural_similarity as ssim
from picamera import PiCamera
from datetime import datetime

STRUCTURAL_SIMILARITY_TOLERANCE = 0.95
RESOLUTION_FOR_MOTION_DETECTION = (67,50)
RESOLUTION_FOR_PHOTO = (3280,2464)

def main():
    camera = PiCamera()
    camera.resolution = RESOLUTION_FOR_MOTION_DETECTION 
    time.sleep(2) # camera warmup time

    img1 = capture_image(camera)
    while True:
        img2 = capture_image(camera)

        similarity = ssim(img1, img2)
        print "ssim: ", str(similarity)

        if similarity < STRUCTURAL_SIMILARITY_TOLERANCE:
            camera.resolution = RESOLUTION_FOR_PHOTO
            snapshot = capture_image(camera)
            camera.resolution = RESOLUTION_FOR_MOTION_DETECTION 
            filename = datetime.now().strftime("hogcam_%Y-%m-%d_%H.%M.%S.jpg")
            cv2.imwrite(filename, snapshot)

        img1 = img2

def capture_image(camera):
    camera.start_preview()
    imageStream = io.BytesIO()
    camera.capture(imageStream, 'jpeg')
    
    imageData = np.fromstring(imageStream.getvalue(), dtype=np.uint8)
    return cv2.imdecode(imageData, cv2.CV_LOAD_IMAGE_GRAYSCALE)

if __name__ == "__main__":
    main()
