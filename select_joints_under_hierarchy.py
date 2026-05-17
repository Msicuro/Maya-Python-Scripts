import pymel.core as pm

def selectJointsInHierarchy():
    roots = pm.selected()
    children = [i.listRelatives(ad=1, type='joint') for i in roots]

    pm.select(roots)
    pm.select(children, add=True)