import pymel.core as pm

def get_influence_objects_for_mesh(mesh):
	skin = pm.listHistory(mesh, type="skinCluster")[0]
	influences = skin.influenceObjects()
	return influences

curr = pm.selected()
clothing_joints = get_influence_objects_for_mesh(curr)
pm.select(clothing_joints)