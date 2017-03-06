import threading

import serial

from dpl.core.connections.abs_connection import Connection


class SerialConnection(Connection):
    def __init__(self, *args, **kwargs):
        self._write_lock = threading.Lock()
        self._ser = serial.Serial(*args, **kwargs)

        self._handlers = set()

        self._is_stopped = True
        self._th = None
        self.start_listening()

    def _input_loop(self):
        while not self._is_stopped:
            data = self._ser.readline()
            self._on_received(data)

    def add_receiver(self, handler: callable):
        self._handlers.add(handler)

    def remove_receiver(self, handler: callable):
        self._handlers.remove(handler)

    def _on_received(self, data: bin):
        for h in self._handlers:
            h(data)

    def write(self, data: bin):
        with self._write_lock:
            self._ser.write(data)

    def stop_listening(self):
        if not self._is_stopped:
            self._is_stopped = True
            self._ser.cancel_read()
            self._th.join()

    def start_listening(self):
        if self._is_stopped:
            self._is_stopped = False
            self._th = threading.Thread(target=self._input_loop)
            self._th.start()

    def __del__(self):
        self._ser.close()
