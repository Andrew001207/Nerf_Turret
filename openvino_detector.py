import cv2 as cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video import VideoStream
from imutils.video import FPS
import time

from multiprocessing import Process
from multiprocessing import Queue

q = Queue()

class Detector(Process):
    def run(self,*args, **kwargs):
        print (args)

        net = cv2.dnn_DetectionModel('person-detection-retail-0013.xml',
                            'person-detection-retail-0013.bin')
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera)

        FPS = 0.0
        if verbose:
            print("[INFO] starting video stream...")

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            start = time.perf_counter()

            frame = frame.array
            _, confidences, boxes = net.detect(frame, confThreshold=0.6)
            rawCapture.truncate(0)

            end = time.perf_counter()

            FPS = 1 / (end - start)
            if verbose:
                print(FPS)

            q.put(boxes)