import pymel.core as pm

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

def createHierarchy(geometry=pm.ls(selection=True)):

    main = pm.group(empty=True, n='{}_Group'.format(str(geometry[0])))
    world = pm.group(empty=True, n="World_Group")
    rig = pm.group(empty=True, n="Rig_Group")
    noxform = pm.group(empty=True, n="noXform_Group")
    scale = pm.group(empty=True, n="Scale_Reader_Group")
    geo = pm.group(empty=True, n="Geo_Group")

    trs = pm.circle(c=[0,0,0], nr=[0,1,0], sw=360, r=3, d=3, ut=0, tol=0.01, s=8, ch=1, n="TRS_CTRL")
    offset = pm.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1.5, d=3, ut=0, tol=0.01, s=8, ch=1, n="Offset_CTRL")

    pm.parent(world, main)
    pm.parent(trs, world)
    pm.parent(offset, trs)
    pm.parent(rig, offset)
    pm.parent(noxform, rig)
    pm.parent(scale, noxform)
    pm.parent(geo, rig)

    pm.scaleConstraint(rig, scale)

    pm.parent(geometry, geo)