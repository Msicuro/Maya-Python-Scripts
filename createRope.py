from maya import cmds as cmds

def selectSpans(verts_in_span):
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

        joints.append(centerJoint())
        cmds.select(clear=True)

    return joints, spans

# TODO: Create locator function with joints from selectSpans() as the position points
def addLocators(joints):
    pass

# TODO: Create curve function with joints from selectionSpans as the position points and skin to control joints
def createCurve(control_joints, joints):
    pass

def selectAllVerts():
    selection = cmds.ls(selection=True)
    shape_node = cmds.listRelatives(selection, s=True)[0]
    all_vertices = cmds.ls('{}.vtx[*]'.format(shape_node), fl=True)

    return all_vertices


def centerJoint():
    """
    Will create a joint based on the center of the current selection.
    :return jnt - string:
    """
    sel = cmds.ls(sl=1, fl=1)
    pos = [cmds.xform(x, q=1, ws=1, bb=1) for x in sel]
    val = len(pos)
    pos = [sum(e) for e in zip(*pos)]
    pos = [e/val for e in pos]
    cmds.select(cl=1)
    jnt = cmds.joint(p=((pos[0]+pos[3])/2, (pos[1] + pos[4])/2, (pos[2]+pos[5])/2))
    cmds.select(sel, r=1)
    return jnt