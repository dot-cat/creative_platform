##############################################################################################
# FIXME List:
# CC27 - Consider Change 27
#   Заменить реализацию на _alternative_get_title
# CC28 - Consider Change 28
#   Пересмотреть ВЕСЬ модуль. И отрефакторить при необходимости. Сейчас (28.02.17) на
#   продолжение возни особо нет времени. Есть более важные задачи.
#   Конкретно по пунктам:
#   * select вместо polling, в отдельном потоке (см. как пример https://git.io/vyYGh)
#   * что-то сделать с декораторами (удалить вообще? вынести в класс? другой вариант?)
#   *
##############################################################################################


import contextlib
import logging
import time
import warnings
import threading

from dpl.core.things import ThingFactory, ThingRegistry
from dpl.core.things import Actuator
from dpl.core.things import Player
from dpl.specific.connections.mpd_client import MPDClientConnection

import mpd

LOGGER = logging.getLogger(__name__)


def _execute_if_enabled(method_to_decorate):
    def wrapper(self, *args, **kwargs):
        if not self._is_enabled:
            return Actuator.ExecutionResult.IGNORED_UNAVAILABLE
        else:
            return method_to_decorate(self, *args, **kwargs)

    return wrapper


def _lost_checker(method_to_decorate):
    def wrapper(self, *args, **kwargs):
        try:
            return method_to_decorate(self, *args, **kwargs)
        except mpd.ConnectionError:
            self._is_lost = True
            return Actuator.ExecutionResult.IGNORED_UNAVAILABLE
        except ConnectionRefusedError:
            self._is_lost = True
            return Actuator.ExecutionResult.IGNORED_UNAVAILABLE
        except ConnectionResetError:
            self._is_lost = True
            return Actuator.ExecutionResult.IGNORED_UNAVAILABLE

    return wrapper


class MPDPlayer(Player):
    def __init__(self, con_instance: MPDClientConnection, con_params=None, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)
        self._is_enabled = True  # type: bool
        self._last_updated = time.time()  # type: float
        self._last_status = {}  # type: dict
        self._last_current_track = {}  # type: dict
        self._upd_thread = None  # type: threading.Thread
        self._upd_interval = 2  # seconds
        self._is_lost_value = False  # type: bool
        self._con_lock = threading.Lock()  # type: threading.Lock

        self._restart_updater()

    def __del__(self):
        LOGGER.debug("Deleter: %s", self)

    def _restart_updater(self):
        self._upd_thread = threading.Thread(target=self._updater_loop)
        self._upd_thread.start()

    @contextlib.contextmanager
    def _connection(self):
        try:
            self._con_lock.acquire()
            self._con_instance.reconnect()
            self._is_lost = False
            yield
        except mpd.ConnectionError as e:
            if e.args[0] == 'Already connected':
                LOGGER.warning("Connection already established in %s", self)
                yield
            else:
                raise
        finally:
            self._con_instance.disconnect()
            self._con_lock.release()

    @classmethod
    def __mpd_state_to_self_state(cls, mpd_state: str) -> Player.States:
        if mpd_state == "play":
            return cls.States.playing
        elif mpd_state == "stop":
            return cls.States.stopped
        elif mpd_state == "pause":
            return cls.States.paused
        elif mpd_state is None:
            return cls.States.unknown
        else:
            LOGGER.error("Unknown state of the MPD player: %s", mpd_state)
            return cls.States.unknown

    def _call_on_update(self, *args, **kwargs):
        if self.on_update:
            self.on_update(args, kwargs)

    def _call_on_avail_update(self, *args, **kwargs):
        if self.on_avail_update:
            self.on_avail_update(args, kwargs)

    def _updater_loop(self):
        while self._is_enabled:
            self._update()
            time.sleep(self._upd_interval)

    @property
    def state(self):
        return self.__mpd_state_to_self_state(
            self._last_status.get("state")
        )

    @property
    def is_available(self) -> bool:  # FIXME: Изменить реализацию, загрушка
        """
        Доступность объекта для использования
        :return: True - доступен, False - недоступен
        """
        return self._is_enabled and not self._is_lost

    @property
    def last_updated(self) -> float:  # Fixme: CC23
        """
        Возвращает время, когда объект был обновлен в последний раз
        :return: float, UNIX time
        """
        return self._last_updated

    @property
    def _is_lost(self) -> bool:
        return self._is_lost_value

    @_is_lost.setter
    def _is_lost(self, value: bool) -> None:
        if self._is_lost_value != value:
            self._is_lost_value = value
            LOGGER.debug("Connection status change: lost = %s on %s", self._is_lost, self)
            self._call_on_update()

    def disable(self) -> None:
        """
        Отключает объект, останавливает обновление состояния и
        делает его неактивным
        :return: None
        """
        if self._is_enabled:
            self._is_enabled = False
            self._upd_thread.join()

            LOGGER.debug("Component disabled: %s", self)

            self._call_on_avail_update(self, None)

    def enable(self) -> None:
        """
        Включает объект, запускает обновление состояние и делает
        его активным
        :return: None
        """
        if not self._is_enabled:
            self._is_enabled = True
            self._restart_updater()

            LOGGER.debug("Component enabled: %s", self)

            self._call_on_avail_update(self, None)

    @_lost_checker
    def _update(self, skip_check: bool=False) -> None:
        """
        Обновляет значения всех свойств
        :skip_check: Пропускать ли проверку на наличие отличий
        :return:
        """
        assert self._is_enabled

        old_properies = self.to_dict()

        with self._connection():
            new_status = self._con_instance.status()
            new_curr_track = self._con_instance.currentsong()

        self._last_status = new_status
        self._last_current_track = new_curr_track
        self._last_updated = time.time()

        self._call_on_update(self, old_properies)

    @property
    def volume(self) -> int:  # Fixme: CC26
        """
        Текущий уровень громкости в процентах
        :return: int, -1 = n/a
        """
        return self._last_status.get("volume", -1)

    @property
    def source(self) -> str or None:
        """
        Имя текущего файла либо URI потока
        :return: str
        """
        return self._last_current_track.get("file", None)

    @staticmethod
    def _alternative_get_title(ti: dict) -> str:
        """
        Вернуть название текущего трека.
        Альтернативный подход к составлению заголовка. Используется в mpc и компоненте HomeAssistant
        :param: Информация о текущем треке, полученная от MPD
        :return: название трека
        """
        warnings.warn("This method may be deleted in the next releases", FutureWarning)

        default = None

        name = ti.get("name", default)
        title = ti.get("title", default)

        if name is None:  # it's not a stream
            result = title
        elif title is None:  # there is no title, may be a stream
            result = name
        else:  # it's a stream with a title
            result = "{stream_name}: {title}".format(stream_name=name, title=title)

        return result

    def _get_title(self, ti: dict) -> str:
        """
        Вернуть название текущего трека.
        Подход к составлению заголовка, который используется в MPDroid и ncmpcpp
        :param: Информация о текущем треке, полученная от MPD
        :return: название трека
        """
        default = "unknown"

        source = ti.get("file", default)  # Если источник неизвестен - вернуть None
        name = ti.get("name", source)  # Если поток неизвестен - вернуть источник
        title = ti.get("title", name)  # Если название трека неизевстно - вернуть поток

        return title

    @property
    def title(self) -> str:
        """
        Название текущего трека либо потока
        :return: str
        """
        ti = self._last_current_track

        title = self._get_title(ti)  # Fixme: CC27

        return title

    @property
    def artist(self) -> str or None:
        """
        Имя исполнителя трека
        :return: строка либо None, если информация отсутствует
        """
        return self._last_current_track.get("artist", None)

    @property
    def album(self) -> str or None:
        """
        Название альбома трека
        :return: строка либо None, если информация отсутствует
        """
        return self._last_current_track.get("album", None)

    @property
    def elapsed(self) -> float:
        """
        Позиция проигрывания трека. Истекшее время с начала проигрывания трека в секундах.
        :return: float
        """
        return self._last_status.get("elapsed", -1.0)

    @property
    def duration(self) -> float:
        """
        Длина трека текущего трека в секундах
        :return: float, -1.0 = бесконечный трек/стрим
        """
        return self._last_current_track.get("time", -1.0)

    @_execute_if_enabled
    @_lost_checker
    def set_volume(self, value: int) -> Actuator.ExecutionResult:
        """
        Установить новое значение громкости в диапазоне от 0 до 100
        :param value: значаение громкости
        :return: Actuator.ExecutionResult
        """
        if value < 0 or value > 100:
            raise ValueError()

        with self._connection():
            self._con_instance.setvol()

        return Actuator.ExecutionResult.OK

    @_execute_if_enabled
    @_lost_checker
    def play(self) -> Actuator.ExecutionResult:
        with self._connection():
            self._con_instance.play()

        return Actuator.ExecutionResult.OK

    @_execute_if_enabled
    @_lost_checker
    def stop(self) -> Actuator.ExecutionResult:
        with self._connection():
            self._con_instance.stop()

        return Actuator.ExecutionResult.OK

    @_execute_if_enabled
    @_lost_checker
    def pause(self) -> Actuator.ExecutionResult:
        with self._connection():
            self._con_instance.pause()

        return Actuator.ExecutionResult.OK

    @_execute_if_enabled
    @_lost_checker
    def next(self) -> Actuator.ExecutionResult:
        with self._connection():
            try:
                self._con_instance.next()
            except mpd.CommandError:  # Треки нельзя переключать тогда, когда плеер MPD остановлен
                return self.ExecutionResult.IGNORED_BAD_STATE

    @_execute_if_enabled
    @_lost_checker
    def prev(self) -> Actuator.ExecutionResult:
        with self._connection():
            try:
                self._con_instance.previous()
            except mpd.CommandError:  # Треки нельзя переключать тогда, когда плеер MPD остановлен
                return self.ExecutionResult.IGNORED_BAD_STATE

    @_execute_if_enabled
    @_lost_checker
    def seek(self, track_pos: float) -> Actuator.ExecutionResult:
        """
        Прокрутить текущий трек к указанной позиции
        :param track_pos: позиция в треке
        :return: Actuator.ExecutionResult
        """
        with self._connection():
            try:
                self._con_instance.seekcur(track_pos)
            except mpd.CommandError:  # Треки нельзя переключать тогда, когда плеер MPD остановлен
                return self.ExecutionResult.IGNORED_BAD_STATE


class MPDPlayerFactory(ThingFactory):
    @staticmethod
    def build(con_instance, con_params: dict, metadata: dict=None) -> MPDPlayer:
        return MPDPlayer(con_instance, con_params, metadata)


ThingRegistry.register_factory(
    "player", MPDClientConnection, MPDPlayerFactory()
)
