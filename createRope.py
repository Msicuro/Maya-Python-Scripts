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


def setPositionPercentage(curve, curve_bind_joints, locators):
    joint_percentage_values = {}
    curve_shape = cmds.listRelatives(curve, shape=True)[0]

    # Get the max arc length value of the curve
    arc_len = cmds.createNode('arcLengthDimension', name='temp_delete_arcLen')
    arc_len_translate = cmds.listRelatives(arc_len, parent=True)[0]

    cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.nurbsGeometry'.format(arc_len))
    cmds.connectAttr('{}.maxValue'.format(curve_shape), '{}.uParamValue'.format(arc_len))

    total_length = cmds.getAttr('{}.arcLength'.format(arc_len))

    # Get the final percentage value on the curve for each joint and save to the dictionary
    for i in range(len(curve_bind_joints)):
        #Create a temp transform node and move it to the joint position
        temp_transform = cmds.createNode('transform', name='temp_delete_transform')
        cmds.delete(cmds.parentConstraint(curve_bind_joints[i], temp_transform))

        # Create the arcLength and nearestPoint nodes and set/connect the appropriate attributes
        temp_nearest_point = cmds.createNode('nearestPointOnCurve')
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.inputCurve'.format(temp_nearest_point))
        cmds.connectAttr('{}.translate'.format(temp_transform), '{}.inPosition'.format(temp_nearest_point))

        temp_arc_len = cmds.createNode('arcLengthDimension')
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.nurbsGeometry'.format(temp_arc_len))
        cmds.connectAttr('{}.parameter'.format(temp_nearest_point), '{}.uParamValue'.format(temp_arc_len))
        final_arc = cmds.getAttr('{}.arcLength'.format(temp_arc_len))

        percentage_value = final_arc/total_length

        #Save the percentage value of the corresponding joint to the dictionary
        joint_percentage_values[curve_bind_joints[i]] = percentage_value

        cmds.delete(temp_transform)
        cmds.delete(temp_nearest_point)
        cmds.delete(temp_arc_len)

    return joint_percentage_values

def attachToMotionPath(joint_percentage_values, curve, curve_bind_joints):
    """
    Attaches a motion path node to the curve joints using the percentage value from setPositionPercentage()
    """
    curve_shape = cmds.listRelatives(curve, shape=True)[0]
    motion_paths = []

    # Iterate through each joint and attach the motion path node with the corresponding percentage value as the uValue
    for i in range(len(curve_bind_joints)):
        motion_paths.append(cmds.createNode('motionPath', name='{}_motionPath'.format(curve_bind_joints[i])))
        cmds.setAttr('{}.fractionMode'.format(motion_paths[i]), True)
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.geometryPath'.format(motion_paths[i]))
        cmds.setAttr('{}.uValue'.format(motion_paths[i]), joint_percentage_values[i])

        cmds.connectAttr('{}.allCoordinates'.format(motion_paths[i]), '{}.translate'.format(curve_bind_joints[i]))