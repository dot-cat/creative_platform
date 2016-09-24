#!/usr/bin/env python

import signal
import logging

logging.basicConfig(level=logging.DEBUG)

from controller import Controller


def signal_handler(signal, frame):
    print('You pressed Ctrl+C - or killed me with -2')
    controller.stop_api()


signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    controller = Controller()

    signal.pause()
