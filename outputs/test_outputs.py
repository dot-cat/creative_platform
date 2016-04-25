import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from outputs import Outputs

all_outputs = Outputs()


def test_light():
    rooms = ['room 1', 'room 2', 'room 3', 'room 4', 'room 5', 'room 6']

    for room in rooms:
        all_outputs.turn_light(room, all_outputs.ON)
        print("{0:b}".format(all_outputs.get_state()))

    for room in rooms:
        all_outputs.turn_light(room, all_outputs.OFF)
        print("{0:b}".format(all_outputs.get_state()))


def test_doors():
    doors = ['First door', 'Second door', 'Third door']

    for door in doors:
        all_outputs.open_door(door)
        print("{0:b}".format(all_outputs.get_state()))

    for door in doors:
        all_outputs.close_door(door)
        print("{0:b}".format(all_outputs.get_state()))


def test_blinds():
    blinds = ['First blind', 'Second blind', 'Third blind', 'Fourth blind']

    for blind in blinds:
        all_outputs.open_blind(blind)
        print("{0:b}".format(all_outputs.get_state()))

    for blind in blinds:
        all_outputs.close_blind(blind)
        print("{0:b}".format(all_outputs.get_state()))


if __name__ == "__main__":
    test_light()
    test_doors()
    test_blinds()
