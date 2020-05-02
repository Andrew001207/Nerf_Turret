from inputs import devices
from inputs import get_gamepad
import serial

port = serial.Serial('/dev/ttyACM0', 115200)

def command_turn(value):
    port.write(b'C4-%i\n' % value)

def command_fire(value):
    port.write(b'C1-%i\n' % value)

def command_vert(value):
    port.write(b'C2-%i\n' % value)

def command_horiz(value):
    print(b'C3-%i\n' % value)
    port.write(b'C3-%i\n' % value)

while 1:
    events = get_gamepad()
    for event in events:
        if event.code == 'ABS_RZ':
            command_turn(event.state)
        if event.code == 'BTN_SOUTH' and event.state == 1:
            command_fire(event.state) 
        if event.code == 'ABS_Y':
            command_vert(event.state / 256 + 128)
        if event.code == 'ABS_X':
            command_horiz(event.state / 256 + 128)  
        print(event.ev_type, event.code, event.state)