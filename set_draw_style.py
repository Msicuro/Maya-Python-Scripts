import pymel.core as pm

def setDrawStyle(index=0):
    '''
    Sets the draw style of the selected object, typically used on joints
    Args:
        index: index corresponding to the drawStyle attribute options in the Attribute Editor
                For joints:
                    0 = Bone
                    1 = Multi-Child as Box
                    2 = None
                    3 = Joint
    '''

    sel = pm.selected()

    for i in sel:
        if type(pm.getAttr("{}.drawStyle".format(i))) == int:
            pm.setAttr("{}.drawStyle".format(i), index)