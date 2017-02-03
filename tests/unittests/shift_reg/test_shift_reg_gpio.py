import unittest

from dpl.libs.gpio_chooser import GPIO

from dpl.libs.shift_reg_gpio import ShiftRegGPIO

GPIO.setmode(GPIO.BOARD)

si = 37  # пин для входных данных
rck = 33  # пин для сдвига регистров хранения
sck = 35  # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

common_args = [si, rck, sck, sclr]

skip_reason_non_rpi = 'Following tests are only valid for RPi, ' \
                      'other platforms can have different pin IDs'


@unittest.skipUnless(GPIO.__name__ == 'RPi.GPIO', skip_reason_non_rpi)
class TestShiftRegConstructor(unittest.TestCase):
    def __common_arg_test_part(self, invalid_arg, error_type, error_msg):
        for i in range(0, len(common_args)):
            args_copy = common_args[:]

            args_copy[i] = invalid_arg

            with self.assertRaisesRegex(error_type, error_msg):
                ShiftRegGPIO(*args_copy)

    def test_invalid_arg_type(self):
        self.__common_arg_test_part('str', ValueError, 'Channel must be an integer or list/tuple of integers')

    def test_negative_port_value(self):
        self.__common_arg_test_part(-1, ValueError, 'The channel sent is invalid*')

    def test_invalid_port_value(self):
        self.__common_arg_test_part(1000, ValueError, 'The channel sent is invalid*')


class TestShiftRegCapacity(unittest.TestCase):
    def test_invalid_capacity_type(self):
        with self.assertRaisesRegex(ValueError, 'num_of_slaves must be an integer'):
            ShiftRegGPIO(*common_args, 'str')

    def test_invalid_capacity_value(self):
        with self.assertRaisesRegex(ValueError, 'num_of_slaves can\'t be negative'):
            ShiftRegGPIO(*common_args, -1)

    def test_check_single_capacity(self):
        sr = ShiftRegGPIO(*common_args, 0)

        self.assertEqual(sr.get_capacity(), 8)

    def test_check_several_capacity(self):
        nslaves = 2
        ntotal = nslaves + 1

        sr = ShiftRegGPIO(*common_args, nslaves)

        self.assertEqual(sr.get_capacity(), ntotal*8)


class TestShiftRegWrite(unittest.TestCase):
    def test_too_big_value(self):
        sr = ShiftRegGPIO(*common_args)

        with self.assertRaisesRegex(ValueError, 'Number of bits in data can\'t '
                                                'exceed {0} bits'.format(sr.get_capacity())):
            sr.write_data(1 << sr.get_capacity())

    # TODO: Тесты с реальным чтением значений с портов регистра
    @unittest.skipUnless(GPIO.__name__ == 'RPi.GPIO', skip_reason_non_rpi)
    def test_1st_sr_1st_bit(self):
        pass

    @unittest.skipUnless(GPIO.__name__ == 'RPi.GPIO', skip_reason_non_rpi)
    def test_1st_sr_middle_bit(self):
        pass

    @unittest.skipUnless(GPIO.__name__ == 'RPi.GPIO', skip_reason_non_rpi)
    def test_1st_sr_last_bit(self):
        pass

    @unittest.skipUnless(GPIO.__name__ == 'RPi.GPIO', skip_reason_non_rpi)
    def test_2nd_sr_1st_bit(self):
        pass

    @unittest.skipUnless(GPIO.__name__ == 'RPi.GPIO', skip_reason_non_rpi)
    def test_2nd_sr_last_bit(self):
        pass


if __name__ == '__main__':
    unittest.main()
