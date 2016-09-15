from controllable_objects.specific.shift_reg.slider import Slider, ShiftRegBuffered


def get_slider_by_params(con_instance, con_params):
    if isinstance(con_instance, ShiftRegBuffered):
        return Slider(con_instance, con_params)

    else:
        raise ValueError("Implementation of Slider for specified connection is missing")
