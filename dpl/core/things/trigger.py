##############################################################################################
# FIXME List:
#
##############################################################################################

import logging
import warnings
from enum import Enum

from dpl.core.things import Actuator

LOGGER = logging.getLogger(__name__)


class Trigger(Actuator):
    """
    Объект с двумя состояниями: включено и выключено
    """
    class States(Enum):
        """
        Возможные состояния триггера
        """
        on = True
        off = False
        unknown = None

    __COMMAND_LIST = ("toggle", "activate", "deactivate", "on", "off")

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
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
        :return: bool, True в состоянии on, False в других состояниях
        """
        return self.state == self.States.on

    def on(self) -> Actuator.ExecutionResult:
        """
        Немедленно устанавливает триггер в состояние "включено"
        """
        raise NotImplementedError

    def off(self) -> Actuator.ExecutionResult:
        """
        Немедленно устанавливает триггер в состояние "выключено"
        """
        raise NotImplementedError

    def set_on(self) -> Actuator.ExecutionResult:
        """
        Немедленно устанавливает триггер в состояние "включено"
        """
        warnings.warn("Deprecated, use on method instead", DeprecationWarning)
        return self.on()

    def set_off(self) -> Actuator.ExecutionResult:
        """
        Немедленно устанавливает триггер в состояние "выключено"
        """
        warnings.warn("Deprecated, use off method instead", DeprecationWarning)
        return self.off()

    def activate(self) -> Actuator.ExecutionResult:
        """
        Переключает Trigger в состояние on
        :return: Actuator.ExecutionResult
        """
        return self.on()

    def deactivate(self) -> Actuator.ExecutionResult:
        """
        Переключает Trigger в состояние off
        :return: Actuator.ExecutionResult
        """
        return self.off()

    def toggle(self) -> Actuator.ExecutionResult:  # Fixme: CC1
        """
        Переключить из текущего состояния в противоположное
        :return: Actuator.ExecutionResult
        """
        if self.state == self.States.unknown:
            warnings.warn("Unknown state handling may be deleted", FutureWarning)

            LOGGER.debug(
                "Unable to toggle %s object from %s state",
                self,
                self.state
            )
            return Actuator.ExecutionResult.IGNORED_BAD_STATE

        return super().toggle()
