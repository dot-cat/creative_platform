import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from outputs import Outputs

AllOutputs = Outputs()

rooms = ['room 1', 'room 2', 'room 3', 'room 4', 'room 5', 'room 6']

for room in rooms:
    AllOutputs.turn_light(room, AllOutputs.ON)
    print("{0:b}".format(AllOutputs.current_state))

for room in rooms:
    AllOutputs.turn_light(room, AllOutputs.OFF)
    print("{0:b}".format(AllOutputs.current_state))
