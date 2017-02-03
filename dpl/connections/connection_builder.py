import logging

from dpl.connections.abs_connection import ConnectionFactory, Connection
import dpl.connections.all_enabled  # FIXME: CC20

from dpl.connections.connection_registry import ConnectionRegistry


def get_connection_by_config(config: dict) -> Connection:
    factory = ConnectionRegistry.resolve_factory(config["con_type"])

    if factory is None:
        logging.warning("Unknown connection: %s", config)
        return None
    else:
        return factory.build(config)
