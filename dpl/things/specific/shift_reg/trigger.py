##############################################################################################
# FIXME List:
# DH2 - Dirty Hack 2
#   Копипаста docstrings методов между классами. Возможно, docstrings в классах тоже
#   можно наследовать?
# CC3 - Consider Change 3
#   Номер пина проверяется несколько раз: один раз в конструкторе Trigger'а и каждый раз
#   при запуске метода set_buf_bit сдвигового регистра. Лишние потери производительности
#   на пустом месте
##############################################################################################


from dpl.specific.connections.shift_reg_buffered import ShiftRegBuffered
from dpl.things.abstract import AbsTrigger


def check_shift_reg_type(test_obj):
    if not isinstance(test_obj, ShiftRegBuffered):
        raise ValueError('type of con_instance value must be a ShiftRegBuffered')


class Trigger(AbsTrigger):
    """
    Объект с двумя состояниями: включено и выключено,
    connections'ом выступает сдвиговый регистр
    """

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор
        :param metadata:
        :param con_instance: экземпляр сдвигового регистра
        :param con_params: целое число, пин сдвигового регистра, на который подключен триггер
        """
        check_shift_reg_type(con_instance)

        con_instance.check_bit_pos(con_params)  # Fixme: CC3

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
        if not isinstance(target_state, self.States):
            raise ValueError('Type of state argument must be a Trigger.State')

        self.con_instance.set_buf_bit(self.con_params, target_state.value)

    def apply_buffer_state(self):
        # FIXME: DH2
        """
        Отослать состояние из буффера в connection
        """
        self.con_instance.write_buffer()

    def get_state(self):
        # FIXME: DH2
        """
        Вернуть свое состояние внешнему миру из буфера
        :return: значение типа self.States
        """
        return self.States(self.con_instance.get_buf_bit(self.con_params))

