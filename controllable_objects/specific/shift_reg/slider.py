##############################################################################################
# FIXME List:
# CC3 - Consider Change 3
#   См. файл controllable_objects/specific/trigger.py
# CC4 - Consider Change 4
#   Проверка на тип толком и не нужна: наличие полей pos, neg и их типы проверяются и так.
# CC5 - Consider Change 5
#   Вместо количества секунд передавать функцию, которая будет ждать окончания перехода.
# CC6 - Consider Change 6
#   Защита на случай многопоточного выполнения - предотвращает зависание двери в не-
#   определенном состоянии (например, предотвращает останов двери раньше времени).
##############################################################################################

from controllable_objects.abstract.abs_slider import AbsSlider
from connections.shift_reg_wrapper import ShiftRegWrapper

import time


def check_shift_reg_type(test_obj):
    if not isinstance(test_obj, ShiftRegWrapper):
        raise ValueError('type of con_instance value must be a ShiftRegWrapper')


class Slider(AbsSlider):
    """
    Объект с четырьмя состояниями: закрыто, открывается, открыто, открывается.
    connections'ом выступает сдвиговый регистр
    """
    class PinStruct(object):
        """
        Структура (почти), содержит информацию о выводах сдвигового регистра,
        которые отвечают за положительный и отрицательный выводы двигателя.
        """
        def __init__(self, pos, neg):
            if pos == neg:
                raise ValueError('pos and neg pins can\'t be the same')

            self.pos = pos
            self.neg = neg

    def __init__(self, con_instance, con_params, transition_time=1):
        """
        Конструктор
        :param con_instance: экземпляр сдвигового регистра
        :param con_params: заполненная структура self.PinStruct, информация о выводах регистра и двигателя
        :param transition_time: время переключения между двумя состояниями в секундах  #CC5
        """
        check_shift_reg_type(con_instance)

        if not isinstance(con_params, self.PinStruct):  # Fixme: CC4
            raise ValueError('con_params must be an instance of Slider.PinStruct class')

        if transition_time <= 0:
            raise ValueError('transition_time must be bigger than zero')

        con_instance.check_bit_pos(con_params.pos)  # Fixme: CC3
        con_instance.check_bit_pos(con_params.neg)  # Fixme: CC3

        self.transition_time = transition_time  # Fixme CC5

        super().__init__(con_instance, con_params)

        self.close()  # Закрываем дверь, если она была открыта

    def set_state(self, target_state):
        """
        Немедленно установить состояние слайдера
        :param target_state: желаемое состояние
        :return: None
        """
        self.set_state_buffer(target_state)

        self.apply_buffer_state()

    def open(self):
        """
        Открыть слайдер, для публичного использования
        :return: None
        """
        # Если слайдер закрыт или закрывается...
        if self.get_state() == self.States.closed or self.get_state() == self.States.closing:
            # ...начинаем его открывать...
            self.set_state(self.States.opening)

            # ...и ждем открытия
            self.__wait_open()
        else:
            return  # Иначе выходим

        # Если никто не изменил состояние слайдера вместо нас...
        if self.get_state() == self.States.opening:  # Fixme: CC6
            self.set_state(self.States.opened)  # ...останавливаем дверь, открыто

    def close(self):
        """
        Закрыть слайдер, для публичного использования
        :return: None
        """
        # Если дверь открыта или открывается...
        if self.get_state() == self.States.opened or self.get_state() == self.States.opening:
            # ...начинаем ее закрывать...
            self.set_state(self.States.closing)

            # ...и ждем закрытия
            self.__wait_close()
        else:
            return  # Иначе выходим

        # Если никто не изменил состояние двери вместо нас...
        if self.get_state() == self.States.closing:  # Fixme: CC6
            self.set_state(self.States.closed)  # ...останавливаем дверь, закрыто

    def set_state_buffer(self, target_state):
        """
        Установка состояния в буффере, без отсылки в con_instance
        :param target_state: желаемое состояние
        :return: None
        """
        if type(target_state) != self.States:
            raise ValueError('Type of target_state argument must be a Slider.State')

        self.con_instance.set_buf_bit(self.con_params.pos, target_state.value[0])
        self.con_instance.set_buf_bit(self.con_params.neg, target_state.value[1])

    def apply_buffer_state(self):
        """
        Применить состояние из буфера
        :return: None
        """
        self.con_instance.write_buffer()

    def get_state(self):
        """
        Получить текущее состояние
        :return: состояние, экземпляр типа Slider.States
        """
        return self.States(
            [
                self.con_instance.get_buf_bit(self.con_params.pos),
                self.con_instance.get_buf_bit(self.con_params.neg)
            ]
        )

    def __wait_close(self):
        """
        Блокирующая функция, ожидает окончания закрытия двери
        :return: None
        """
        time.sleep(self.transition_time)

    def __wait_open(self):
        """
        Блокирующая функция, ожидает окончания открытия двери
        :return: None
        """
        time.sleep(self.transition_time)
