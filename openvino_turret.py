from openvino_detector import q, Detector
from turret import *
import time
from simple_pid import PID


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
    
command_vert(200)
command_turn(1)

pid_x = PID(0.025, 0.00, 0.0000, setpoint=0)
# pid_y = PID(0.1, 0.1, 0.05, setpoint=0)

pid_x.output_limits = (-1, 1) 
# pid_x.sample_time = 0.025


if __name__ == '__main__':
    d = Detector(daemon=True)
    d.start()
    while True:
        boxes = q.get()
        if len(boxes) == 0: 
            command_horiz(0)
            continue
        target = find_biggest(boxes)
        errors = compute_error(*target)
        output = pid_x(errors[0])
        print(target, errors, output)
        command_horiz(output)

        

