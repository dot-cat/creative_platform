import unittest
import time

from dpl.controllable_objects.specific.players.mpd_player import MPDPlayer
from dpl.connections.mpd_client import MPDClientConnection


@unittest.skip("Not implemented, mocking needed")
class TestMPDClient(unittest.TestCase):
    def test_all(self):
        connection = MPDClientConnection("localhost", 6600)
        player = MPDPlayer(connection)

        player.stop()

        time.sleep(10)

        player.play()
