import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video import VideoStream
from imutils.video import FPS
# Load the model.
print('KK')
net = cv.dnn_DetectionModel('person-detection-retail-0013.xml',
                            'person-detection-retail-0013.bin')
# Specify target device.
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

print("[INFO] starting video stream...")
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)


# Read an image.
#print('Omae')
#frame = cv.imread('1.jpeg')
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    if frame is None:
        print("NOFRMAE")
        continue
        raise Exception('Image not found!')
    # Perform an inference.
    _, confidences, boxes = net.detect(frame, confThreshold=0.5)
    print(boxes)
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
