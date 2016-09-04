##############################################################################################
# FIXME List:
# CC4 - Consider Change 4
#   Описание CC4 см. в test_sr_trigger
# DH3 - Dirty Hack 3
#   По-хорошему нужно проверять не только конечные состояния (opened, closed), но и
#   промежуточные (opening, closing). Но для этого нужно или использовать Mock'и, или
#   писать собственный сдвиговик-пустышку.
#   Связано с задачей: T70.
##############################################################################################

import RPi.GPIO as GPIO
import unittest
import logging

from controllable_objects.specific.shift_reg.slider import Slider, ShiftRegWrapper


GPIO.setmode(GPIO.BOARD)

si = 37  # пин для входных данных
rck = 33  # пин для сдвига регистров хранения
sck = 35  # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

sr_args = (si, rck, sck, sclr)

sr = ShiftRegWrapper(*sr_args)
sl_bit_pos = 0
sl_bit_neg = 1
transition_time = 0.1

sl_pinstruct = Slider.ConParams(sl_bit_pos, sl_bit_neg, transition_time)
sl_common_params = (sr, sl_pinstruct)

logging.debug('test_sr_slider: {0}'.format(sr))


class TestSliderInit(unittest.TestCase):
    def test_init_normal(self):
        Slider(sr, sl_pinstruct)

    def test_init_invalid_switch_time(self):
        with self.assertRaisesRegex(ValueError, 'transition_time must be bigger than zero'):
            Slider.ConParams(sl_bit_pos, sl_bit_neg, 0)

        with self.assertRaisesRegex(ValueError, 'transition_time must be bigger than zero'):
            Slider.ConParams(sl_bit_pos, sl_bit_neg, -1)

    def test_init_invalid_connection_type(self):
        with self.assertRaisesRegex(ValueError, 'type of con_instance value must be a ShiftRegWrapper'):
            Slider('str', sl_pinstruct)

    def test_init_invalid_connection_params(self):
        with self.assertRaisesRegex(ValueError, 'con_params must be an instance of Slider.ConParams class*'):
            Slider(sr, 'str')

    def test_init_with_dict(self):
        Slider(sr, {"pin_pos": sl_bit_pos, "pin_neg": sl_bit_neg, "transition_time": transition_time})

    def test_init_with_invalid_dict(self):
        with self.assertRaisesRegex(ValueError, "con_params must be an instance of Slider.ConParams class or "
                                                "a compatible dict"):
            Slider(sr, {"bla": sl_bit_pos, "pin_neg": sl_bit_neg, "transition_time": transition_time})


class TestSliderMethods(unittest.TestCase):
    def test_init_state(self):
        sl = Slider(*sl_common_params)

        self.assertEqual(sl.get_state(), sl.States.closed)

    def test_open_closed(self):
        sl = Slider(*sl_common_params)

        sl.open()

        self.assertEquals(sl.get_state(), sl.States.opened)

        self.assertEqual(sr.get_buf_bit(sl_bit_pos), 1)
        self.assertEqual(sr.get_buf_bit(sl_bit_neg), 1)

    def test_close_closed(self):
        sl = Slider(*sl_common_params)

        sl.close()

        self.assertEquals(sl.get_state(), sl.States.closed)

        self.assertEqual(sr.get_buf_bit(sl_bit_pos), 0)
        self.assertEqual(sr.get_buf_bit(sl_bit_neg), 0)

    def test_close_opened(self):
        sl = Slider(*sl_common_params)

        sl.open()

        sl.close()

        self.assertEquals(sl.get_state(), sl.States.closed)

        self.assertEqual(sr.get_buf_bit(sl_bit_pos), 0)
        self.assertEqual(sr.get_buf_bit(sl_bit_neg), 0)

    def test_open_opened(self):
        sl = Slider(*sl_common_params)

        sl.open()

        sl.open()

        self.assertEquals(sl.get_state(), sl.States.opened)

        self.assertEqual(sr.get_buf_bit(sl_bit_pos), 1)
        self.assertEqual(sr.get_buf_bit(sl_bit_neg), 1)

    def test_toggle_closed(self):
        sl = Slider(*sl_common_params)

        sl.toggle()

        self.assertEquals(sl.get_state(), sl.States.opened)

        self.assertEqual(sr.get_buf_bit(sl_bit_pos), 1)
        self.assertEqual(sr.get_buf_bit(sl_bit_neg), 1)

    def test_toggle_opened(self):
        sl = Slider(*sl_common_params)

        sl.open()

        sl.toggle()

        self.assertEquals(sl.get_state(), sl.States.closed)

        self.assertEqual(sr.get_buf_bit(sl_bit_pos), 0)
        self.assertEqual(sr.get_buf_bit(sl_bit_neg), 0)
