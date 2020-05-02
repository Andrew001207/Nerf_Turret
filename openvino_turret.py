from openvino_detector import q, Detector
from turret import *
import time

def compute_error(x,y,w,h):
    error_x = 320 - (x + w / 2)
    error_y = 240 - (y + h / 2)
    return error_x, error_y

def find_biggest(boxes):
    biggest = 0
    for i, box in enumerate(boxes):
        if box[2] * box[3] > boxes[biggest][2]*boxes[biggest][2]:
            biggest = i
    return boxes[biggest]

def check_dir(x1,w):
    return 320 < x1 + w/2
    
command_vert(200)
command_turn(1)


if __name__ == '__main__':
    d = Detector(daemon=True)
    d.start()
    while True:
        boxes = q.get()
        if len(boxes) == 0: 
            continue
        target = find_biggest(boxes)
        print(target, compute_error(*target))
        

