import pymel.core as pm

def curveFromVerts():
    #TODO: Change function to create a curve base on positions from anything
    """
    Creates a curve with positions from selected vertices
    """
    if pm.ls(selection=True):
        verts = pm.ls(selection=True)
    else:
        raise RuntimeError("No vertices selected!")

    # point_positions = [pm.pointPosition(v, w=True) for v in verts]

    point_positions = []
    for v in verts:
        if isinstance(v, pm.MeshVertex):
            point_positions.append(pm.pointPosition(v, w=True))
        else:
            raise RuntimeError('{} is not a vertice! Please only select vertices'.format(v))

    print ("They're all vertices!")
    pm.curve(p=point_positions)