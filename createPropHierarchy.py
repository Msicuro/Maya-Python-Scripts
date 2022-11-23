from may import cmds

"""
1. Create the following groups:
- "{geo_name}_Group"
- World_Group
- Rig_Group
- No Xform
- Scale Reader_Group
- Geo_Group

2. Create the following controls
- TRS_CTRL
- Offset_CTRL

3. Scale constrain the Scale Reader to the Rig group

4. Parent geometry under the geo group
"""

def createHierarchy(geometry=cmds.ls(selection=True)):

    main = cmds.group(empty=True, n='{}_Group'.format(str(geometry[0])))
    world = cmds.group(empty=True, n="World_Group")
    rig = cmds.group(empty=True, n="Rig_Group")
    noxform = cmds.group(empty=True, n="noXform_Group")
    scale = cmds.group(empty=True, n="Scale_Reader_Group")
    geo = cmds.group(empty=True, n="Geo_Group")

    trs = cmds.circle(c=[0,0,0], nr=[0,1,0], sw=360, r=3, d=3, ut=0, tol=0.01, s=8, ch=1, n="TRS_CTRL")
    offset = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1.5, d=3, ut=0, tol=0.01, s=8, ch=1, n="Offset_CTRL")

    cmds.parent(world, main)
    cmds.parent(trs, world)
    cmds.parent(offset, trs)
    cmds.parent(rig, offset)
    cmds.parent(noxform, rig)
    cmds.parent(scale, noxform)
    cmds.parent(geo, rig)

    cmds.scaleConstraint(rig, scale)

    cmds.delete(cmds.parentConstraint(geometry, main))
    cmds.parent(geometry, geo)