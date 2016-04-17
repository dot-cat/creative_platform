from .outputs import Outputs

AllOutputs = Outputs()

AllOutputs.open_door('Open first door')

print(AllOutputs.current_state)

AllOutputs.turn_light('room 1', AllOutputs.ON)

print(AllOutputs.current_state)

AllOutputs.turn_light('room 2', AllOutputs.OFF)

print(AllOutputs.current_state)

AllOutputs.turn_light('room 1', AllOutputs.ON)

print(AllOutputs.current_state)

AllOutputs.turn_light('room 1', AllOutputs.OFF)

print(AllOutputs.current_state)
