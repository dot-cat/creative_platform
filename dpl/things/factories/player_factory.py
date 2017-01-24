from dpl.things.specific.players.mpd_player import (
    MPDPlayer,
    MPDClientConnection,
    AbsPlayer
)


def get_player_by_params(con_instance, con_params, metadata=None) -> AbsPlayer:
    if isinstance(con_instance, MPDClientConnection):
        return MPDPlayer(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Player for specified connection is missing")
