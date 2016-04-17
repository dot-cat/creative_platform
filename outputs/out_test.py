import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from outputs import Outputs

AllOutputs = Outputs()

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.open_door('Open first door')

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.open_door('Close first door')

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.open_door('Open second door')

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.open_door('Close second door')

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.open_door('Open first door')

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.open_door('Close first door')

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 1', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 2', AllOutputs.OFF)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 1', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 2', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 3', AllOutputs.ON)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 3', AllOutputs.OFF)

print("{0:b}".format(AllOutputs.current_state))

AllOutputs.turn_light('room 1', AllOutputs.OFF)

print("{0:b}".format(AllOutputs.current_state))
