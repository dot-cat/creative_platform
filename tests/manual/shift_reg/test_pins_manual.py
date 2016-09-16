import connections.gpio_dummy as GPIO
import time

from utils.get_user_answer import get_user_answer

from connections.shift_reg_gpio import ShiftRegGPIO


def test_forward(register):
    for i in range(0, register.get_capacity()):
        register.write_data(1 << i)
        time.sleep(1)

    print('Did you seen successive light up of diodes from first to last?')  # FIXME: Check grammar here
    return get_user_answer()


def test_backward(register):
    for i in range(register.get_capacity() - 1, -1, -1):
        register.write_data(1 << i)
        time.sleep(1)

    print('Did you seen successive light up of diodes from last to first?')  # FIXME: Check grammar here
    return get_user_answer()

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    si = 37  # пин для входных данных
    rck = 33  # пин для сдвига регистров хранения
    sck = 35  # пин для синхросигнала и сдвига
    sclr = 40  # пин для очистки

    reg = ShiftRegGPIO(si, sck, rck, sclr, 2)

    test_forward(reg)
    test_backward(reg)
