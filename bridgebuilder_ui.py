from PySide2 import QtWidgets, QtCore, QtGui
import bridgeBuilder
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

def getMayaMainWindow():
    window = omui.MQtUtil_mainWindow()
    pointer = wrapInstance(long(window), QtWidgets.QMainWindow)
    return pointer

class RopeUI(QtWidgets.QDialog):
    def __init__(self):
        parent = getMayaMainWindow()
        super(RopeUI, self).__init__(parent=parent)

        self.setWindowTitle("Rope Builder")
        # self.rope = RopeUI()

        self.buildUI()
        #self-populateUI()

    def buildUI(self):
        # Create parent layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # Create the name section layout and add it to the main layout
        # Name Section
        name_widget = QtWidgets.QWidget()
        name_layout = QtWidgets.QGridLayout(name_widget)
        main_layout.addWidget(name_widget)

        # Create the elements in the name section and add them to the section
        name_label = QtWidgets.QLabel("Name")
        self.name_combo = QtWidgets.QComboBox()
        self.name_combo.addItem("left")
        self.name_combo.addItem("right")

        self.name_line = QtWidgets.QLineEdit()
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItem("Main Rope")
        self.type_combo.addItem("Support")

        name_layout.addWidget(name_label, 0, 0)
        name_layout.addWidget(self.name_combo, 0, 1)
        name_layout.addWidget(self.name_line, 0, 2)
        name_layout.addWidget(self.type_combo, 0, 3)

        # selectSpans Section
        select_spans_widget = QtWidgets.QWidget()
        select_spans_layout = QtWidgets.QGridLayout(select_spans_widget)
        main_layout.addWidget(select_spans_widget)

        self.select_checkbox = QtWidgets.QCheckBox()
        self.select_checkbox.setText("Create Joints Along Cylinder")
        #self.select_checkbox.setFont(QtGui.QFont( 12))

        select_spans_layout.addWidget(self.select_checkbox, 0, 0)

        select_verts_text = QtWidgets.QLabel("Subdivision Axis: ")
        #select_verts_text.setAlignment(QtCore.Qt.Alignment(1))
        #select_verts_text.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        select_verts_text.setFont(QtGui.QFont("Arial", 7))
        print("Size Policy: {}".format(dir(QtWidgets.QSizePolicy())))


        # createCurve Section
        curve_widget = QtWidgets.QWidget()
        curve_layout = QtWidgets.QGridLayout(curve_widget)
        main_layout.addWidget(curve_widget)

        self.curve_checkbox = QtWidgets.QCheckBox()
        self.curve_checkbox.setText("Create Control Curve")

        curve_layout.addWidget(self.curve_checkbox, 0, 0)

        # Position Percentage section
        position_percent_widget = QtWidgets.QWidget()
        position_percent_layout = QtWidgets.QGridLayout(position_percent_widget)
        main_layout.addWidget(position_percent_widget)

        self.position_percent_checkbox = QtWidgets.QCheckBox()
        self.position_percent_checkbox.setText("Set Locator Curve Position Percentage")

        position_percent_layout.addWidget(self.position_percent_checkbox, 0, 0)

        # Attach to Motion Path section
        motion_path_widget = QtWidgets.QWidget()
        motion_path_layout = QtWidgets.QGridLayout(motion_path_widget)
        motion_path_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        main_layout.addWidget(motion_path_widget)

        self.motion_path_checkbox = QtWidgets.QCheckBox()
        self.motion_path_checkbox.setText("Attach Locators to Motion Path")
        self.rotations_checkbox = QtWidgets.QCheckBox()
        self.rotations_checkbox.setText("Include Motion Path Rotations")

        motion_path_layout.addWidget(self.motion_path_checkbox, 0, 0)
        motion_path_layout.addWidget(self.rotations_checkbox, 1, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)


        # Bind section
        bind_widget = QtWidgets.QWidget()
        bind_layout = QtWidgets.QGridLayout(bind_widget)
        main_layout.addWidget(bind_widget)

        self.bind_curve_checkbox = QtWidgets.QCheckBox()
        self.bind_curve_checkbox.setText("Bind Curve to Control Joints")
        self.bind_mesh_checkbox = QtWidgets.QCheckBox()
        self.bind_mesh_checkbox.setText("Bind Mesh to Locator Joints")

        bind_layout.addWidget(self.bind_curve_checkbox, 0, 0)
        bind_layout.addWidget(self.bind_mesh_checkbox, 1, 0)

        # Run Button
        run_button = QtWidgets.QPushButton("Run")
        main_layout.addWidget(run_button)

        # Set font size for function widgets
        main_font_size = 18
        select_spans_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        curve_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        position_percent_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        self.motion_path_checkbox.setStyleSheet("font-size: {}px".format(main_font_size))
        self.rotations_checkbox.setStyleSheet("font-size: 12px")
        bind_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        run_button.setStyleSheet("font-size: {}px".format(main_font_size))

        # Test button functionality
        # rope_stats = run_button.clicked.connect(partial(bridgeBuilder.selectSpans("{}_{}_{}".format(
        #     self.name_combo.currentText(),
        #     self.name_line.text(),
        #     self.type_combo.currentText()))))

        # Test selectSpans functionality
        run_button.clicked.connect(self.runButtonFunctions)

    def runSelectSpans(self):
        self.bind_joints,\
        self.locators,\
        self.spans,\
        self.name,\
        self.mesh,\
        self.constructor = bridgeBuilder.selectSpans("{}_{}_{}".format(self.name_combo.currentText(),
                                                                       self.name_line.text(),
                                                                       self.type_combo.currentText()
        ))
        return self.bind_joints, self.locators, self.spans, self.name, self.mesh, self.constructor

    def runCreateCurve(self):
        self.curv, \
        self.positions, \
        self.ctrl_joints = bridgeBuilder.createCurve("{}_{}_{}".format(self.name_combo.currentText(),
                                                                       self.name_line.text(),
                                                                       self.type_combo.currentText()))
        return self.curv, self.positions, self.ctrl_joints

    def runSetPositionPercentage(self):
        self.joint_percentages = bridgeBuilder.setPositionPercentage(self.curv, self.locators)
        return self.joint_percentages

    def runAttachMotionPaths(self):
        self.motion_paths = bridgeBuilder.attachToMotionPath(joint_percentage_values=self.joint_percentages,
                                                             curve=self.curv, locators=self.locators,
                                                             ctrl_joints=self.ctrl_joints,
                                                             rope_type=self.type_combo.currentText(),
                                                             rotation=self.rotations_checkbox.isChecked())
        print("ROPE TYPE: {}".format(self.type_combo.currentText()))
        return self.motion_paths
    def runBindJoints(self):
        # Save the skin cluster for the curve and mesh if they exist
        curve_skin_cluster = [i for i in cmds.listHistory(self.curv) if cmds.objectType(i, isType="skinCluster")]
        mesh_skin_cluster = [i for i in cmds.listHistory(self.mesh) if cmds.objectType(i, isType="skinCluster")]

        # Check if the object being skinned already has a skin cluster before binding
        if self.bind_curve_checkbox.isChecked() and not self.bind_mesh_checkbox.isChecked():
            if not curve_skin_cluster:
                print("BIND CURVE")
                bridgeBuilder.bindJoints(mesh=self.curv, joints=self.ctrl_joints)
        elif self.bind_mesh_checkbox.isChecked() and not self.bind_curve_checkbox.isChecked():
            if not mesh_skin_cluster:
                print("BIND MESH")
                bridgeBuilder.bindJoints(mesh=self.mesh, joints=self.bind_joints)
        else:
            if not mesh_skin_cluster and not curve_skin_cluster:
                print("BINDING CURVE AND MESH")
                bridgeBuilder.bindJoints(mesh=self.curv, joints=self.ctrl_joints)
                bridgeBuilder.bindJoints(mesh=self.mesh, joints=self.bind_joints)

    def checkCheckBoxes(self):
        rope_functions = {
            self.select_checkbox: self.runSelectSpans,
            self.curve_checkbox: self.runCreateCurve,
            self.position_percent_checkbox: self.runSetPositionPercentage,
            self.motion_path_checkbox: self.runAttachMotionPaths,
            self.bind_curve_checkbox: self.runBindJoints,
            self.bind_mesh_checkbox: self.runBindJoints
        }
        self.button_functions = []

        for i in rope_functions:
            if i.isChecked() == True:
                self.button_functions.append(rope_functions[i])
        return rope_functions, self.button_functions

    def runButtonFunctions(self):
        self.checkCheckBoxes()

        for i in self.button_functions:
            print(i)
            i()






def showUI():
    ui = RopeUI()
    ui.show()
    return ui