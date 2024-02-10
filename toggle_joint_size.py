import pymel.core as pm
from itertools import cycle

# myIterator = cycle(display_sizes)

def setJointSize():
    '''
    Cycles through joint display sizes
    Returns:

    '''
    # new_display = next(myIterator)
    # pm.jointDisplayScale(new_display)
    display_sizes = [0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 1.0, 1.5]

    current_scale = pm.jointDisplayScale(query=True)

    if current_scale not in display_sizes or current_scale == display_sizes[-1]:
        pm.jointDisplayScale(display_sizes[0])
    else:
        current_scale_index = display_sizes.index(current_scale)
        pm.jointDisplayScale(display_sizes[current_scale_index + 1])