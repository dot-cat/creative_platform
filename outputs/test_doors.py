import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from outputs import Outputs

AllOutputs = Outputs()

AllOutputs.turn_light('room 1', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 2', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 3', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 4', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 5', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 6', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

time.sleep(1000)
