import unittest
import logging
from unittest.mock import Mock

from controllable_objects.specific.serial.trigger import Trigger
from serial import Serial

ser_con = Mock(spec_set=Serial)

con_params = {"pin": 13, "active_low": "false"}
con_params_active_low = {"pin": 13, "active_low": "true"}


class TestTriggerInit(unittest.TestCase):
    def test_init_normal(self):
        trig = Trigger(ser_con, con_params)

        self.assertEqual(trig.ACTIVE, 1)
        self.assertEqual(trig.INACTIVE, 0)

    def test_init_normal_active_low(self):
        trig = Trigger(ser_con, con_params_active_low)

        self.assertEqual(trig.ACTIVE, 0)
        self.assertEqual(trig.INACTIVE, 1)

    def test_init_invalid_connection_type(self):
        with self.assertRaisesRegex(ValueError, 'type of con_instance value must be a Serial'):
            Trigger(None, con_params)


class TestTriggerMethods(unittest.TestCase):
    def test_set_on(self):
        trig = Trigger(ser_con, con_params)

        trig.on()

        ser_con.write.assert_called_with(b'13 1\n')

    def test_set_off(self):
        trig = Trigger(ser_con, con_params)

        trig.off()

        ser_con.write.assert_called_with(b'13 0\n')


class TestTriggerMethodsActiveLow(unittest.TestCase):
    def test_set_on(self):
        trig = Trigger(ser_con, con_params_active_low)

        trig.on()

        ser_con.write.assert_called_with(b'13 0\n')

    def test_set_off(self):
        trig = Trigger(ser_con, con_params_active_low)

        trig.off()

        ser_con.write.assert_called_with(b'13 1\n')
