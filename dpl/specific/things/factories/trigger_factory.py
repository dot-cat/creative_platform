from dpl.specific.things.shift_reg.trigger import Trigger, ShiftRegTrigger, ShiftRegBuffered


def get_trigger_by_params(con_instance, con_params, metadata=None) -> Trigger:
    if isinstance(con_instance, ShiftRegBuffered):
        return ShiftRegTrigger(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Trigger for specified connection is missing")
