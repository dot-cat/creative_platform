from controllable_objects.specific.shift_reg.trigger import Trigger, ShiftRegWrapper


def get_trigger_by_params(con_instance, con_params):
    if isinstance(con_instance, ShiftRegWrapper):
        return Trigger(con_instance, con_params)

    else:
        raise ValueError("Implementation of Trigger for specified connection is missing")