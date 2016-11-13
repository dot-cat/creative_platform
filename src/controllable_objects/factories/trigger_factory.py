from controllable_objects.specific.shift_reg.trigger import AbsTrigger, Trigger, ShiftRegBuffered
from controllable_objects.specific.serial.trigger import Trigger as SerTrigger
import serial


def get_trigger_by_params(con_instance, con_params, metadata=None) -> AbsTrigger:
    if isinstance(con_instance, ShiftRegBuffered):
        return Trigger(con_instance, con_params["sr_pin"], metadata)

    elif isinstance(con_instance, serial.Serial):
        return SerTrigger(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Trigger for specified connection is missing")
