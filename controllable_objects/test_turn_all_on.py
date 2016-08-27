#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from connections.shift_reg import ShiftRegister


# устанавливаем пины
si = 37    # пин для входных данных
rck = 33   # пин для сдвига регистров хранения
sck = 35   # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки
temp = 16

WorkRegistr = ShiftRegister(si, sck, rck, sclr)

#while 1:
WorkRegistr.write_data(0b11111111111111111111111)
#    time.sleep(1)
#WorkRegistr.write_data(0b00000000000000000000000)

time.sleep(1000000)