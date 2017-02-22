from enum import IntEnum

from dpl.core.things import Thing


class Actuator(Thing):
    """
    Базовый абстрактный класс для всех объектов системы ("вещей"),
    которые могут выполнять некоторый набор операций

    Гарантии:
    * выполняемые команды возвращают код ошибки при обрыве соединения
    * позволяет получить список всех доступных команд
    * обладает методом execute, который выполняет одну из доступных команд
    """

    class ExecutionResult(IntEnum):
        """
        Результат выполнения операции
        """
        OK = 0
        IGNORED_BAD_STATE = 1
        IGNORED_UNAVAILABLE = 2

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    def execute(self, cmd: str, *args, **kwargs) -> ExecutionResult:
        """
        Запускает выполнение команды, указанной в cmd
        :param cmd: строка, команда на выполнение
        :param args, kwargs: параметры команды
        :return: возвращаемое значение
        """
        invalid_cmd_error = ValueError("Invalid command: {0}".format(cmd))

        if cmd not in self.commands:
            raise invalid_cmd_error

        cmd_func = self.__getattribute__(cmd)

        if cmd_func is not callable:
            raise invalid_cmd_error

        return cmd_func(*args, **kwargs)

    def toggle(self) -> ExecutionResult:
        """
        Переключает объект между двумя крайними состояниями
        :return: результат выполнения
        """
        raise NotImplementedError
