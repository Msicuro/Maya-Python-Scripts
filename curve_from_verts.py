import pymel.core as pm

def curveFromVerts():
    """
    Creates a curve with positions from selected vertices
    """
    if pm.ls(selection=True):
        verts = pm.ls(selection=True)
    else:
        raise RuntimeError("No vertices selected!")

    point_positions = [pm.pointPosition(v, w=True) for v in verts]

    pm.curve(p=point_positions)