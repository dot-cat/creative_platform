##############################################################################################
# FIXME List:
#
##############################################################################################

import logging

from dpl.core.things import Actuator

logger = logging.getLogger(__name__)


class Trigger(Actuator):
    """
    Объект с двумя состояниями: включено и выключено
    """
    class States(Actuator.States):
        """
        Возможные состояния триггера
        """
        on = True
        off = False

    __COMMAND_LIST = ("toggle", "on", "off")

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        """
        super().__init__(con_instance, con_params, metadata)

    @property
    def command_list(self) -> tuple:
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

    def execute(self, cmd: str, *args, **kwargs) -> Actuator.ExecutionResult:
        """
        Запускает выполнение команды, указанной в cmd
        :param cmd: строка, команда на выполнение
        :param args, kwargs: параметры команды
        :return: возвращаемое значение
        """
        invalid_cmd_error = ValueError("Invalid command: {0}".format(cmd))

        if cmd not in self.__COMMAND_LIST:
            raise invalid_cmd_error

        cmd_func = self.__getattribute__(cmd)

        if cmd_func is not callable:
            raise invalid_cmd_error

        return cmd_func(*args, **kwargs)

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
        raise DeprecationWarning("Deprecated, use on method instead")

    def set_off(self) -> Actuator.ExecutionResult:
        """
        Немедленно устанавливает триггер в состояние "выключено"
        """
        raise DeprecationWarning("Deprecated, use off method instead")

    def toggle(self) -> Actuator.ExecutionResult:
        """
        Переключить из текущего состояния в противоположное
        """
        if self.state == self.States.on:  # если переключатель включен
            # выключаем его
            return self.off()

        elif self.state == self.States.off:  # если переключатель выключен...
            # включаем его
            return self.on()

        else:
            logger.debug(
                "Unable to toggle %s object from %s state",
                self,
                self.state
            )
            return Actuator.ExecutionResult.IGNORED_BAD_STATE
