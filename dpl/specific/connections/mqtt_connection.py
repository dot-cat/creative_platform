import paho.mqtt.client as mqtt
import logging

from dpl.core.connections import (
    Connection,
    ConnectionFactory,
    ConnectionRegistry
)


class MQTTClientConnection(Connection):
    def __init__(self, *args, **kwargs):
        self.__mqtt_instance = mqtt.Client(*args, **kwargs)  # type: mqtt.Client
        self.__state = self.States.DISABLED  # type: Connection.States

        self.__mqtt_instance.on_disconnect = self.__on_disconnect  # type: callable
        self.__mqtt_instance.on_connect = self.__on_connect  # type: callable

        self.__host = None
        self.__port = None
        self.__keepalive = None
        self.__bind_address = None
        self.__up_params_set = False

    @property
    def underlying(self):
        return self.__mqtt_instance

    def set_connect_params(self, host, port=1883, keepalive=60, bind_address=""):
        self.__host = host
        self.__port = port
        self.__keepalive = keepalive
        self.__bind_address = bind_address
        self.__up_params_set = True

    def connect(self):
        if self.__up_params_set:
            self.__mqtt_instance.connect_async(
                host=self.__host,
                port=self.__port,
                keepalive=self.__keepalive,
                bind_address=self.__bind_address
            )
            self.__state = self.States.CONNECTING
        else:
            raise ValueError("Unable to bring this connection connect: "
                             "call set_connect_params method first")

    def disconnect(self):
        self.__state = self.States.DISABLED
        self.__mqtt_instance.disconnect()

    @property
    def state(self):
        raise NotImplementedError

    def __on_disconnect(self, client, userdata, rc):
        if self.__state == self.States.CONNECTED:
            self.__state = self.States.CONNECTING

    def __on_connect(self, client, userdata, rc):
        self.__state = self.States.CONNECTED


class MQTTClientConnectionFactory(ConnectionFactory):
    @staticmethod
    def build(config: dict):
        con = MQTTClientConnection(
            **config["init_params"]
        )

        con.set_connect_params(
            **config["con_params"]
        )

        return con


ConnectionRegistry.register_factory(
    "mqtt_client",
    MQTTClientConnectionFactory()
)
