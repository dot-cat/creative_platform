import logging

from dpl.core.connections import ConnectionRegistry
from dpl.core.connections import Connection


def get_connection_by_config(config: dict) -> Connection:
    factory = ConnectionRegistry.resolve_factory(config["con_type"])

    if factory is None:
        logging.warning("Unknown connection: %s", config)
        return None
    else:
        return factory.build(config)
