##############################################################################################
# FIXME List:
# CC3 - Consider Change 3
#   См. файл things/specific/trigger.py
# CC4 - Consider Change 4
#   Проверка на тип толком и не нужна: наличие полей pos, neg и их типы проверяются и так.
# CC5 - Consider Change 5
#   Вместо количества секунд передавать функцию, которая будет ждать окончания перехода.
# CC6 - Consider Change 6
#   Защита на случай многопоточного выполнения - предотвращает зависание двери в не-
#   определенном состоянии (например, предотвращает останов двери раньше времени).
##############################################################################################

import time

from dpl.specific.connections.shift_reg_buffered import ShiftRegBuffered
from dpl.things.abstract import AbsSlider


def check_shift_reg_type(test_obj):
    if not isinstance(test_obj, ShiftRegBuffered):
        raise ValueError('type of con_instance value must be a ShiftRegBuffered')


class Slider(AbsSlider):
    """
    Объект с четырьмя состояниями: закрыто, открывается, открыто, открывается.
    connections'ом выступает сдвиговый регистр
    """
    class ConParams(object):
        """
        Структура (почти), содержит информацию, необходимую для работы со сдвиговым регистром.
        """
        def __init__(self, pin_pos, pin_neg, transition_time=1):
            """
            Конструктор
            :param pin_pos: положительный пин на сдвиговом регистре
            :param pin_neg: отрицательный пин на сдвиговом регистре
            :param transition_time: время переключения между состояниями в секундах
            """
            if pin_pos == pin_neg:
                raise ValueError('pos and neg pins can\'t be the same')

            if transition_time <= 0:
                raise ValueError('transition_time must be bigger than zero')

            self.pos = pin_pos
            self.neg = pin_neg
            self.transition_time = transition_time  # Fixme: CC5

    def __init__(self, con_instance, con_params: ConParams or dict, metadata=None):
        """
        Конструктор
        :param metadata:
        :param con_instance: экземпляр сдвигового регистра
        :param con_params: заполненная структура self.ConParams, информация о подключении.
               Или словарь, на основе которого такую структуру можно создать.
        """
        check_shift_reg_type(con_instance)

        con_params_error = ValueError(
            "con_params must be an instance of "
            "Slider.ConParams class or a compatible dict"
        )

        if not isinstance(con_params, self.ConParams):  # Fixme: CC4
            if isinstance(con_params, dict):
                try:
                    con_params = self.ConParams(**con_params)
                except TypeError:
                    raise con_params_error
            else:
                raise con_params_error

        con_instance.check_bit_pos(con_params.pos)  # Fixme: CC3
        con_instance.check_bit_pos(con_params.neg)  # Fixme: CC3

        super().__init__(con_instance, con_params, metadata)

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
        if not isinstance(target_state, self.States):
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
        time.sleep(self.con_params.transition_time)  # Fixme: CC5

    def __wait_open(self):
        """
        Блокирующая функция, ожидает окончания открытия двери
        :return: None
        """
        time.sleep(self.con_params.transition_time)  # Fixme: CC5
