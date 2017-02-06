import time
import unittest

from dpl.specific.connections.mpd_client import MPDClientConnection
from dpl.specific.things.players import MPDPlayer


@unittest.skip("Not implemented, mocking needed")
class TestMPDClient(unittest.TestCase):
    def test_all(self):
        connection = MPDClientConnection("localhost", 6600)
        player = MPDPlayer(connection)

        player.stop()

        time.sleep(10)

        player.play()
