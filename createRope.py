from maya import cmds as cmds

#################################
##Steps to create a bridge rope##
#################################
# Use selectSpans to create joints at each span of a cylinder
# Select the joints that will be used as the control joints (or select the spans that will be used to map the controls
# Run the createCurve function
# Run setPositionPercentage
# Run attachToMotionPath

def selectSpans(verts_in_span, joint_name):
    """
    Creates joints at center of each span of a cylinder using the number of vertices that make up each span
    Args:
        verts_in_span: The number of vertices that make up one span
        joint_name: The preferred name for the newly created joints
    Returns:
        mesh_bind_joints, locators, spans
    """
    all_verts, mesh = selectAllVerts()

    spans = []
    mesh_bind_joints = []
    # Calculate the number of spans on the mesh
    num_of_spans = int(len(all_verts) / verts_in_span)

    # Select vertices in bulk based on the number of vertices per span and create a joint at the center point before
    # iterating to the next span
    inc = 0
    for i in range(num_of_spans):
        spans.append([])
        for vert in range(verts_in_span):
            spans[i].append(all_verts[inc])
            cmds.select(all_verts[inc], add=True)
            inc += 1

        mesh_bind_joints.append(centerJoint(name="{}_BIND_{}".format(joint_name, i)))
        cmds.select(clear=True)

    # Create duplicate joints to use as bind joints for the mesh and bind them
    cmds.select(clear=True)
    cmds.select(mesh_bind_joints, mesh)
    cmds.SmoothBindSkin()

    # Create locators to attach above the mesh bind joints
    locators = addLocators(mesh_bind_joints)
    for i in range(len(locators)):
        cmds.parent(mesh_bind_joints[i], locators[i])

    return mesh_bind_joints, locators, spans


def addLocators(joints):
    """
    Creates locators at the selected positions based on a list of joints (or any selected objects with transforms)
    Args:
        joints: Any joints or transforms for locator positions
    Returns:
        locators: A list of names of the created locators
    """
    locators = []
    for i in joints:
        loc = cmds.spaceLocator(name="{}".format(i).replace("JNT", "LOC"))
        cmds.delete(cmds.pointConstraint(i, loc))
        locators.append(loc[0])

    return locators


def createCurve():
    """
    Creates a curve with points along the selected control joints/transforms along with joints to use as controls
    Returns: curve, positions, control_joints
    """
    control_transforms = cmds.ls(selection=True)
    positions = []
    control_joints = []

    # Iterate through the control transforms and save the positions to use for curve creation
    cmds.select(clear=True)
    for i in control_transforms:
        cmds.select(i)
        control_joints.append(centerJoint(name="{}".format(i.replace("LOC", "CTRL").replace("_BIND",""))))
        positions.append(cmds.xform(i, query=True, translation=True, worldSpace=True))

    # Increase the size of the control joints and create a transform group above them
    for i in control_joints:
        cmds.setAttr("{}.radius".format(i), 1.8)
        zero = cmds.group(empty=True, n="{}".format(i.replace("JNT", "ZERO_GRP")))
        cmds.delete(cmds.parentConstraint(i, zero)[0])
        cmds.parent(i, zero)

    # Create the curve with CVs at the positions of the control joints
    curve = cmds.curve(point=positions)

    # Bind the control joints to the curve
    cmds.select(control_joints, curve)
    cmds.SmoothBindSkin()

    return curve, positions, control_joints

def selectAllVerts():
    """
    Selects and returns all vertices on a mesh
    """
    selection = cmds.ls(selection=True)
    shape_node = cmds.listRelatives(selection, s=True)[0]
    all_vertices = cmds.ls('{}.vtx[*]'.format(shape_node), fl=True)

    return all_vertices, selection


def centerJoint(name):
    """
    Will create a joint based on the center of the current selection(s).
    CREDIT: Script from Rigging Dojo
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


def setPositionPercentage(curve, locators):
    """
    Stores the arcLength for each corresponding joint on the curve into a dictionary
    Args:
        curve:
        locators: The transforms to determine the position on the curve

    Returns:
        locator_percentage_values: A list of the arcLen/percentage values on the curve of each transform
    """
    locator_percentage_values = {}
    curve_shape = cmds.listRelatives(curve, shapes=True)[0]

    # Get the max arc length value of the curve
    arc_len = cmds.createNode('arcLengthDimension', name='temp_delete_arcLen')
    arc_len_transform = cmds.listRelatives(arc_len, parent=True)[0]

    cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.nurbsGeometry'.format(arc_len))
    cmds.connectAttr('{}.maxValue'.format(curve_shape), '{}.uParamValue'.format(arc_len))

    total_length = cmds.getAttr('{}.arcLength'.format(arc_len))

    cmds.delete(arc_len_transform)

    # Get the final percentage value on the curve for each locator and save to the dictionary
    for i in range(len(locators)):
        #Create a temp transform node and move it to the locator position
        temp_transform = cmds.createNode('transform', name='temp_delete_transform')
        cmds.delete(cmds.parentConstraint(locators[i], temp_transform))

        # Create the arcLength and nearestPoint nodes and set/connect the appropriate attributes
        temp_nearest_point = cmds.createNode('nearestPointOnCurve')
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.inputCurve'.format(temp_nearest_point))
        cmds.connectAttr('{}.translate'.format(temp_transform), '{}.inPosition'.format(temp_nearest_point))

        temp_arc_len = cmds.createNode('arcLengthDimension')
        temp_arc_len_transform = cmds.listRelatives(temp_arc_len, parent=True)[0]
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.nurbsGeometry'.format(temp_arc_len))
        cmds.connectAttr('{}.parameter'.format(temp_nearest_point), '{}.uParamValue'.format(temp_arc_len))
        final_arc = cmds.getAttr('{}.arcLength'.format(temp_arc_len))

        percentage_value = final_arc/total_length

        #Save the percentage value of the corresponding locator to the dictionary
        locator_percentage_values[locators[i]] = percentage_value

        cmds.delete(temp_transform)
        cmds.delete(temp_nearest_point)
        cmds.delete(temp_arc_len_transform)

    return locator_percentage_values

def attachToMotionPath(joint_percentage_values, curve, locators):
    """
    Attaches a motion path node to the locators above the mesh joints using the percentage value from setPositionPercentage()
    Args:
        joint_percentage_values: The percentage values of transforms along the curve taken from setPositionPercentage()
        curve: The base curve
        locators: The locators parented above the joints skinned to the mesh
    """
    curve_shape = cmds.listRelatives(curve, shapes=True)[0]
    motion_paths = []

    # Iterate through each joint and attach the motion path node with the corresponding percentage value as the uValue
    for i in range(len(locators)):
        motion_paths.append(cmds.createNode('motionPath', name='{}_motionPath'.format(locators[i])))
        cmds.setAttr('{}.fractionMode'.format(motion_paths[i]), True)
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.geometryPath'.format(motion_paths[i]))
        cmds.setAttr('{}.uValue'.format(motion_paths[i]), joint_percentage_values[locators[i]])

        cmds.connectAttr('{}.allCoordinates'.format(motion_paths[i]), '{}.translate'.format(locators[i]))

    return motion_paths

def createSupports(bind_joints, locators):
    # Run selectSpans separately

    # Select the outer and middle bind joints for the control joints using the bind joints created from selectSpans
    cmds.select(clear=True)
    ctrl_joints = []
    cmds.select(locators[0])
    cmds.select(locators[(len(locators) / 2) - 1], add=True)
    cmds.select(locators[len(locators) / 2], add=True)
    cmds.select(locators[(len(locators) / 2) + 1], add=True)
    cmds.select(locators[-1], add=True)

    print('Selections: {}'.format(cmds.ls(selection=True)))
    # Create the curve with the selected control joints
    curve, positions, ctrl_joints = createCurve()
    cmds.select(clear=True)

    curve_shape = cmds.listRelatives(curve, shapes=True)[0]
    motion_paths = []
    # Create the nPOC and motionPath nodes using the locators created from selectSpans
    for i in range(len(locators)):
        # Create the nPOC node and connect the locators translates to it
        temp_nPOC = cmds.createNode('nearestPointOnCurve')
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.inputCurve'.format(temp_nPOC))
        cmds.connectAttr('{}.translate'.format(locators[i]), '{}.inPosition'.format(temp_nPOC))
        param = cmds.getAttr('{}.parameter'.format(temp_nPOC))
        # Delete the nPOC node to remove its connection from the locator
        cmds.delete(temp_nPOC)

        # Create the motionPath node and connect the parameter value from the nPOC node into it
        motion_paths.append(cmds.createNode('motionPath', name='{}_motionPath'.format(locators[i])))
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.geometryPath'.format(motion_paths[i]))
        print('Motion Path[{}]: {}'.format(i, motion_paths[i]))
        print('Param: {}'.format(param))
        cmds.setAttr('{}.uValue'.format(motion_paths[i]), param)

        # Connect the motionPaths Coordinates attribute into the locator
        cmds.connectAttr('{}.allCoordinates'.format(motion_paths[i]), '{}.translate'.format(locators[i]))

def bindPlanks():
    # Select the vertices on each side of the plank
    # Create a joint in the center on each side
    # Bind the joints to the board
    # Create a Buffer group above the joints
    # Parent constrain the Buffer groups to the corresponding locator on the rope
    pass
