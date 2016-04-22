import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from outputs import Outputs

AllOutputs = Outputs()

doors = ['First door', 'Second door', 'Third door']

#time.sleep(10)

for door in doors:
    AllOutputs.open_door(door)
    print("{0:b}".format(AllOutputs.current_state))

for door in doors:
    AllOutputs.close_door(door)
    print("{0:b}".format(AllOutputs.current_state))
