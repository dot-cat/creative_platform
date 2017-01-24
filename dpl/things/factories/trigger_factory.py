from dpl.things.specific.shift_reg.trigger import AbsTrigger, Trigger, ShiftRegBuffered


def get_trigger_by_params(con_instance, con_params, metadata=None) -> AbsTrigger:
    if isinstance(con_instance, ShiftRegBuffered):
        return Trigger(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Trigger for specified connection is missing")
