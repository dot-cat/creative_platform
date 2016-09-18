#!/usr/bin/env python

from time import sleep
import logging

from controller import Controller


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    controller = Controller()

    try:
        controller.listener_cli.listener_thread.join()
    except KeyboardInterrupt:
        pass

    print('Exited')
    pass
