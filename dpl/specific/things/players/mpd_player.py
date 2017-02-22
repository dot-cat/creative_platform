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

    @property
    def extended_info(self):
        """
        Возвращает расширенную информацию о состоянии объекта
        :return: словарь с информацией либо None
        """
        try:
            with self._connection():
                return self._con_instance.status()
        except ConnectionRefusedError:
            return None

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

    def get_current_track(self) -> dict:  # CC16
        warnings.warn(
            "This method will be removed in v0.4. "
            "All needed information is moved to extended_info attribute",
            PendingDeprecationWarning
        )
        try:
            with self._connection():
                return self._con_instance.currentsong()  # CC 17
        except ConnectionRefusedError:
            return {
                "name": "undefined"
            }  # CC 18


class MPDPlayerFactory(ThingFactory):
    @staticmethod
    def build(con_instance, con_params: dict, metadata: dict=None) -> MPDPlayer:
        return MPDPlayer(con_instance, con_params, metadata)


ThingRegistry.register_factory(
    "player", MPDClientConnection, MPDPlayerFactory()
)
