import unittest
from unittest.mock import Mock
from copy import copy

from events.event_hub import EventHub
from handlers.abs_handler import AbsHandler
from events.message_pattern import MessagePattern
from events.abs_message import Message, time

msg_pattern_button = MessagePattern(
    "button",
    ["B1", "B2"],
    ["pressed"]
)

msg_pattern_player = MessagePattern(
    "player",
    ["PLAY1", "PLAY2", "PLAY100"],
    ["started", "stopped", "paused", "next_track", "prev_track"]
)


def generate_pattern_modification(msg_pattern: MessagePattern, sources=None, events=None):
    if sources is None:
        sources = msg_pattern.sources

    if events is None:
        events = msg_pattern.events

    subpattern = MessagePattern(
        msg_pattern.type,
        sources,
        events
    )

    return subpattern


def generate_sample_msg(msg_pattern: MessagePattern, source_index=0, event_index=0):
    msg = Message(
        msg_pattern.type,
        msg_pattern.sources[source_index],
        msg_pattern.events[event_index],
        time.time(),
        None
    )

    return msg


def generate_test_handler(msg_pattern: MessagePattern):
    handler = Mock(spec_set=AbsHandler)
    handler.get_sensitivity_list.return_value = msg_pattern

    return handler

msg_sample_button = generate_sample_msg(msg_pattern_button)


class TestEventHubInit(unittest.TestCase):
    def test_event_hub_init(self):
        eh = EventHub()
        self.assertEquals(eh.handler_resolver, dict())


class TestEventHubAcceptEventOneHandler(unittest.TestCase):
    def test_handled_one_source(self):
        eh = EventHub()
        handler = generate_test_handler(msg_pattern_button)
        eh.add_handler(handler)

        eh.accept_event(msg_sample_button)

        handler.handle.assert_called_once_with(msg_sample_button)

    def test_handled_different_sources(self):
        eh = EventHub()
        handler = generate_test_handler(msg_pattern_button)
        eh.add_handler(handler)

        for source in msg_pattern_button.sources:
            msg = Message(
                msg_pattern_button.type,
                source,
                msg_pattern_button.events[0],
                time.time(),
                None
            )

            eh.accept_event(msg)
            handler.handle.assert_called_with(msg)

    def test_handled_different_events(self):
        eh = EventHub()
        handler = generate_test_handler(msg_pattern_button)
        eh.add_handler(handler)

        for event in msg_pattern_button.events:
            msg = Message(
                msg_pattern_button.type,
                msg_pattern_button.sources[0],
                event,
                time.time(),
                None
            )

            eh.accept_event(msg)
            handler.handle.assert_called_with(msg)

    def test_not_handled_other_type(self):
        eh = EventHub()

        handler = generate_test_handler(msg_pattern_button)

        eh.add_handler(handler)

        msg_changed = copy(msg_sample_button)
        msg_changed.type = "unknown type"

        eh.accept_event(msg_changed)

        handler.handle.assert_not_called()

    def test_not_handled_other_source(self):
        eh = EventHub()
        handler = generate_test_handler(msg_pattern_button)
        eh.add_handler(handler)

        msg_changed = copy(msg_sample_button)
        msg_changed.source = "B1000000"

        eh.accept_event(msg_changed)

        handler.handle.assert_not_called()

    def test_not_handled_other_event(self):
        eh = EventHub()
        handler = generate_test_handler(msg_pattern_button)
        eh.add_handler(handler)

        msg_changed = copy(msg_sample_button)
        msg_changed.event = "unknown event"

        eh.accept_event(msg_changed)

        handler.handle.assert_not_called()


class TestEventHubAcceptEventSeveralHandlers(unittest.TestCase):
    def test_handled_by_one_handler(self):
        handler_player = generate_test_handler(msg_pattern_player)
        handler_button = generate_test_handler(msg_pattern_button)

        eh = EventHub()
        eh.add_handler(handler_player)
        eh.add_handler(handler_button)

        eh.accept_event(msg_sample_button)

        handler_button.handle.assert_called_once_with(msg_sample_button)
        handler_player.assert_not_called()

    def test_handled_by_another_handler(self):
        handler_player = generate_test_handler(msg_pattern_player)
        handler_button = generate_test_handler(msg_pattern_button)

        msg_sample_player = generate_sample_msg(msg_pattern_player)

        eh = EventHub()
        eh.add_handler(handler_player)
        eh.add_handler(handler_button)

        eh.accept_event(msg_sample_player)

        handler_button.assert_not_called()
        handler_player.handle.assert_called_once_with(msg_sample_player)

    def test_handled_by_both_handlers(self):
        handler_first_player = generate_test_handler(
            generate_pattern_modification(
                msg_pattern_player, sources=[msg_pattern_player.sources[0]]
            )
        )

        handler_all_players = generate_test_handler(msg_pattern_player)

        msg_sample_player = generate_sample_msg(msg_pattern_player)

        eh = EventHub()
        eh.add_handler(handler_first_player)
        eh.add_handler(handler_all_players)

        eh.accept_event(msg_sample_player)

        handler_all_players.handle.assert_called_once_with(msg_sample_player)
        handler_first_player.handle.assert_called_once_with(msg_sample_player)
