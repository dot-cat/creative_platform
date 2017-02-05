from enum import Enum

from dpl.core.things import Actuator


class Player(Actuator):
    """
    Плеер. Объект, который проигрывает медиафайлы
    """
    class States(Enum):
        """
        Возможные состояния выдвигающегося элемента
        """
        playing = 0,
        stopped = 1,
        paused = 2,
        undefined = None

    __COMMAND_LIST = ("toggle", "play", "stop", "pause", "next", "prev")

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    @property
    def command_list(self) -> tuple:
        """
        Возвращает список всех доступных команд
        :return: tuple
        """
        return self.__COMMAND_LIST

    def play(self) -> Actuator.ExecutionResult:
        raise NotImplementedError

    def stop(self) -> Actuator.ExecutionResult:
        raise NotImplementedError

    def pause(self) -> Actuator.ExecutionResult:
        raise NotImplementedError

    def next(self) -> Actuator.ExecutionResult:
        raise NotImplementedError

    def prev(self) -> Actuator.ExecutionResult:
        raise NotImplementedError

    def toggle(self) -> Actuator.ExecutionResult:
        """
        Переключает состояние плеера в противоположное:
        запускает остановленное воспроизведение и останавливает запущенное
        :return None
        """
        # Если проигрывание остановлено...
        if self.state == self.States.stopped or self.state == self.States.paused:
            self.play()  # запускаем его

        # Если проигрывание запущено...
        elif self.state == self.States.playing:
            self.pause()  # приостанавливаем его

        # Fixme CC1:
        else:  # Если состояние другое...
            return self.ExecutionResult.IGNORED_BAD_STATE
