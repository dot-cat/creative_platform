##############################################################################################
# FIXME List:
# CC15 - Consider Change 15
#   Выбрасывает исключение в случае неудачного подключения. Вопрос: отсавить как есть или 
#   перехватывать?
# CC16 - Consider Change 16
#   Может возвращать None вместо "undefined"?
# CC17 - Consider Change 17
#   Отдавать только строку (атрибут "name") или полный словарь с информацией от текущем треке?
# CC18 - Consider Change 18
#   Отдавать только {"name": "name here"} или полный словарь ( с ключами file, id, name, pos)?
##############################################################################################


import contextlib
import logging
import time
import warnings

from dpl.core.things import ThingFactory, ThingRegistry
from dpl.core.things import Actuator
from dpl.core.things import Player
from dpl.specific.connections.mpd_client import MPDClientConnection

import mpd

logger = logging.getLogger(__name__)


class MPDPlayer(Player):
    def __init__(self, con_instance: MPDClientConnection, con_params=None, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)
        self._is_enabled = True
        self._last_seen = time.time()

    @contextlib.contextmanager
    def _connection(self):
        try:
            self._con_instance.reconnect()
            yield
        finally:
            self._con_instance.disconnect()

    @classmethod
    def __mpd_state_to_self_state(cls, mpd_state: str) -> Player.States:
        if mpd_state == "play":
            return cls.States.playing
        elif mpd_state == "stop":
            return cls.States.stopped
        elif mpd_state == "pause":
            return cls.States.paused
        else:
            logger.warning("Unknown state of MPD player: %s", mpd_state)
            return cls.States.undefined

    @property
    def state(self):
        try:
            with self._connection():
                status = self._con_instance.status()
        except ConnectionRefusedError:
            return MPDPlayer.States.undefined

        return self.__mpd_state_to_self_state(status["state"])

    @property
    def is_available(self) -> bool:  # FIXME: Изменить реализацию, загрушка
        """
        Доступность объекта для использования
        :return: True - доступен, False - недоступен
        """
        return self._is_enabled

    def _update_last_seen(self):
        self._last_seen = time.time()

    @property
    def last_seen(self) -> float:  # Fixme: CC23
        """
        Возвращает время, когда объект был доступен в последний раз
        :return: float, UNIX time
        """
        if self._is_enabled:
            self._update_last_seen()

        return self._last_seen

    def disable(self) -> None:
        """
        Отключает объект, останавливает обновление состояния и
        делает его неактивным
        :return: None
        """
        self._is_enabled = False

        if self.on_avail_update:
            self.on_avail_update(self)

    def enable(self) -> None:
        """
        Включает объект, запускает обновление состояние и делает
        его активным
        :return: None
        """
        self._is_enabled = True

        if self.on_avail_update:
            self.on_avail_update(self)

    def _get_status(self) -> dict:
        warnings.warn(
            "This method is a temporary solution and must be removed  "
            "or changed before release",
            DeprecationWarning
        )

        try:
            with self._connection():
                return self._con_instance.status()  # CC 17
        except ConnectionRefusedError:
            return {}  # CC 18

    @property
    def volume(self) -> int:  # Fixme: CC26
        """
        Текущий уровень громкости в процентах
        :return: int, -1 = n/a
        """
        status = self._get_status()
        return status.get("volume", -1)

    @property
    def source(self) -> str:
        """
        Имя текущего файла либо URI потока
        :return: str
        """
        ti = self._get_current_track_info()
        return ti.get("file", None)  # None = error

    @property
    def title(self) -> str:
        """
        Название текущего трека либо потока
        :return: str
        """
        ti = self._get_current_track_info()
        return ti.get(
            "title",
            ti.get(  # if there is no title -> try to get stream name
                "name", None
            )
        )  # None = error

    @property
    def artist(self) -> str or None:
        """
        Имя исполнителя трека
        :return: строка либо None, если информация отсутствует
        """
        ti = self._get_current_track_info()
        return ti.get("artist", None)

    @property
    def album(self) -> str or None:
        """
        Название альбома трека
        :return: строка либо None, если информация отсутствует
        """
        ti = self._get_current_track_info()
        return ti.get("album", None)

    @property
    def elapsed(self) -> float:
        """
        Позиция проигрывания трека. Истекшее время с начала проигрывания трека в секундах.
        :return: float
        """
        ti = self._get_status()
        return ti.get("elapsed", -1.0)

    @property
    def duration(self) -> float:
        """
        Длина трека текущего трека в секундах
        :return: float, -1.0 = бесконечный трек/стрим
        """
        ti = self._get_current_track_info()
        return ti.get("time", -1.0)

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

    def play(self) -> Actuator.ExecutionResult:  # CC15
        with self._connection():
            self._con_instance.play()

        return Actuator.ExecutionResult.OK

    def stop(self) -> Actuator.ExecutionResult:  # CC15
        with self._connection():
            self._con_instance.stop()

        return Actuator.ExecutionResult.OK

    def pause(self) -> Actuator.ExecutionResult:  # CC15
        with self._connection():
            self._con_instance.pause()

        return Actuator.ExecutionResult.OK

    def next(self) -> Actuator.ExecutionResult:  # CC15
        with self._connection():
            try:
                self._con_instance.next()
            except mpd.CommandError:  # Треки нельзя переключать тогда, когда плеер MPD остановлен
                return self.ExecutionResult.IGNORED_BAD_STATE

    def prev(self) -> Actuator.ExecutionResult:  # CC15
        with self._connection():
            try:
                self._con_instance.previous()
            except mpd.CommandError:  # Треки нельзя переключать тогда, когда плеер MPD остановлен
                return self.ExecutionResult.IGNORED_BAD_STATE

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

    def _get_current_track_info(self) -> dict:
        warnings.warn(
            "This method is a temporary solution and must be removed  "
            "or changed before release",
            DeprecationWarning
        )

        try:
            with self._connection():
                return self._con_instance.currentsong()  # CC 17
        except ConnectionRefusedError:
            return dict()  # CC 18

    def get_current_track(self) -> dict:  # CC16
        warnings.warn(
            "This method will be removed in v0.4. "
            "All needed information is moved to corresponding properties",
            PendingDeprecationWarning
        )
        return self._get_current_track_info()


class MPDPlayerFactory(ThingFactory):
    @staticmethod
    def build(con_instance, con_params: dict, metadata: dict=None) -> MPDPlayer:
        return MPDPlayer(con_instance, con_params, metadata)


ThingRegistry.register_factory(
    "player", MPDClientConnection, MPDPlayerFactory()
)
