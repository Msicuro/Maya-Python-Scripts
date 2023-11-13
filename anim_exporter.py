import pymel.core as pm

root1 = pm.ls(sl=1)
joint_children1 = root1[0].listRelatives(ad=1, type='joint')
joint_children1.insert(0, root1[0])

root2 = pm.ls(sl=1)
joint_children2 = root2[0].listRelatives(ad=1, type='joint')
joint_children2.insert(0, root2[0])


for i in range(len(joint_children1)):
    pm.copyKey(str(joint_children1[i]))
    pm.pasteKey(str(joint_children2[i]))