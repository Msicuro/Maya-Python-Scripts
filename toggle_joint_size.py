import pymel.core as pm
from itertools import cycle

display_sizes = [0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 1.0, 1.5]
myIterator = cycle(display_sizes)

def setJointSize():
    new_display = next(myIterator)
    pm.jointDisplayScale(new_display)