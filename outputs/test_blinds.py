import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from outputs import Outputs

AllOutputs = Outputs()

blinds = ['First blind', 'Second blind', 'Third blind']

time.sleep(10)

for blind in blinds:
    AllOutputs.open_blind(blind)
    print("{0:b}".format(AllOutputs.current_state))

for blind in blinds:
    AllOutputs.close_blind(blind)
    print("{0:b}".format(AllOutputs.current_state))
