import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

from shift_reg_lib import ShiftRegister

# устанавливаем пины
si = 37    # пин для входных данных
rck = 33   # пин для сдвига регистров хранения
sck = 35   # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

WorkRegistr = ShiftRegister(si, sck, rck, sclr, 2)

while 1:
    for i in range(0, 24):
        WorkRegistr.write_data(1 << i)
        time.sleep(1)
