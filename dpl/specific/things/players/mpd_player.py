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

from dpl.core.things import ThingFactory, ThingRegistry
from dpl.core.things import Player
from dpl.specific.connections.mpd_client import MPDClientConnection


class MPDPlayer(Player):
    def __init__(self, con_instance: MPDClientConnection, con_params=None, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    @contextlib.contextmanager
    def connection(self):
        try:
            self.con_instance.reconnect()
            yield
        finally:
            self.con_instance.disconnect()

    @classmethod
    def __mpd_state_to_self_state(cls, mpd_state: str) -> Player.States:
        if mpd_state == "play":
            return cls.States.playing
        elif mpd_state == "stop":
            return cls.States.stopped
        elif mpd_state == "pause":
            return cls.States.paused
        else:
            logging.warning("Unknown state of MPD player: %s", mpd_state)
            return cls.States.undefined

    def get_state(self):
        try:
            with self.connection():
                status = self.con_instance.status()
        except ConnectionRefusedError:
            return MPDPlayer.States.undefined

        return self.__mpd_state_to_self_state(status["state"])

    def play(self) -> None:  # CC15
        with self.connection():
            self.con_instance.play()

    def stop(self) -> None:  # CC15
        with self.connection():
            self.con_instance.stop()

    def pause(self) -> None:  # CC15
        with self.connection():
            self.con_instance.pause()

    def next(self) -> None:  # CC15
        with self.connection():
            self.con_instance.next()

    def prev(self) -> None:  # CC15
        with self.connection():
            self.con_instance.previous()

    def get_current_track(self) -> dict:  # CC16
        try:
            with self.connection():
                return self.con_instance.currentsong()  # CC 17
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
