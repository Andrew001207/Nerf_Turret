from openvino_detector import q, Detector
from turret import *
import time

def check_center(x1,w):
    if x1 + w/6 < 320 < x1 + 5/6*w:
        return True
    else:
        return False

def check_dir(x1,w):
    return 320 < x1 + w/2
    
command_vert(200)
command_turn(1)


if __name__ == '__main__':
    d = Detector(daemon=True)
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
