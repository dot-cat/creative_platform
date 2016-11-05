##############################################################################################
# FIXME List:
# DH2 - Dirty Hack 2
#   Копипаста docstrings методов между классами. Возможно, docstrings в классах тоже
#   можно наследовать?
# CN1 - Change Now! 1
#   Игнорятся con_params
##############################################################################################


from controllable_objects.abstract.abs_trigger import AbsTrigger
import serial


def check_con_type(test_obj):
    if not isinstance(test_obj, serial.Serial):
        raise ValueError('type of con_instance value must be a Serial')


class Trigger(AbsTrigger):
    """
    Объект с двумя состояниями: включено и выключено,
    connections'ом выступает сдвиговый регистр
    """

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор
        :param metadata:
        :param con_instance: экземпляр последовательного подключения
        :param con_params: строка, которую высылать
        """
        # FIXME: CN1
        check_con_type(con_instance)

        self.buffer_state = self.States.off

        super().__init__(con_instance, con_params, metadata)

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
            self.con_instance.write(b"0\n")
        elif self.buffer_state == self.States.off:
            self.con_instance.write(b"1\n")

    def get_state(self):
        # FIXME: DH2
        """
        Вернуть свое состояние внешнему миру из буфера
        :return: значение типа self.States
        """
        return self.buffer_state

