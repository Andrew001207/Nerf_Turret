import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video import VideoStream
from imutils.video import FPS
from turret import *
# Load the model.
print('KK')
net = cv.dnn_DetectionModel('person-detection-retail-0013.xml',
                            'person-detection-retail-0013.bin')
# Specify target device.
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

def check_center(x1,w):
    if x1 + w/6 < 320 < x1 + 5/6*w:
        return True
    else:
        return False

def check_dir(x1,w):
    return 320 < x1 + w/2
    
command_vert(200)
command_turn(1)
print("[INFO] starting video stream...")
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    if frame is None:
        print("NOFRMAE")
        continue
        raise Exception('Image not found!')
    # Perform an inference.
    _, confidences, boxes = net.detect(frame, confThreshold=0.5)
    print(boxes)
    if len(boxes) > 0:
        target = boxes[0]
        if not check_center(target[0], target[2]):
            dir = check_dir(target[0], target[2])
            print("Right"if dir else "Left")
            command_horiz(128 + (40 if dir else -40))
        else:
            print("Fire")
            command_fire(100)
    else:
        command_horiz(128)
    # Draw detected faces on the frame.
    for confidence, box in zip(list(confidences), boxes):
        cv.rectangle(frame, box, color=(0, 255, 0))
    cv.imshow("CAM", frame)
    key = cv.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
cv.destroyAllWindows()
# Save the frame to an image file.
#cv.imwrite('out.png', frame)
