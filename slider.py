##############################################################################################
# FIXME List:
# CC1 - Consider Change 1
#   toggle переключает только между стабильными состояниями. Возможно, нужно добавить и
#   переключение между нестабильными состояниями ('открывается' <-> 'закрывается').
#   Но при этом нужно быть внимательным. Нельзя допустить открываение/закрывание слайдера
#   наполовину из-за того, что один из процессов остановит дверь раньше времени.
##############################################################################################

from enum import Enum

from dpl.core.things import Actuator


class Slider(Actuator):
    """
    Объект с четырьмя состояниями: закрыто, открывается, открыто, открывается
    """
    class States(Enum):
        """
        Возможные состояния выдвигающегося элемента
        """
        closed  = (0, 0)
        closing = (0, 1)
        opening = (1, 0)
        opened  = (1, 1)
        unknown = None

    __COMMAND_LIST = ("toggle", "open", "close")

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    @property
    def commands(self) -> tuple:
        """
        Возвращает список всех доступных команд
        :return: tuple
        """
        return self.__COMMAND_LIST

    @property
    def extended_info(self) -> None:
        """
        Возвращает расширенную информацию о состоянии объекта
        :return: None
        """
        return None

    def open(self) -> Actuator.ExecutionResult:
        """
        Открывает слайдер
        :return: Actuator.ExecutionResult
        """
        raise NotImplementedError

    def close(self) -> Actuator.ExecutionResult:
        """
        Закрывает слайдер
        :return: Actuator.ExecutionResult
        """
        raise NotImplementedError

    def toggle(self) -> Actuator.ExecutionResult:
        """
        Переключает состояние слайдера в противоположное:
        открывает закрытый, закрывает открытый
        :return: Actuator.ExecutionResult
        """
        if self.state == self.States.opened:  # Если слайдер открыт...
            return self.close()  # закрываем его

        elif self.state == self.States.closed:  # Если слайдер закрыт...
            return self.open()  # открываем его

        # Fixme CC1:
        else:  # Если слайдер открывается или закрывается...
            return Actuator.ExecutionResult.IGNORED_BAD_STATE  # игнорируем команду
