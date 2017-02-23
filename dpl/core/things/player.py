##############################################################################################
# FIXME List:
# CC26 - Consider Change 26
#   Реализовать setter для свойства volume
##############################################################################################

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

    __COMMAND_LIST = ("set_volume", "toggle", "play", "stop",
                      "pause", "next", "prev", "seek")

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
    def volume(self) -> int:  # Fixme: CC26
        """
        Текущий уровень громкости в процентах
        :return: int, -1 = n/a
        """
        raise NotImplementedError

    @property
    def source(self) -> str:
        """
        Имя текущего файла либо URI потока
        :return: str
        """
        raise NotImplementedError

    @property
    def title(self) -> str:
        """
        Название текущего трека либо потока
        :return: str
        """
        raise NotImplementedError

    @property
    def artist(self) -> str or None:
        """
        Имя исполнителя трека
        :return: строка либо None, если информация отсутствует
        """
        raise NotImplementedError

    @property
    def album(self) -> str or None:
        """
        Название альбома трека
        :return: строка либо None, если информация отсутствует
        """
        raise NotImplementedError

    @property
    def elapsed(self) -> float:
        """
        Позиция проигрывания трека. Истекшее время с начала проигрывания трека в секундах.
        :return: float
        """
        raise NotImplementedError

    @property
    def duration(self) -> float:
        """
        Длина трека текущего трека в секундах
        :return: float, -1.0 = бесконечный трек/стрим
        """
        raise NotImplementedError

    def to_dict(self) -> dict:
        """
        Метод, возвращающий копию объекта в виде словаря
        :return: словарь-копия значений из свойств
        """
        result = super().to_dict()  # Свойства базового класса

        # Специфичные поля:
        result["volume"] = self.volume
        result["source"] = self.source
        result["title"] = self.title
        result["artist"] = self.artist
        result["album"] = self.album
        result["elapsed"] = self.elapsed
        result["duration"] = self.duration

        return result

    def set_volume(self, value: int) -> Actuator.ExecutionResult:
        """
        Установить новое значение громкости в диапазоне от 0 до 100
        :param value: значаение громкости
        :return: Actuator.ExecutionResult
        """
        raise NotImplementedError

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

    def seek(self, track_pos: float) -> Actuator.ExecutionResult:
        """
        Прокрутить текущий трек к указанной позиции
        :param track_pos: позиция в треке
        :return: Actuator.ExecutionResult
        """
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
