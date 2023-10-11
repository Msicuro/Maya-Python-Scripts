import pymel.core as pm
from PySide2 import QtCore, QtWidgets, QtGui

# Get the top group of the referenced rig and save the prefix without "RN"
ref_node = pm.ls(type="reference")[0]
clean_ref_name = "{}_".format(str(ref_node).replace("RN", ""))

# Duplicate the reference rig group and remove the reference node prefix from the hierarchy
top_ref_group = ref_node.nodes()[0]
export_group = pm.duplicate(top_ref_group)
pm.rename(export_group, "{}".format(str(export_group).replace("1", "")))

root1 = pm.ls(sl=1)
joint_children1 = root1[0].listRelatives(ad=1, type='joint')
joint_children1.insert(0, root1[0])

root2 = pm.ls(sl=1)
joint_children2 = root2[0].listRelatives(ad=1, type='joint')
joint_children2.insert(0, root2[0])


for i in range(len(joint_children1)):
    pm.copyKey(str(joint_children1[i]))
    pm.pasteKey(str(joint_children2[i]))

class copyKeysUI(QtWidgets.QDialog):
    def __init__(self):
        super(copyKeysUI, self).__init__()

        self.setWindowTitle("Copy Skeleton Keys")
        # self.rope = RopeUI()

        self.buildUI()
        #self-populateUI()

    def buildUI(self):
        parent_layout = QtWidgets.QVBoxLayout(self)



