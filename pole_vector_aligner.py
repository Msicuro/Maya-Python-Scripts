from maya import cmds
from maya.api import OpenMaya
from functools import partial


def get_pos_as_mvector(node):
    """Get a transform position as an MVector instance.

    Args:
        node (str): Name of transform.

    Returns:
        MVector: Position of given transform node.
    """
    pos = cmds.xform(node, query=True, translation=True, worldSpace=True)
    return OpenMaya.MVector(pos)


def place_pole_vector_ctrl(pv_ctrl, start, mid, end, shift_factor=2):
    """Position and orient the given poleVector control to avoid popping.

    Args:
        pv_ctrl (str): Name of transform to be used as poleVector.
        start (str): Name of start joint.
        mid (str): Name of mid joint.
        end (str): Name of end joint.
        shift_factor (float): How far ctrl should be moved away from mid joint.
    """
    # Find mid-point between start and end joint
    start_pos = get_pos_as_mvector(start)
    end_pos = get_pos_as_mvector(end)
    center_pos = (start_pos + end_pos) / 2

    # Use vector from mid-point to mid joint...
    mid_pos = get_pos_as_mvector(mid)
    offset = mid_pos - center_pos
    # ...to place the poleVector control
    pv_pos = center_pos + offset * shift_factor
    cmds.xform(pv_ctrl, translation=pv_pos, worldSpace=True)

    # Orient ctrl so that the XY-plane coincides with plane of joint chain.
    aim_constraint = cmds.aimConstraint(
        mid,
        pv_ctrl,
        aimVector=(-1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="object",
        worldUpObject=start,
    )
    cmds.delete(aim_constraint)


def createWindow():
    window = cmds.window(title="Align Pole Vector")

    cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 250)])

    cmds.text(label='IK Start Joint')
    start_field = cmds.textField("start")
    cmds.button(label="<<", command=partial(updateTextBox, start_field))

    cmds.text(label='IK Mid Joint')
    mid_field = cmds.textField("mid")
    cmds.button(label="<<", command=partial(updateTextBox, mid_field))

    cmds.text(label='IK End Joint')
    end_field = cmds.textField("end")
    cmds.button(label="<<", command=partial(updateTextBox, end_field))

    cmds.text(label='Polve Vector CTRL')
    pvector_field = cmds.textField("pvctrl")
    cmds.button(label="<<", command=partial(updateTextBox, pvector_field))

    cmds.button(label="Run", width=380, command=runPVCommand)

    cmds.showWindow()


def updateTextBox(textfield, *args):
    selection = cmds.ls(sl=1)[0]
    add = cmds.textField(textfield, edit=True, text=selection)


def runPVCommand(*args):
    print(cmds.textField("start", q=1))

    place_pole_vector_ctrl(
        start=cmds.textField("start", q=1, text=1),
        mid=cmds.textField("mid", q=1, text=1),
        end=cmds.textField("end", q=1, text=1),
        pv_ctrl=cmds.textField("pvctrl", q=1, text=1),
        shift_factor=2,
    )


createWindow()