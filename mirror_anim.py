import pymel.core as pm

## Mirror IK foot controls ##
# Save controls
left_ik_foot_ctrl = pm.selected()[0]
right_ik_foot_ctrl = pm.PyNode(left_ik_foot_ctrl.name().replace("L_", "R_"))

# Save left control translates and non-zero rig attributes
left_translates = left_ik_foot_ctrl.getTranslation(space="object")

left_attrs = left_ik_foot_ctrl.listAttr(keyable=True, inUse=True)[6:]
left_non_zero_attrs = [i for i in left_attrs if i.get() != 0]
left_non_zero_attrs_values = [i.get() for i in left_non_zero_attrs]

# Save right control translates and non-zero rig attributes
right_translates = right_ik_foot_ctrl.getTranslation(space="object")

right_attrs = right_ik_foot_ctrl.listAttr(keyable=True, inUse=True)[6:]
right_non_zero_attrs = [i for i in right_attrs if i.get() != 0]
right_non_zero_attrs_values = [i.get() for i in right_non_zero_attrs]

# Swap translation values on left & right controls
left_ik_foot_ctrl.setTranslation(right_translates)
right_ik_foot_ctrl.setTranslation(left_translates)

# Swap rig attributes on left & right controls
for i, v in enumerate(left_non_zero_attrs):
    v.set(right_non_zero_attrs_values[i])
for i, v in enumerate(right_non_zero_attrs):
    v.set(left_non_zero_attrs_values[i])


## Mirror FK controls
left_fk_ctrl = pm.selected()[0]
# Assumes L_ and R_ naming convention
right_fk_ctrl = pm.PyNode(left_fk_ctrl.name().replace("L_", "R_"))

left_rotations = left_fk_ctrl.getRotation(space="object")
right_rotations = right_fk_ctrl.getRotation(space="object")

left_fk_ctrl.setRotation(right_rotations, space="object")
right_fk_ctrl.setRotation(left_rotations, space="object")