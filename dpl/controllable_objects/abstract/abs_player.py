from enum import Enum
import logging

from dpl.controllable_objects.abstract import AbsControllable


class AbsPlayer(AbsControllable):
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

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    def play(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def pause(self) -> None:
        raise NotImplementedError

    def next(self) -> None:
        raise NotImplementedError

    def prev(self) -> None:
        raise NotImplementedError

    def get_current_track(self) -> dict:
        raise NotImplementedError

    def toggle(self) -> None:
        """
        Переключает состояние плеера в противоположное:
        запускает остановленное воспроизведение и останавливает запущенное
        :return None
        """
        curr_state = self.get_state()

        # Если проигрывание остановлено...
        if curr_state == self.States.stopped or curr_state == self.States.paused:
            self.play()  # запускаем его

        # Если проигрывание запущено...
        elif curr_state == self.States.playing:
            self.pause()  # приостанавливаем его

        # Fixme CC1:
        else:  # Если состояние другое...
            pass  # игнорируем команду
