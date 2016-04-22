import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from shift_reg_lib import ShiftRegister


# устанавливаем пины
si = 37    # пин для входных данных
rck = 33   # пин для сдвига регистров хранения
sck = 35   # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки
temp = 16

WorkRegistr = ShiftRegister(si, sck, rck, sclr, 2)
while 1:
    for i in range(16, 24):
        WorkRegistr.write_data(1 << i)
        time.sleep(0.5)

    for i in range(8, 16):
        WorkRegistr.write_data(1 << i)
        time.sleep(0.5)

    for i in range(0, 8):
        WorkRegistr.write_data(1 << i)
        time.sleep(0.5)

# while 1:
#     WorkRegistr.write_data(0b11111111111111111111111)
#     time.sleep(1)
#     WorkRegistr.write_data(0b00000000000000000000000)

time.sleep(100)