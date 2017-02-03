from dpl.core.things import Player

from dpl.specific.things.players import (
    MPDPlayer,
    MPDClientConnection
)


def get_player_by_params(con_instance, con_params, metadata=None) -> Player:
    if isinstance(con_instance, MPDClientConnection):
        return MPDPlayer(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Player for specified connection is missing")
