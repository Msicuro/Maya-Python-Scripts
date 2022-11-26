from maya import cmds

"""

"""

def createHierarchy(geometry=cmds.ls(selection=True), name=str(cmds.ls(selection=True)[0])):

    main = cmds.group(empty=True, n='{}_Group'.format(name))
    world = cmds.group(empty=True, n="{}_World_Group".format(name))
    ctrl = cmds.group(empty=True, n="{}_Ctrl_Group".format(name))
    rig = cmds.group(empty=True, n="{}_Rig_Group".format(name))
    bind = cmds.group(empty=True, n="{}_Bind_Group".format(name))
    noxform = cmds.group(empty=True, n="{}_noXform_Group".format(name))
    scale = cmds.group(empty=True, n="{}_Scale_Reader_Group".format(name))
    geo = cmds.group(empty=True, n="{}_Geo_Group".format(name))

    trs = cmds.circle(c=[0,0,0], nr=[0,1,0], sw=360, r=3, d=3, ut=0, tol=0.01, s=8, ch=1, n="{}_TRS_CTRL".format(name))
    offset = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1.5, d=3, ut=0, tol=0.01, s=8, ch=1, n="{}_Offset_CTRL".format(name))


    # Parent the specific component groups to the main group
    cmds.parent(world, main)
    cmds.parent(rig, main)
    cmds.parent(geo, main)
    cmds.parent(bind, main)

    # Parent and move the groups needed for handling controls
    cmds.parent(trs, world)
    cmds.parent(offset, trs)
    # TODO: Determine if this can be a point contstraint or if it needs to stay parent
    cmds.delete(cmds.parentConstraint(geometry, world))
    cmds.parent(ctrl, offset)

    # Parent the no-transforms group and scale constraint
    cmds.parent(noxform, rig)
    cmds.parent(scale, noxform)
    cmds.scaleConstraint(rig, scale)

    # Parent the selected geometry to the geo group
    cmds.parent(geometry, geo)