#!/usr/bin/python

import sys
import io
import time

import cv2
import numpy as np
from picamera import PiCamera
from datetime import datetime

def capture_image(camera):
    imageStream = io.BytesIO()
    camera.capture(imageStream, 'jpeg')
    
    # Construct a numpy array from the stream
    imageData = np.fromstring(imageStream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    return cv2.imdecode(imageData, 1)

def main():
    camera = PiCamera()
    camera.resolution = (133,100)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    img1 = capture_image(camera)
    while True:
        img2 = capture_image(camera)

        d = cv2.absdiff(img1, img2)
        s = d.sum()
        print "abs diff sum: ", s
        if s > 200:
            camera.resolution = (3280,2464)
            snapshot = capture_image(camera)
            camera.resolution = (133,100)
            filename = datetime.now().strftime("hogcam_%Y-%m-%d_%H.%M.%S.jpg")
            cv2.imwrite(filename, snapshot)

        img1 = img2

if __name__ == "__main__":
    main()
