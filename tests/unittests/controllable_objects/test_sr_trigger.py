##############################################################################################
# FIXME List:
# CC4 - Consider Change 4
#   В python есть такая замечательная штука, как unittest.mock. Она позволяет заменить реальные
#   объекты на заглушки, тестировать вызов функций и переданные при этом аргументы и т.д.
#   Как результат - мы убираем привязку к зависимостям при тестировании и можем, например,
#   тестировать сдвиговый регистр на ноуте, без RPi.GPIO. Или использовать CI-сервисы
#   (например Travis, Jenkins и др.)
#   Задача (T70): разобраться с mock'ами, убрать привязку к сдвиговику и GPIO в тестах.
##############################################################################################

import RPi.GPIO as GPIO
import unittest
import logging

from controllable_objects.specific.shift_reg.trigger import Trigger, ShiftRegWrapper


GPIO.setmode(GPIO.BOARD)

si = 37  # пин для входных данных
rck = 33  # пин для сдвига регистров хранения
sck = 35  # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

sr_args = [si, rck, sck, sclr]

sr = ShiftRegWrapper(*sr_args)
tr_bit_pos = 0

logging.debug('test_sr_trigger: {0}'.format(sr))


class TestTriggerInit(unittest.TestCase): 
    def test_init_normal(self):
        Trigger(sr, tr_bit_pos)

    def test_init_invalid_connection_type(self):
        with self.assertRaisesRegex(ValueError, 'type of con_instance value must be a ShiftRegWrapper'):
            Trigger('str', tr_bit_pos)

    def test_init_invalid_pin(self):
        with self.assertRaisesRegex(ValueError, 'Bit number must be an integer'):
            Trigger(sr, 'str')

        with self.assertRaisesRegex(ValueError, 'Bit number must be positive or zero'):
            Trigger(sr, -1)

        with self.assertRaisesRegex(ValueError, 'Bit position can\'t be bigger than '
                                                'register capacity \({0}\)'.format(sr.get_capacity())):
            Trigger(sr, sr.get_capacity())

        with self.assertRaisesRegex(ValueError, 'Bit position can\'t be bigger than '
                                                'register capacity \({0}\)'.format(sr.get_capacity())):
            Trigger(sr, sr.get_capacity() + 1)


class TestTriggerMethods(unittest.TestCase):
    def test_get_init_state(self):
        trig = Trigger(sr, tr_bit_pos)

        self.assertEqual(trig.get_state(), trig.States.off)

    def test_set_invalid_state(self):
        trig = Trigger(sr, tr_bit_pos)

        with self.assertRaisesRegex(ValueError, 'Type of state argument must be a Trigger.State'):
            trig.set_state('str')

    def test_set_state_on(self):
        trig = Trigger(sr, tr_bit_pos)

        trig.set_state(trig.States.on)

        self.assertEqual(trig.get_state(), trig.States.on)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 1)

    def test_set_state_off(self):
        trig = Trigger(sr, tr_bit_pos)

        trig.set_state(trig.States.off)

        self.assertEqual(trig.get_state(), trig.States.off)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 0)

    def test_set_on(self):
        trig = Trigger(sr, tr_bit_pos)

        trig.set_on()

        self.assertEqual(trig.get_state(), trig.States.on)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 1)

    def test_set_off(self):
        trig = Trigger(sr, tr_bit_pos)

        trig.set_off()

        self.assertEqual(trig.get_state(), trig.States.off)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 0)

    def test_toggle(self):
        trig = Trigger(sr, tr_bit_pos)

        trig.set_off()

        trig.toggle()

        self.assertEqual(trig.get_state(), trig.States.on)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 1)

        trig.toggle()

        self.assertEqual(trig.get_state(), trig.States.off)

        self.assertEqual(sr.get_buf_bit(tr_bit_pos), 0)


if __name__ == '__main__':
    unittest.main()
