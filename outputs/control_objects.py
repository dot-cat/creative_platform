#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shift_reg_wrapper import ShiftRegWrapper
from enum import Enum


class Trigger(object):
    """
    Объект с двумя состояниями: включено и выключено.
    Во включенном состоянии записывает 1-цу в регистр,
    в выключенном - ноль
    """

    class States(Enum):
        """
        Возможные состояния переключателя
        """
        on = True
        off = False

    def __init__(self, shift_reg, bit_pos):
        """
        Конструктор
        :param shift_reg: сдвиговый регистр, в котором хранится текущее состояние
        :param bit_pos: позиция бита, который контролирует объект
        :return: None
        """
        self.shift_reg = shift_reg
        self.bit_pos = bit_pos

    def set_state(self, state):
        """
        Установка состояния объекта и запись состояния в буфер
        :param state: желаемое состояние
        :return: None
        """
        assert Trigger.States.on == True and Trigger.States.off == False,\
            'state code changed, update this function before usage'

        if type(state) != Trigger.States:
            raise ValueError('Type of state argument must be a Trigger.State')

        self.shift_reg.set_buf_bit(self.bit_pos, state)
        return

    def set_on(self):
        """
        Включение объекта
        :return: none
        """
        self.set_state(self.States.on)
        return

    def set_off(self):
        """
        Выключение объекта
        :return: none
        """
        self.set_state(self.States.off)
        return

    def get_state(self):
        """
        Получение текущего состояния переключателя
        :return: значение типа Trigger.States
        """
        return Trigger.States(self.shift_reg.get_buf_bit(self.bit_pos))

    def apply_state(self):
        """
        Принудительная запись содержимого буфера в регистр
        :return: None
        """
        self.shift_reg.write_buffer()


class Slider(object):
    """
    Объект с четырьмя состояниями: закрыто, открывается, открыто, открывается
    """
    class States(Enum):
        """
        Возможные состояния выдвигающегося элемента
        """
        closed  = [0, 0]
        closing = [0, 1]
        opening = [1, 0]
        opened  = [1, 1]



    pass


class Door(Slider):
    pass


class Blinds(Slider):
    pass


class Light(Trigger):
    pass


class Cooler(Trigger):
    pass