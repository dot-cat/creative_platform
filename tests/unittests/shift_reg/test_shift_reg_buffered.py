import unittest
from unittest.mock import Mock

from dpl.libs.shift_reg_buffered import ShiftRegBuffered

from dpl.libs.abs_shift_reg import AbsShiftRegister

sr_base = Mock(spec_set=AbsShiftRegister)
sr_base.get_capacity.return_value = 8


class TestSRBuffer(unittest.TestCase):
    def test_init_state(self):
        sr = ShiftRegBuffered(sr_base)

        self.assertEqual(sr.get_buffer(), 0b0)

    def test_set_invalid_value(self):
        sr = ShiftRegBuffered(sr_base)

        with self.assertRaisesRegex(ValueError, 'Value must be 1 or zero, True or False'):
            sr.set_buf_bit(0, 'str')

        with self.assertRaisesRegex(ValueError, 'Value must be 1 or zero, True or False'):
            sr.set_buf_bit(0, 2)

        with self.assertRaisesRegex(ValueError, 'Value must be 1 or zero, True or False'):
            sr.set_buf_bit(0, -1)

    def test_set_invalid_position(self):
        sr = ShiftRegBuffered(sr_base)

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
        sr = ShiftRegBuffered(sr_base)

        sr.set_buf_bit(0, True)

        self.assertEqual(sr.get_buffer(), 0b1)

    def test_set_last_buf_bit(self):
        sr = ShiftRegBuffered(sr_base)

        max_bit_pos = 7
        expected = 1 << max_bit_pos  # 0b10000000

        sr.set_buf_bit(max_bit_pos, True)

        self.assertEqual(sr.get_buffer(), expected)

    def test_set_bits_successively(self):
        sr = ShiftRegBuffered(sr_base)

        max_bit_pos = 7
        expected = (1 << max_bit_pos) | 1  # 0b10000001

        sr.set_buf_bit(0, True)
        sr.set_buf_bit(max_bit_pos, True)

        self.assertEqual(sr.get_buffer(), expected)

    def test_set_same_bit_successively(self):
        sr = ShiftRegBuffered(sr_base)

        sr.set_buf_bit(0, True)
        sr.set_buf_bit(0, False)

        self.assertEqual(sr.get_buffer(), 0b0)

        sr.set_buf_bit(0, True)
        sr.set_buf_bit(0, True)

        self.assertEqual(sr.get_buffer(), 0b1)

    def test_get_bit_value(self):
        sr = ShiftRegBuffered(sr_base)

        bit_pos = 1

        sr.set_buf_bit(bit_pos, True)

        self.assertEqual(sr.get_buf_bit(bit_pos), True)

        sr.set_buf_bit(bit_pos, False)

        self.assertEqual(sr.get_buf_bit(bit_pos), False)


class TestSRWrite(unittest.TestCase):
    def test_buffer_state_after_write(self):
        sr = ShiftRegBuffered(sr_base)

        test_data = 0b1100

        sr.write_data(test_data)

        self.assertEqual(sr.get_buffer(), test_data)


if __name__ == '__main__':
    unittest.main()
