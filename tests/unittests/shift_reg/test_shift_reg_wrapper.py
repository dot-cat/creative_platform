import RPi.GPIO as GPIO
import unittest

from connections.shift_reg_wrapper import ShiftRegWrapper


GPIO.setmode(GPIO.BOARD)

si = 37  # пин для входных данных
rck = 33  # пин для сдвига регистров хранения
sck = 35  # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

common_args = [si, rck, sck, sclr]


class TestSRBuffer(unittest.TestCase):
    def test_init_state(self):
        sr = ShiftRegWrapper(*common_args)

        self.assertEqual(sr.get_buffer(), 0b0)

    def test_set_invalid_value(self):
        sr = ShiftRegWrapper(*common_args)

        with self.assertRaisesRegex(ValueError, 'Value must be 1 or zero, True or False'):
            sr.set_buf_bit(0, 'str')

        with self.assertRaisesRegex(ValueError, 'Value must be 1 or zero, True or False'):
            sr.set_buf_bit(0, 2)

        with self.assertRaisesRegex(ValueError, 'Value must be 1 or zero, True or False'):
            sr.set_buf_bit(0, -1)

    def test_set_invalid_position(self):
        sr = ShiftRegWrapper(*common_args)

        with self.assertRaisesRegex(ValueError, 'Bit number must be an integer'):
            sr.set_buf_bit('str', 1)

        with self.assertRaisesRegex(ValueError, 'Bit number must be positive or zero'):
            sr.set_buf_bit(-1, 1)

        with self.assertRaisesRegex(ValueError, 'Bit position can\'t be bigger than '
                                                'register capacity \({0}\)'.format(sr.get_capacity())):
            sr.set_buf_bit(sr.get_capacity(), 1)

        with self.assertRaisesRegex(ValueError, 'Bit position can\'t be bigger than '
                                                'register capacity \({0}\)'.format(sr.get_capacity())):
            sr.set_buf_bit(sr.get_capacity() + 1, 1)

    def test_set_first_buf_bit(self):
        sr = ShiftRegWrapper(*common_args)

        sr.set_buf_bit(0, True)

        self.assertEqual(sr.get_buffer(), 0b1)

    def test_set_last_buf_bit(self):
        sr = ShiftRegWrapper(*common_args)

        max_bit_pos = 7
        expected = 1 << max_bit_pos  # 0b10000000

        sr.set_buf_bit(max_bit_pos, True)

        self.assertEqual(sr.get_buffer(), expected)

    def test_set_bits_successively(self):
        sr = ShiftRegWrapper(*common_args)

        max_bit_pos = 7
        expected = (1 << max_bit_pos) | 1  # 0b10000001

        sr.set_buf_bit(0, True)
        sr.set_buf_bit(max_bit_pos, True)

        self.assertEqual(sr.get_buffer(), expected)

    def test_set_same_bit_successively(self):
        sr = ShiftRegWrapper(*common_args)

        sr.set_buf_bit(0, True)
        sr.set_buf_bit(0, False)

        self.assertEqual(sr.get_buffer(), 0b0)

        sr.set_buf_bit(0, True)
        sr.set_buf_bit(0, True)

        self.assertEqual(sr.get_buffer(), 0b1)

    def test_get_bit_value(self):
        sr = ShiftRegWrapper(*common_args)

        bit_pos = 1

        sr.set_buf_bit(bit_pos, True)

        self.assertEqual(sr.get_buf_bit(bit_pos), True)

        sr.set_buf_bit(bit_pos, False)

        self.assertEqual(sr.get_buf_bit(bit_pos), False)


class TestSRWrite(unittest.TestCase):
    def test_buffer_state_after_write(self):
        sr = ShiftRegWrapper(*common_args)

        test_data = 0b1100

        sr.write_data(test_data)

        self.assertEqual(sr.get_buffer(), test_data)


if __name__ == '__main__':
    unittest.main()
