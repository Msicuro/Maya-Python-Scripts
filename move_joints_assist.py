#### Move skinned joints ####
import pymel.core as pm

# Save all the transform nodes in the scene that have a valid Shape node attached
mesh_transforms = [i for i in pm.ls(type=pm.nt.Transform) if i.getShape()]

# Loop through the transforms with a valid skin cluster attached
# and activate/deactivate moveJointsMode
for i in mesh_transforms:
    if i.history(type="skinCluster"):
        clust = i.history(type="skinCluster")[0]
        pm.skinCluster(clust, edit=True, moveJointsMode=False)

# Delete all bind poses in the scene
poses = pm.ls(type='dagPose')
for i in poses:
    if i.bindPose.get():
        pm.delete(i)

# Create and save a new bind pose on all selected objects (should be joints)
pm.dagPose(selection=True, save=True, bindPose=True)