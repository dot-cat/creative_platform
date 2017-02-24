##############################################################################################
# FIXME List:
# CC1 - Consider Change 1
#   toggle переключает не только между стабильными состояниями ('открыто' <-> 'закрыто'),
#   но и между нестабильными ('открывается' <-> 'закрывается').
#   При этом нужно быть внимательным. Нельзя допустить открывание/закрывание слайдера
#   наполовину из-за того, что один из процессов остановит дверь раньше времени.
#   Возможно, следует переключать только между стабильными состояниями.
##############################################################################################

import logging
from enum import Enum
import warnings

from dpl.core.things import Actuator

logger = logging.getLogger(__name__)


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

    __COMMAND_LIST = ("toggle", "activate", "deactivate", "open", "close")

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    @property
    def actions(self) -> tuple:
        """
        Возвращает список всех доступных команд
        :return: tuple
        """
        return self.__COMMAND_LIST

    @property
    def is_active(self) -> bool:
        """
        Находится ли объект в одном из активных состояний
        :return: bool, True в состоянии opening либо open, False в других состояниях
        """
        return self.state == self.States.opened or \
               self.state == self.States.opening

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

    def activate(self) -> Actuator.ExecutionResult:
        """
        Переключает слайдер в состояние open
        :return: Actuator.ExecutionResult
        """
        return self.open()

    def deactivate(self) -> Actuator.ExecutionResult:
        """
        Переключает слайдер в состояние closed
        :return: Actuator.ExecutionResult
        """
        return self.close()

    def toggle(self) -> Actuator.ExecutionResult:
        """
        Переключает состояние слайдера в противоположное:
        открывает закрытый, закрывает открытый
        :return: Actuator.ExecutionResult
        """
        if self.state == self.States.unknown:
            warnings.warn("Unknown state handling may be deleted", FutureWarning)

            logger.debug(
                "Unable to toggle %s object from %s state",
                self,
                self.state
            )
            return Actuator.ExecutionResult.IGNORED_BAD_STATE

        return super().toggle()
