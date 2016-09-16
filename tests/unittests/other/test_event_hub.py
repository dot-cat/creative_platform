import unittest

from events.event_hub import EventHub
from handlers.abs_handler import AbsHandler
from events.message_pattern import MessagePattern
from events.abs_message import Message, time


msg_pattern = MessagePattern(
    "button",
    ["B1", "B2"],
    ["pressed"]
)

msg_sample = Message(
    "button",
    "B1",
    "pressed",
    time.time(),
    None
)

handler = AbsHandler(msg_pattern, None)


class TestEventHub(unittest.TestCase):
    def test_event_hub_init(self):
        eh = EventHub()
        self.assertEquals(eh.handler_resolver, dict())

    def test_handler(self):
        eh = EventHub()

        print(msg_sample)

        eh.add_handler(handler)
        eh.accept_event(msg_sample)
