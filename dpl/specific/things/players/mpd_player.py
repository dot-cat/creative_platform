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

from dpl.core.things import ThingFactory, ThingRegistry, Actuator
from dpl.core.things import Player
from dpl.specific.connections.mpd_client import MPDClientConnection

logger = logging.getLogger(__name__)


class MPDPlayer(Player):
    def __init__(self, con_instance: MPDClientConnection, con_params=None, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

        self._is_con_failed = False
        self._is_enabled = True
        self._state = self.States.undefined
        self._extended_info = None

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
    def extended_info(self) -> dict or None:
        return self._extended_info

    @property
    def is_available(self) -> bool:
        """
        Доступность объекта для использования
        :return: True - доступен, False - недоступен
        """
        return self._is_enabled and not self._is_con_failed

    def _state_updater(self):
        ci = self._con_instance  # type: MPDClientConnection

        while self._is_enabled:
            ci.idle()
            self._extended_info = ci.status()
            self._state = self.__mpd_state_to_self_state(self._extended_info["state"])
            

class MPDPlayerFactory(ThingFactory):
    @staticmethod
    def build(con_instance, con_params: dict, metadata: dict=None) -> MPDPlayer:
        return MPDPlayer(con_instance, con_params, metadata)


ThingRegistry.register_factory(
    "player", MPDClientConnection, MPDPlayerFactory()
)
