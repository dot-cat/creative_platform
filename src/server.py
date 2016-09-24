#!/usr/bin/env python

import signal
import sys
import logging
import time

logging.basicConfig(level=logging.DEBUG)

from controller import Controller


def signal_handler(signal, frame):
    print('You pressed Ctrl+C - or killed me with -2')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    controller = Controller()

    time.sleep(100)
    signal.pause()
