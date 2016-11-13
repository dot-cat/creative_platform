import unittest
from copy import copy

from messages.message_pattern import MessagePattern

valid_message_pattern_params = {
    "type": "button",
    "source_list": ["B1", "B2"],
    "event_list": ["pressed"]
}


class TestMessagePatternInit(unittest.TestCase):
    def test_normal_init(self):
        mp = MessagePattern(
            **valid_message_pattern_params
        )

    def test_init_not_iterable_sources(self):
        invalid_params = copy(valid_message_pattern_params)

        invalid_params["source_list"] = None

        with self.assertRaisesRegex(ValueError, "source_list must be iterable"):
            mp = MessagePattern(
                **invalid_params
            )

    def test_init_not_iterable_events(self):
        invalid_params = copy(valid_message_pattern_params)

        invalid_params["event_list"] = None

        with self.assertRaisesRegex(ValueError, "event_list must be iterable"):
            mp = MessagePattern(
                **invalid_params
            )

    def test_init_empty_sources(self):
        invalid_params = copy(valid_message_pattern_params)

        invalid_params["source_list"] = []

        with self.assertRaisesRegex(ValueError, "source_list can't be empty"):
            mp = MessagePattern(
                **invalid_params
            )

    def test_init_empty_events(self):
        invalid_params = copy(valid_message_pattern_params)

        invalid_params["event_list"] = []

        with self.assertRaisesRegex(ValueError, "event_list can't be empty"):
            mp = MessagePattern(
                **invalid_params
            )

if __name__ == '__main__':
    unittest.main()
