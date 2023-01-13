import maya.cmds as cmds

def createThree(selection = cmds.ls(sl=True)):

	for each in selection:
		grp1 = cmds.group(empty=True, n = each + "_NULL_GRP")
		cmds.delete(cmds.parentConstraint(each, grp1)[0])
		grp2 = cmds.group(empty=True, n = each + "_ZERO_GRP")
		cmds.delete(cmds.parentConstraint(each, grp2)[0])
		grp3 = cmds.group(empty=True, n = each + "_BUFF_GRP")
		cmds.delete(cmds.parentConstraint(each, grp3)[0])
		cmds.parent(each, grp3)
		cmds.parent(grp3, grp2)
		cmds.parent(grp2, grp1)
		cmds.makeIdentity(each, t=1, r=1,s=1, apply=True)

def createTwo(selection = cmds.ls(sl=True)):
	if type(selection) is list:
		for each in selection:
			grp1 = cmds.group(empty=True, n=each + "_NULL_GRP")
			cmds.delete(cmds.parentConstraint(each, grp1))
			grp2 = cmds.group(empty=True, n=each + "_BUFF_GRP")
			cmds.delete(cmds.parentConstraint(each, grp2))
			cmds.parent(each, grp2)
			cmds.parent(grp2, grp1)
			#cmds.makeIdentity(each, t=1, r=1, s=1, apply=True)
	else:
		grp1 = cmds.group(empty=True, n=selection + "_NULL_GRP")
		cmds.delete(cmds.parentConstraint(selection, grp1))
		grp2 = cmds.group(empty=True, n=selection + "_BUFF_GRP")
		cmds.delete(cmds.parentConstraint(selection, grp2))
		cmds.parent(selection, grp2)
		cmds.parent(grp2, grp1)
		#cmds.makeIdentity(selection, t=1, r=1, s=1, apply=True)