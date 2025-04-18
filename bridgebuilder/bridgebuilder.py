from maya import cmds as cmds
import create_buffer_groups as buffer
import logging

#################################
##Steps to create a bridge rope##
#################################
# Use selectSpans to create joints at each span of a cylinder
# Select the joints that will be used as the control joints (or select the spans that will be used to map the controls
# Run the createCurve function
# Run setPositionPercentage
# Run attachToMotionPath

# Set up logger config and current level
logging.basicConfig()
logger = logging.getLogger("BridgeBuilder")
logger.setLevel(logging.DEBUG)

def selectSpans(joint_name, verts_in_span=None):
    """
    Creates joints at center of each span of a cylinder using the number of vertices that make up each span
    Args:
        verts_in_span: The number of vertices that make up one edge loop/span (if a constructor node is present on a
        polygon mesh, the subdivisionsAxis attribute will be used)
        joint_name: The preferred name for the newly created joints
    Returns:
        mesh_bind_joints, locators, spans, joint_name, mesh, constructor
    """
    all_verts, mesh, constructor = selectAllVerts()

    shape_node = cmds.listRelatives(mesh, s=True)[0]
    spans = []
    mesh_bind_joints = []

    # Calculate the number of spans
    if cmds.objectType(shape_node, isType="nurbsSurface"):
        # TODO: Test script on nurbsSurfaces and figure out how to deal with the first two spans
        num_of_spans = len(cmds.ls('{}.cv[*][0]'.format(shape_node), fl=True)) - 2
        span_range = len(cmds.ls('{}.cv[*][0]'.format(shape_node), fl=True))
        for i in range(span_range):
            vert_span = cmds.ls('{}.cv[{}][*]'.format(shape_node, i), fl=True)
            cmds.select(vert_span)
            if i <= 9:
                mesh_bind_joints.append(centerJoint(name="{}_BIND_0{}".format(joint_name, i)))
            else:
                mesh_bind_joints.append(centerJoint(name="{}_BIND_{}".format(joint_name, i)))
            cmds.select(clear=True)

    elif cmds.objectType(shape_node, isType="mesh"):
        # If verts_in_span is None, set it to the subdivisionsAxis from the constructor node
        logger.debug("CONSTUCTOR: {}".format(constructor))
        if not verts_in_span:
            verts_in_span = cmds.getAttr("{}.subdivisionsAxis".format(constructor))

        logger.debug("VERTS IN SPAN: {}".format(verts_in_span))
        num_of_spans = int(len(all_verts) / verts_in_span)

        # Select vertices in bulk based on the number of vertices per span and create a joint at the center point before
        # iterating to the next span
        inc = 0
        for i in range(num_of_spans):
            spans.append([])
            for vert in range(verts_in_span):
                spans[i].append(all_verts[inc])
                # cmds.select(all_verts[inc], add=True)
                inc += 1

        for i in range(len(spans)):
            cmds.select(spans[i])
            if i <= 9:
                mesh_bind_joints.append(centerJoint(name="{}_BIND_0{}".format(joint_name, i)))
            else:
                mesh_bind_joints.append(centerJoint(name="{}_BIND_{}".format(joint_name, i)))
            cmds.select(clear=True)

    else:
        raise Exception("Wrong lever! (Lever as in node type, please select a nurbsSurface or mesh)")

    # Create locators to attach above the mesh bind joints
    locators = addLocators(mesh_bind_joints)
    for i in range(len(locators)):
        cmds.parent(mesh_bind_joints[i], locators[i])

    return mesh_bind_joints, locators, spans, joint_name, mesh, constructor


def addLocators(joints, name=""):
    """
    Creates locators at the selected positions based on a list of transforms
    Args:
        joints: Any joints or transforms for locator positions
    Returns:
        locators: A list of names of the created locators
    """
    locators = []
    for i in joints:
        if name == "":
            loc = cmds.spaceLocator(name="{}".format(i).replace("JNT", "LOC"))
        else:
            loc = cmds.spaceLocator(name="{}_LOC".format(name))
        logger.debug("i: {}".format(i))
        logger.debug("LOC: {}".format(loc))
        cmds.delete(cmds.pointConstraint(i, loc))
        locators.append(loc[0])

    return locators


def createCurve(name=""):
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
        zero = cmds.group(empty=True, n="{}_ZERO_GRP".format(i))
        cmds.delete(cmds.parentConstraint(i, zero)[0])
        cmds.parent(i, zero)

    # Create the curve with CVs at the positions of the control joints
    curve = cmds.curve(point=positions, n="{}_CRV".format(name))

    return curve, positions, control_joints

def selectAllVerts():
    """
    Lists and returns all vertices on the selected mesh or nurbsSurface
    Returns:
        all_vertices: A list of the vertices collected
        selection: The selected mesh
        constructor_node: The constructor node of the mesh
    """
    selection = cmds.ls(selection=True)
    shape_node = cmds.listRelatives(selection, s=True)[0]
    constructor_node = cmds.listHistory(selection)[1]

    if cmds.objectType(shape_node, isType="nurbsSurface"):
        logger.info("Selecting nurbs CVs")
        all_vertices = cmds.ls('{}.cv[*][*]'.format(shape_node), fl=True)
    elif cmds.objectType(shape_node, isType="mesh"):
        logger.info("Selecting mesh Vertices")
        all_vertices = cmds.ls('{}.vtx[*]'.format(shape_node), fl=True)
    else:
        raise Exception("Wrong lever! (Lever as in node type, please select a nurbsSurface or mesh)")

    return all_vertices, selection, constructor_node


def centerJoint(name):
    """
    Creates a joint at the center of the current selection(s).
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
    # Divide the updated positions by 2 to get the final position (center of the bounding box of all the selected objects put together)
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

def attachToMotionPath(joint_percentage_values, curve, locators, ctrl_joints=None, rope_type="main", rotation=False):
    """
    Attaches a motion path node to the locators above each mesh joint using the percentage value from the
    setPositionPercentage function
    Args:
        joint_percentage_values: The percentage values of transforms along the curve taken from setPositionPercentage()
        curve: The base curve
        locators: The locators parented above the joints skinned to the mesh
        ctrl_joints: The control joints to re-orient to match the bind joints/locators
    Returns:
        motion_paths: List of motion path nodes created
    """
    curve_shape = cmds.listRelatives(curve, shapes=True)[0]
    motion_paths = []
    logger.debug("ROPE TYPE: {}".format(rope_type))

    # Iterate through each joint and attach the motion path node with the corresponding percentage value as the uValue
    for i in range(len(locators)):
        motion_paths.append(cmds.createNode('motionPath', name='{}_motionPath'.format(locators[i])))
        cmds.setAttr('{}.fractionMode'.format(motion_paths[i]), True)
        cmds.connectAttr('{}.worldSpace[0]'.format(curve_shape), '{}.geometryPath'.format(motion_paths[i]))
        cmds.setAttr('{}.uValue'.format(motion_paths[i]), joint_percentage_values[locators[i]])

        cmds.connectAttr('{}.allCoordinates'.format(motion_paths[i]), '{}.translate'.format(locators[i]))

        if rotation:
            cmds.setAttr('{}.follow'.format(motion_paths[i]), True)
            cmds.setAttr('{}.worldUpVectorX'.format(motion_paths[i]), 0)
            cmds.setAttr('{}.worldUpVectorY'.format(motion_paths[i]), 1)
            cmds.setAttr('{}.worldUpVectorZ'.format(motion_paths[i]), 0)

            cmds.setAttr('{}.frontAxis'.format(motion_paths[i]), 0)
            cmds.setAttr('{}.upAxis'.format(motion_paths[i]), 1)

            cmds.connectAttr('{}.rotateX'.format(motion_paths[i]), '{}.rotateX'.format(locators[i]))
            cmds.connectAttr('{}.rotateY'.format(motion_paths[i]), '{}.rotateY'.format(locators[i]))
            cmds.connectAttr('{}.rotateZ'.format(motion_paths[i]), '{}.rotateZ'.format(locators[i]))

            #Iterate through the control joints and match the transforms of the appropriate locator only if it's a main
            if "Main" in rope_type:
                for c in range(len(ctrl_joints)):
                    logger.debug(ctrl_joints)
                    ctrl_zero_group = cmds.listRelatives(ctrl_joints[c], parent=True)[0]

                    #Get the value right before "_CTRL" in the control joint and compare to the locator index
                    ctrl_index = ctrl_joints[c].find("_CTRL")
                    ctrl_index = ctrl_joints[c][ctrl_index-2:ctrl_index]
                    logger.debug("CTRL INDEX: {}".format(ctrl_index))

                    locator_index = locators[i].find("_LOC")
                    locator_index = locators[i][locator_index - 2:locator_index]
                    logger.debug("LOCATOR INDEX: {}".format(i))

                    if ctrl_index == locator_index:
                        cmds.delete(cmds.parentConstraint(locators[i], ctrl_zero_group))
                        logger.debug("SUCCESS")
                        break
                    else:
                        logger.debug("FAIL")

            elif "Support" in rope_type:
                #Create a new locator to use as the world up object for the motion path only on the top joint
                if i == 0:
                    #Get the first control joint to snap the new locator to
                    first_joint = []
                    first_joint.append(ctrl_joints[0])

                    # Create the new locator to use as the Up Object for the motion paths
                    up_object = addLocators(first_joint)
                    logger.debug("UP OBJECT: {}".format(up_object))

                    # Rename the new locator

                    #Move the new locator inward by 1 unit
                    up_object_pos = cmds.getAttr("{}.translateX".format(up_object[0]))

                    if "left" in str(up_object[0]):
                        cmds.move(up_object_pos - 2, up_object[0], x=True)
                    elif "right" in str(up_object[0]):
                        cmds.move(up_object_pos + 2, up_object[0], x=True)
                    else:
                        raise Exception(
                            "CTRL joint must have 'left' or 'right' in the name to determine up object position")

                    #Connect worldUp object on the motion path to the up_object locator
                    cmds.setAttr('{}.worldUpType'.format(motion_paths[i]), 1)
                    cmds.connectAttr("{}.worldMatrix[0]".format(up_object[0]), "{}.worldUpMatrix".format(motion_paths[i]))

                    # Parent the up object locator to the ik joint parent group
                    cmds.parent(up_object[i], first_joint[0])
                    #cmds.pointConstraint(first_joint[0], up_object[i])

                # Connect worldUp object on the motion path to the up_object locator
                else:
                    # Connect worldUp object on the motion path to the up_object locator
                    cmds.setAttr('{}.worldUpType'.format(motion_paths[i]), 1)
                    cmds.connectAttr("{}.worldMatrix[0]".format(up_object[0]), "{}.worldUpMatrix".format(motion_paths[i]))
                    #cmds.pointConstraint(first_joint[0], up_object[i])
            else:
                raise Exception("Please select rope type 'main' or 'support'")

    return motion_paths

def createSupports(bind_joints, locators):
    '''
    Creates a curve and connects motionPath and Nearest Point on Curve nodes for a vertical cylinder
    Args:
        locators: The locators from the selectSpans function corresponding to the bind joint positions

    '''
    # Run selectSpans separately

    # Select the outer and middle bind joints for the control joints using the bind joints created from selectSpans
    cmds.select(clear=True)
    ctrl_joints = []
    cmds.select(locators[0])
    cmds.select(locators[(len(locators) / 2) - 1], add=True)
    cmds.select(locators[len(locators) / 2], add=True)
    cmds.select(locators[(len(locators) / 2) + 1], add=True)
    cmds.select(locators[-1], add=True)

    logger.debug('Selections: {}'.format(cmds.ls(selection=True)))
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
        logger.debug('Motion Path[{}]: {}'.format(i, motion_paths[i]))
        logger.debug('Param: {}'.format(param))
        cmds.setAttr('{}.uValue'.format(motion_paths[i]), param)

        # Connect the motionPaths Coordinates and rotate attributes into the locator
        cmds.connectAttr('{}.allCoordinates'.format(motion_paths[i]), '{}.translate'.format(locators[i]))
        cmds.connectAttr('{}.rotateX'.format(motion_paths[i]), '{}.rotateX'.format(locators[i]))
        cmds.connectAttr('{}.rotateY'.format(motion_paths[i]), '{}.rotateY'.format(locators[i]))
        cmds.connectAttr('{}.rotateZ'.format(motion_paths[i]), '{}.rotateZ'.format(locators[i]))


def setupNPOCPath(curve, locators):
    '''
    Separately create the Nearest Point on Curve and motionPath connections
    Args:
        curve: The control curve
        locators: The locators from the selectSpans function corresponding to the bind joint positions

    '''
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
        logger.debug('Motion Path[{}]: {}'.format(i, motion_paths[i]))
        logger.debug('Param: {}'.format(param))
        cmds.setAttr('{}.uValue'.format(motion_paths[i]), param)

        # Connect the motionPaths Coordinates attribute into the locator
        cmds.connectAttr('{}.allCoordinates'.format(motion_paths[i]), '{}.translate'.format(locators[i]))
def buildSupport(ctrl_joints, increment=0):
    '''
    Creates 5 joints with an IK chain to control tethered cylinders
    Args:
        ctrl_joints: The control joints from the createCurve function

    Returns:
        new_ik_handle, new_ik_ctrl, new_pvector: The IK handle, IK control and pole vector for the cylinder
    '''
    # Identify the updated name, IK joints and the middle index to isolate the center joint
    new_base_name = str(ctrl_joints[0]).split("0")[0]

    ik_joints = ctrl_joints[::2]
    middle_index = int(len(ik_joints) / 2)

    # Save the existing parent groups for the IK joints to delete
    middle_joint_group = cmds.ls(ik_joints[middle_index], long=True)[0].split('|')[1:-1][0]
    last_joint_group = cmds.ls(ik_joints[-1], long=True)[0].split('|')[1:-1][0]

    cmds.parent(ik_joints[-1], ik_joints[middle_index])
    cmds.parent(ik_joints[middle_index], ik_joints[0])

    # Delete the previous joint groups
    cmds.delete(middle_joint_group)
    cmds.delete(last_joint_group)
    # Orient the ik joints
    cmds.joint(ik_joints[0], edit=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)
    # Add an IK handle to the first, middle and last control joints (these should be in the same hierarchy)
    new_ik_handle = cmds.ikHandle(n="{}{}_ikHandle".format(new_base_name, increment), sj=ik_joints[0], ee=ik_joints[-1])
    #Create a control for the ik handle
    new_ik_ctrl = cmds.circle(n="{}{}_ikCTRL".format(new_base_name, increment), c=(0,0,0), nr=(0, 1, 0), sw=360, r= 1, d=3, ut=0, tol=0.01, s=8, ch=1)
    cmds.delete(cmds.pointConstraint(new_ik_handle, new_ik_ctrl))
    ik_ctrl_group = buffer.createTwo(new_ik_ctrl[0])
    cmds.select("{}.cv[*]".format(new_ik_ctrl[0]))
    cmds.rotate(90, 0, 0, r=1, os=1, fo=1)

    cmds.parent(new_ik_handle[0], new_ik_ctrl[0])

    # Point constrain the remaining group nodes above the two joints (which should be separate) to the appropriate ik control joints
    mid_joints = ctrl_joints[1::2]
    for i, v in enumerate(mid_joints):
        top_parent = cmds.ls(v, long=True)[0].split('|')[1:-1][0]
        cmds.pointConstraint(ik_joints[i], ik_joints[i + 1], top_parent)

    # Create a curve control (or any control shape) and move it to the center control joint and away
    new_pvector = cmds.curve(n="{}{}_pVector".format(new_base_name, increment), d=1, p=[(0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    cmds.delete(cmds.pointConstraint(ik_joints[1], new_pvector))

    pv_position = cmds.getAttr("{}.translateX".format(new_pvector))
    if "left" in str(ik_joints[0]):
        cmds.move(pv_position+6, new_pvector, x=True)
    elif "right" in str(ik_joints[0]):
        cmds.move(pv_position-6, new_pvector, x=True)
    else:
        raise Exception("IK joints must have 'left' or 'right' in the name to determine pole vector position")

    pvector_group = buffer.createTwo(new_pvector)
    # Create a pole vector constraint with the ik handle and a point constraint with the ik control
    cmds.poleVectorConstraint(new_pvector, new_ik_handle[0])
    cmds.pointConstraint(new_ik_ctrl, pvector_group, mo=1)

    #Group the pole vector and ik control
    ik_group = cmds.group(pvector_group, n="{}{}_IK_GRP".format(new_base_name,increment))
    cmds.parent(ik_ctrl_group, ik_group)

    return new_ik_handle, new_ik_ctrl, new_pvector


def bindPlanks(boards):
    '''
    Create joints and buffer groups on either side of a poly cube
    Args:
        boards: A list of poly cube meshes
    Returns:
        left_joints, right_joints: Lists of the left and right joints on either sides of the poly cubes
    '''

    left_joints = []
    right_joints = []
    for i in boards:
        # Select all verts on the board
        cmds.select(i)
        all_vertices, selection = selectAllVerts()

        # Select just the left side verts and create a joint
        cmds.select(all_vertices[1::2])
        left_joint = centerJoint("left_" + str(i))
        left_joints.append(left_joint)

        # Create a group for the left side joint
        left_grp = cmds.group(empty=True, n=left_joint + "_BUFF_GRP")
        cmds.delete(cmds.parentConstraint(left_joint, left_grp))
        cmds.parent(left_joint, left_grp)

        # Select just the right side verts and create a joint
        cmds.select(all_vertices[0::2])
        right_joint = centerJoint("right_" + str(i))
        right_joints.append(right_joint)

        # Create a group for the right side joint
        right_grp = cmds.group(empty=True, n=right_joint + "_BUFF_GRP")
        cmds.delete(cmds.parentConstraint(right_joint, right_grp))
        cmds.parent(right_joint, right_grp)

        # Bind the joints
        cmds.select(left_joint, right_joint, i)
        cmds.SmoothBindSkin()

    return left_joints, right_joints

def createControls(ctrl_joints, name):
    '''
    Creates vertical nurbs circles at given points
    Args:
        ctrl_joints: A list of joints corresponding to the new controls
        name: Intended name for the controls

    Returns:
        controls: A list of created controls
    '''

    controls = []
    for i, v in enumerate(ctrl_joints):
        new_circle = cmds.circle(n="{}_{}_CTRL".format(name, i), c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=1)
        cmds.delete(cmds.parentConstraint(v, new_circle[0]))

        cmds.select("{}.cv[*]".format(new_circle[0]))
        cmds.rotate(0, 0, 90, r=1, os=1, fo=1)
        cmds.scale(1.2, 1.2, 1.2, r=1, os=1)

        buffer.createTwo(new_circle[0])
        controls.append(new_circle[0])

    return controls

def bindJoints(mesh, joints, rope_type=""):
    '''
    Bind joints to a single mesh with the rope "type" taken into account
    Args:
        mesh: The mesh to bind to
        joints: A list of joints to bind
        rope_type: The type of rope (with the bridge functionality in mind). If "Support", joint values will be set
        to 1 on each CV to avoid uneven weights
    '''
    cmds.select(clear=True)
    cmds.select(joints, mesh)
    skin_cluster = cmds.skinCluster()[0]
    if "Support" in rope_type:
        logger.debug("CV: {}".format("{}.cv[-1]".format(mesh)))
        logger.debug("CTRL JOINT: {}".format(joints[-1]))
        cmds.skinPercent(skin_cluster, "{}.cv[{}]".format(mesh, len(joints)), transformValue = [joints[-1], 1])


def addStretchyIK(ctrl_joints):
    '''
    Create stretchy IK using the side lengths of the triangle made up of the IK joints
    Args:
        ctrl_joints: List of control joints
    '''
    # Get the upperarm length
    upperarm_length = cmds.getAttr("{}.translateX".format(ctrl_joints[2]))
    # Get the lowerarm length
    lowerarm_length = cmds.getAttr("{}.translateX".format(ctrl_joints[4]))

    # Add the shoulder and elbow joint length for the arm length
    arm_length = upperarm_length+lowerarm_length

    # Create locators at the shoulder and wrist
    arm_joints = [ctrl_joints[0], ctrl_joints[-1]]
    stretch_locators = addLocators(arm_joints, name=arm_joints[0].replace("CTRL", "STRCH").replace("JNT_", ""))

    # Create distance node for arm distance (distance between the shoulder and wrist)
    arm_distance = cmds.shadingNode("distanceBetween", asUtility=True)
    # Connect top and bottom locators to Distance node
    cmds.connectAttr("{}.worldPosition[0]".format(cmds.listRelatives(stretch_locators[0], s=True)[0]), "{}.point1".format(arm_distance))
    cmds.connectAttr("{}.worldPosition[0]".format(cmds.listRelatives(stretch_locators[1], s=True)[0]), "{}.point2".format(arm_distance))

    # Create a multiplyDivide node (set to divide) and name it distance_divider
    arm_divider = cmds.shadingNode("multiplyDivide", asUtility=True, n="distance_divider")
    cmds.setAttr("{}.operation".format(arm_divider), 2)
        # Set input2 of the divider to the arm length
    cmds.setAttr("{}.input2X".format(arm_divider), upperarm_length+lowerarm_length)
        # Plug the distance from the arm distance dimension node into the input1 of the divider
    cmds.connectAttr("{}.distance".format(arm_distance), "{}.input1X".format(arm_divider))

    # Create two multDoubleLiner nodes, one for the upperarm and one for the lowerarm
    upperarm_multiplier = cmds.shadingNode("multDoubleLinear", asUtility=True)
    lowerarm_multiplier = cmds.shadingNode("multDoubleLinear", asUtility=True)
        # Plug the output from the divider into input1 of both multDoubleLinear nodes
    cmds.connectAttr("{}.outputX".format(arm_divider), "{}.input1".format(upperarm_multiplier))
    cmds.connectAttr("{}.outputX".format(arm_divider), "{}.input1".format(lowerarm_multiplier))
        # Set input2 of the upparm multipler to the length of the upperarm (elbow X value)
    cmds.setAttr("{}.input2".format(upperarm_multiplier), upperarm_length)
        # Set input2 of the lowerarm multipler to the length of the lowerarm (wrist X value)
    cmds.setAttr("{}.input2".format(lowerarm_multiplier), lowerarm_length)

    # Create two condition nodes, one for the upperarm and one for the lowerarm
    upperarm_condition = cmds.shadingNode("condition", asUtility=True)
    lowerarm_condition = cmds.shadingNode("condition", asUtility=True)
    cmds.setAttr("{}.operation".format(upperarm_condition), 2)
    cmds.setAttr("{}.operation".format(lowerarm_condition), 2)
        # Plug the distance from the arm distance into FirstTerm of both condition nodes
    cmds.connectAttr("{}.distance".format(arm_distance), "{}.firstTerm".format(upperarm_condition))
    cmds.connectAttr("{}.distance".format(arm_distance), "{}.firstTerm".format(lowerarm_condition))
        # Plug the output from the arm multipliers into ColorIfTrue of both condition nodes
    cmds.connectAttr("{}.output".format(upperarm_multiplier), "{}.colorIfTrueR".format(upperarm_condition))
    cmds.connectAttr("{}.output".format(lowerarm_multiplier), "{}.colorIfTrueR".format(lowerarm_condition))
        # Set the SecondTerm of the both condition nodes to the arm length
    cmds.setAttr("{}.secondTerm".format(upperarm_condition), upperarm_length+lowerarm_length)
    cmds.setAttr("{}.secondTerm".format(lowerarm_condition), upperarm_length+lowerarm_length)
        # Set the ColorIfFalse of the upperarm condition node to the length of the upperarm (elbow X)
    cmds.setAttr("{}.colorIfFalseR".format(upperarm_condition), upperarm_length)
        # Set the ColorIfFalse of the lowerarm condition node to the length of the lowerarm (wrist X)
    cmds.setAttr("{}.colorIfFalseR".format(lowerarm_condition), lowerarm_length)
    # Plug the OutColorR of the upperarm condition node into the translateX of the elbow joint
    cmds.connectAttr("{}.outColorR".format(upperarm_condition), "{}.translateX".format(ctrl_joints[2]))
    # Plug the OutColorR of the lowerarm condition node into the translateX of the wrist joint
    cmds.connectAttr("{}.outColorR".format(lowerarm_condition), "{}.translateX".format(ctrl_joints[4]))

    # Get the ik handle and the ik control before re-parenting
    ik_handle = cmds.listConnections(ctrl_joints[0], type="ikHandle")
    ik_ctrl = cmds.listRelatives(ik_handle, parent=True)
    # Parent the IK handle under the 2nd locator
    cmds.parent(ik_handle, stretch_locators[-1])
    # Parent the 2nd locator under the IK control
    cmds.parent(stretch_locators[-1], ik_ctrl)

    # Get the parent group of the ik control joints
    ctrl_joint_parent_grp = cmds.listRelatives(ctrl_joints[0], parent=True)
    # Parent the 1st locator under the ik joint parent group
    cmds.parent(stretch_locators[0], ctrl_joint_parent_grp)