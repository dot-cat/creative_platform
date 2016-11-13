##############################################################################################
# FIXME List:
# DH2 - Dirty Hack 2
#   Копипаста docstrings методов между классами. Возможно, docstrings в классах тоже
#   можно наследовать?
# CC19 - Consider Change 19
#   Как соединение использовать SerialGPIO вместо Serial?
##############################################################################################

import serial

from controllable_objects.abstract.abs_trigger import AbsTrigger


def check_con_type(test_obj):
    if not isinstance(test_obj, serial.Serial):
        raise ValueError('type of con_instance value must be a Serial')


class Trigger(AbsTrigger):
    """
    Объект с двумя состояниями: включено и выключено,
    connections'ом выступает сдвиговый регистр
    """

    def __init__(self, con_instance, con_params: dict, metadata=None):
        """
        Конструктор
        :param con_instance: экземпляр последовательного подключения
        :param con_params: словарь, который содержит:
                           - pin - id (номер или имя) пина, на котором выставлять состояние
                           - active_low - bool, является ли ноль активным
        :param metadata: метаданные, доп. информация об объекте
        """
        check_con_type(con_instance)

        self.buffer_state = self.States.off

        super().__init__(con_instance, con_params, metadata)

        if con_params.get("active_low", "") == "true":
            self.INACTIVE = 1
            self.ACTIVE = 0
        else:
            self.INACTIVE = 0
            self.ACTIVE = 1

    def set_state(self, target_state):
        # FIXME: DH2
        """
        Немедленно установить конкретное состояние
        :param target_state: значение из self.States, желаемое состояние
        """
        self.set_state_buffer(target_state)

        self.apply_buffer_state()

    def set_state_buffer(self, target_state):
        # FIXME: DH2
        """
        Установить состояние в буффере, не отсылать в connection
        :param target_state: значение из self.States, желаемое состояние
        """
        if type(target_state) != self.States:
            raise ValueError('Type of state argument must be a Trigger.State')

        self.buffer_state = target_state

    def apply_buffer_state(self):
        # FIXME: DH2
        """
        Отослать состояние из буффера в connection
        """
        if self.buffer_state == self.States.on:
            pin_value = self.ACTIVE
        elif self.buffer_state == self.States.off:
            pin_value = self.INACTIVE
        else:
            return

        self.con_instance.write("{0} {1}\n".format(
            self.con_params["pin"], pin_value).encode()
        )

    def get_state(self):
        # FIXME: DH2
        """
        Вернуть свое состояние внешнему миру из буфера
        :return: значение типа self.States
        """
        return self.buffer_state

