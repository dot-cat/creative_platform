import logging
import unittest
from unittest.mock import Mock

from dpl.libs.abs_shift_reg import AbsShiftRegister
from dpl.specific.things.triggers.shift_reg_trigger import ShiftRegTrigger, ShiftRegBuffered

sr_base = Mock(spec_set=AbsShiftRegister)
sr_base.get_capacity.return_value = 8

sr = ShiftRegBuffered(sr_base)

tr_bit_pos = 0

logging.debug('test_sr_trigger: {0}'.format(sr))


class TestTriggerInit(unittest.TestCase): 
    def test_init_normal(self):
        ShiftRegTrigger(sr, tr_bit_pos)

    def test_init_invalid_connection_type(self):
        with self.assertRaisesRegex(ValueError, 'type of con_instance value must be a ShiftRegBuffered'):
            ShiftRegTrigger('str', tr_bit_pos)

    def test_init_invalid_pin(self):
        with self.assertRaisesRegex(ValueError, 'Bit number must be an integer'):
            ShiftRegTrigger(sr, 'str')

        with self.assertRaisesRegex(ValueError, 'Bit number must be positive or zero'):
            ShiftRegTrigger(sr, -1)

        with self.assertRaisesRegex(ValueError, 'Bit position can\'t be bigger than '
                                                'register capacity \({0}\)'.format(sr.get_capacity())):
            ShiftRegTrigger(sr, sr.get_capacity())

        with self.assertRaisesRegex(ValueError, 'Bit position can\'t be bigger than '
                                                'register capacity \({0}\)'.format(sr.get_capacity())):
            ShiftRegTrigger(sr, sr.get_capacity() + 1)


class TestTriggerMethods(unittest.TestCase):
    def test_get_init_state(self):
        trig = ShiftRegTrigger(sr, tr_bit_pos)

        self.assertEqual(trig.get_state(), trig.States.off)

    def test_set_invalid_state(self):
        trig = ShiftRegTrigger(sr, tr_bit_pos)

        with self.assertRaisesRegex(ValueError, 'Type of state argument must be a Trigger.State'):
            trig.set_state('str')

    def test_set_state_on(self):
        trig = ShiftRegTrigger(sr, tr_bit_pos)

        trig.set_state(trig.States.on)

        self.assertEqual(trig.get_state(), trig.States.on)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 1)

    def test_set_state_off(self):
        trig = ShiftRegTrigger(sr, tr_bit_pos)

        trig.set_state(trig.States.off)

        self.assertEqual(trig.get_state(), trig.States.off)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 0)

    def test_set_on(self):
        trig = ShiftRegTrigger(sr, tr_bit_pos)

        trig.set_on()

        self.assertEqual(trig.get_state(), trig.States.on)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 1)

    def test_set_off(self):
        trig = ShiftRegTrigger(sr, tr_bit_pos)

        trig.set_off()

        self.assertEqual(trig.get_state(), trig.States.off)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 0)

    def test_toggle(self):
        trig = ShiftRegTrigger(sr, tr_bit_pos)

        trig.set_off()

        trig.toggle()

        self.assertEqual(trig.get_state(), trig.States.on)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 1)

        trig.toggle()

        self.assertEqual(trig.get_state(), trig.States.off)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 0)


if __name__ == '__main__':
    unittest.main()
