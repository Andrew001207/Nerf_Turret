from multiprocessing import Process
from multiprocessing import Queue

import cv2 as cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video import VideoStream
from imutils.video import FPS
from turret import *
import time
# Load the model.
print('KK')
net = cv2.dnn_DetectionModel('person-detection-retail-0013.xml',
                            'person-detection-retail-0013.bin')
# Specify target device.
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

def check_center(x1,w):
    if x1 + w/6 < 320 < x1 + 5/6*w:
        return True
    else:
        return False

def check_dir(x1,w):
    return 320 < x1 + w/2
    
command_vert(200)
command_turn(1)

q = Queue()

class Detector(Process):
    def run(self):
        print("[INFO] starting video stream...")
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera)

        FPS = 0.0

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            start = time.perf_counter()

            frame = frame.array
            _, confidences, boxes = net.detect(frame, confThreshold=0.5)
            rawCapture.truncate(0)

            end = time.perf_counter()

            FPS = 1 / (end - start)
            print(FPS)

if __name__ == '__main__':
    d = Detector
    d.start()
    while True:
        print(q.get())

# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

#     start = time.perf_counter()

#     frame = frame.array

#     _, confidences, boxes = net.detect(frame, confThreshold=0.5)
#     print(boxes)
#     if len(boxes) > 0:
#         target = boxes[0]
#         if not check_center(target[0], target[2]):
#             dir = check_dir(target[0], target[2])
#             print("Right"if dir else "Left")
#             command_horiz(128 + (40 if dir else -40))
#         else:
#             print("Fire")
#             command_fire(100)
#     else:
#         command_horiz(128)
#     # Draw detected faces on the frame.
#     # for confidence, box in zip(list(confidences), boxes):
#     #     cv2.rectangle(frame, box, color=(0, 255, 0))

#     # cv2.putText(frame, str(round(FPS,3)), (10,25), cv2.FONT_HERSHEY_SIMPLEX,  
#     #                1, (255,255,0), 2, cv2.LINE_AA) 

#     # cv2.imshow("CAM", frame)
    
#     rawCapture.truncate(0)

#     end = time.perf_counter()

#     FPS = 1 / (end - start)
#     print(FPS)
#     # key = cv2.waitKey(1) & 0xFF
#     # if key == ord("q"):
#     #     break
# cv2.destroyAllWindows()
# # Save the frame to an image file.
# #cv2.imwrite('out.png', frame)
