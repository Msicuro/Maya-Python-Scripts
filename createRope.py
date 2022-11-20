from maya import cmds as cmds

def selectSpans(verts_in_span, joint_name):
    all_verts = selectAllVerts()

    spans = []
    joints = []
    num_of_spans = int(len(all_verts) / verts_in_span)
    inc = 0

    for i in range(num_of_spans):
        spans.append([])
        for vert in range(verts_in_span):
            spans[i].append(all_verts[inc])
            cmds.select(all_verts[inc], add=True)
            inc += 1

        joints.append(centerJoint(name="{}_{}".format(joint_name, i)))
        cmds.select(clear=True)

    return joints, spans


def addLocators(joints):
    locators = []
    for i in joints:
        loc = cmds.spaceLocator(name="{}".format(i).replace("JNT", "LOC"))
        cmds.delete(cmds.pointConstraint(i, loc))
        locators.append(loc)

    return locators


def createCurve():
    control_joints = cmds.ls(selection=True)
    positions = []
    curve_joints = []

    for i in control_joints:
        curve_joints.append(cmds.duplicate(i, name=i.replace("bind", "CTRL"))[0])
        positions.append(cmds.xform(i, query=True, translation=True, worldSpace=True))

    curve = cmds.curve(point=positions)

    cmds.select(curve_joints, curve)
    cmds.SmoothBindSkin()

    return curve, positions, curve_joints

def selectAllVerts():
    selection = cmds.ls(selection=True)
    shape_node = cmds.listRelatives(selection, s=True)[0]
    all_vertices = cmds.ls('{}.vtx[*]'.format(shape_node), fl=True)

    return all_vertices


def centerJoint(name):
    """
    Will create a joint based on the center of the current selection. CREDIT: Script from Rigging Dojo
    :return jnt - string:
    """
    sel = cmds.ls(sl=1, fl=1)
    # Get the bounding box transforms for the selection(s)
    pos = [cmds.xform(x, q=1, ws=1, bb=1) for x in sel]
    val = len(pos)
    # Add the zipped positions together
    pos = [sum(e) for e in zip(*pos)]
    # Divide the updated position by the total number of selected objects
    pos = [e/val for e in pos]
    cmds.select(cl=1)
    # Divide the updated positions by 2 to get the final position (center of the bounding box of all the selected objects put together?)
    jnt = cmds.joint(p=((pos[0]+pos[3])/2, (pos[1] + pos[4])/2, (pos[2]+pos[5])/2), name="{}_JNT".format(name))
    cmds.select(sel, r=1)
    return jnt

# TODO: Create curveLogic function that connects the curve shape node,
#  locator, and curve bind joints with the needed utility nodes
def curveLogic(curve_shape, locators, curve_bind_joints):
    pass