import logging

from dpl.core.things import Thing, ThingRegistry, ThingFactory

logger = logging.getLogger(__name__)


def get_thing_by_params(con_instance, con_params, metadata) -> Thing or None:
    item_type = metadata["type"]

    factory = ThingRegistry.resolve_factory(
        item_type,
        type(con_instance),
        None
    )  # type: ThingFactory

    if factory is None:
        if ThingRegistry.has_type(item_type):
            logger.warning("Unsupported connection: %s", con_instance)
        else:
            logger.warning("Unknown type of object: %s", item_type)
        return None
    else:
        return factory.build(con_instance, con_params, metadata)
