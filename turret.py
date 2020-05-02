import serial

port = serial.Serial('/dev/ttyACM0', 115200)

def command_turn(value):
    port.write(b'C4-%i\n' % value)

def command_fire(value):
    port.write(b'C1-%i\n' % value)

def command_vert(value):
    value = int(value * 255)
    port.write(b'C2-%i\n' % value)

def command_horiz(value):
    value = int(value * 128) + 128
    print(b'C3-%i\n' % value)
    port.write(b'C3-%i\n' % value)
