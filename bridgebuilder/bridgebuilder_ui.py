from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
from maya import OpenMayaUI as omui
import bridgebuilder
from shiboken2 import wrapInstance
import logging

# Set up logger config and current level
logging.basicConfig()
logger = logging.getLogger("BridgeBuilder UI")
logger.setLevel(logging.INFO)


def getMayaMainWindow():
    window = omui.MQtUtil_mainWindow()
    pointer = wrapInstance(long(window), QtWidgets.QMainWindow)
    return pointer


class RopeUI(QtWidgets.QDialog):
    def __init__(self):
        parent = getMayaMainWindow()
        super(RopeUI, self).__init__(parent=parent)

        self.setWindowTitle("Rope Builder")

        self.buildUI()

    def buildUI(self):
        '''
        Builds the UI elements to allow functions from bridgebuilder to run

        '''

        # Create parent layout to hold the widgets for each Rope Type
        self.parent_layout = QtWidgets.QVBoxLayout(self)

        # Create the Rig name section layout and add it to the parent layout
        name_widget = QtWidgets.QWidget()
        name_layout = QtWidgets.QGridLayout(name_widget)
        self.parent_layout.addWidget(name_widget)

        # Create the elements in the Rig name section
        # Rope Type Combobox elements are added below when their widget is created
        name_label = QtWidgets.QLabel("Name")

        self.name_combo = QtWidgets.QComboBox()
        prefix_names = ["left", "right", "center"]
        self.name_combo.addItems(prefix_names)

        self.name_line = QtWidgets.QLineEdit()

        self.type_combo = QtWidgets.QComboBox()

        # Create widgets for the tool functions (Main & Support)
        self.type_widgets = {"Main":QtWidgets.QWidget(), "Support":QtWidgets.QWidget()}
        # Add the keys for each tool widget to the Type combo box
        self.type_combo.addItems(sorted(self.type_widgets))

        name_layout.addWidget(name_label, 0, 0)
        name_layout.addWidget(self.name_combo, 0, 1)
        name_layout.addWidget(self.name_line, 0, 2)
        name_layout.addWidget(self.type_combo, 0, 3)


        # Create vertical layouts for the rope types menu options
        main_layout = QtWidgets.QVBoxLayout(self.type_widgets["Main"])
        support_layout = QtWidgets.QVBoxLayout(self.type_widgets["Support"])

        # Add the widgets from the Type combo box to the parent layout
        for i in sorted(self.type_widgets):
            self.parent_layout.addWidget(self.type_widgets[i])

        # Create the Main Rope menu components

        # Setup selectSpans Section for the selectSpans function
        select_spans_widget = QtWidgets.QWidget()
        select_spans_layout = QtWidgets.QGridLayout(select_spans_widget)
        main_layout.addWidget(select_spans_widget)

        self.select_checkbox = QtWidgets.QCheckBox("Create Joints Along Cylinder")
        select_spans_layout.addWidget(self.select_checkbox, 0, 0)

        select_verts_text = QtWidgets.QLabel("Subdivision Axis: ")
        select_verts_text.setFont(QtGui.QFont("Arial", 7))


        # Setup createCurve Section for the createCurve function
        curve_widget = QtWidgets.QWidget()
        curve_layout = QtWidgets.QGridLayout(curve_widget)
        main_layout.addWidget(curve_widget)

        self.curve_checkbox = QtWidgets.QCheckBox("Create Control Curve")
        curve_layout.addWidget(self.curve_checkbox, 0, 0)

        # Setup Position Percentage section for the setPositionPercentage function
        position_percent_widget = QtWidgets.QWidget()
        position_percent_layout = QtWidgets.QGridLayout(position_percent_widget)
        main_layout.addWidget(position_percent_widget)

        self.position_percent_checkbox = QtWidgets.QCheckBox("Set Locator Curve Position Percentage")
        position_percent_layout.addWidget(self.position_percent_checkbox, 0, 0)

        # Setup Attach to Motion Path section fir the attachToMotionPath function
        motion_path_widget = QtWidgets.QWidget()
        motion_path_layout = QtWidgets.QGridLayout(motion_path_widget)
        motion_path_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        main_layout.addWidget(motion_path_widget)

        self.motion_path_checkbox = QtWidgets.QCheckBox("Attach Locators to Motion Path")
        self.rotations_checkbox = QtWidgets.QCheckBox("Include Motion Path Rotations")

        motion_path_layout.addWidget(self.motion_path_checkbox, 0, 0)
        motion_path_layout.addWidget(self.rotations_checkbox, 1, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)


        # Setup Bind section for the bindJoints function
        bind_widget = QtWidgets.QWidget()
        bind_layout = QtWidgets.QGridLayout(bind_widget)
        main_layout.addWidget(bind_widget)

        self.bind_curve_checkbox = QtWidgets.QCheckBox("Bind Curve to Control Joints")
        self.bind_mesh_checkbox = QtWidgets.QCheckBox("Bind Mesh to Locator Joints")

        bind_layout.addWidget(self.bind_curve_checkbox, 0, 0)
        bind_layout.addWidget(self.bind_mesh_checkbox, 1, 0)

        # Setup Run Button to execute selected commands
        run_button = QtWidgets.QPushButton("Run")
        self.parent_layout.addWidget(run_button)


        # Create the Support Rope menu components

        # Setup Support Rope Section for the supportRope function
        support_rope_widget = QtWidgets.QWidget()
        support_rope_layout = QtWidgets.QGridLayout(support_rope_widget)
        support_layout.addWidget(support_rope_widget)

        self.support_rope_checkbox = QtWidgets.QCheckBox("Create Support Ropes")
        support_rope_layout.addWidget(self.support_rope_checkbox, 0, 0)

        # Set font size for the individual function widgets
        main_font_size = 18
        select_spans_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        curve_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        position_percent_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        self.motion_path_checkbox.setStyleSheet("font-size: {}px".format(main_font_size))
        self.rotations_checkbox.setStyleSheet("font-size: 12px")
        bind_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        support_rope_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        run_button.setStyleSheet("font-size: {}px".format(main_font_size))


        # Connect the Run button to the widget functions
        run_button.clicked.connect(self.runButtonFunctions)

        # Show the appropriate widget on startup based on the default combobox option
        self.typecomboboxCallback(self.type_combo.currentIndex())

        # Connect the Type combo box signal to control menu type visibility
        self.type_combo.activated.connect(self.typecomboboxCallback)

    def runSelectSpans(self):
        self.bind_joints, \
        self.locators, \
        self.spans, \
        self.name, \
        self.mesh, \
        self.constructor = bridgebuilder.selectSpans("{}_{}_{}".format(self.name_combo.currentText(),
                                                                       self.name_line.text(),
                                                                       self.type_combo.currentText()))

        return self.bind_joints, self.locators, self.spans, self.name, self.mesh, self.constructor

    # Create functions corresponding to bridgebuilder functions so checkboxes can store/execute them
    def runCreateCurve(self):
        self.curv, \
        self.positions, \
        self.ctrl_joints = bridgebuilder.createCurve("{}_{}_{}".format(self.name_combo.currentText(),
                                                                       self.name_line.text(),
                                                                       self.type_combo.currentText()))
        return self.curv, self.positions, self.ctrl_joints

    def runSetPositionPercentage(self):
        self.joint_percentages = bridgebuilder.setPositionPercentage(self.curv, self.locators)
        return self.joint_percentages

    def runAttachMotionPaths(self):
        self.motion_paths = bridgebuilder.attachToMotionPath(joint_percentage_values=self.joint_percentages,
                                                             curve=self.curv, locators=self.locators,
                                                             ctrl_joints=self.ctrl_joints,
                                                             rope_type=self.type_combo.currentText(),
                                                             rotation=self.rotations_checkbox.isChecked())
        logger.debug("ROPE TYPE: {}".format(self.type_combo.currentText()))
        return self.motion_paths

    def runBindJoints(self):
        # Save the skin cluster for the curve and mesh if they exist
        curve_skin_cluster = [i for i in cmds.listHistory(self.curv) if cmds.objectType(i, isType="skinCluster")]
        mesh_skin_cluster = [i for i in cmds.listHistory(self.mesh) if cmds.objectType(i, isType="skinCluster")]

        # Check if the object being skinned already has a skin cluster before binding
        if self.bind_curve_checkbox.isChecked() and not self.bind_mesh_checkbox.isChecked():
            if not curve_skin_cluster:
                logger.info("BIND CURVE")
                bridgebuilder.bindJoints(mesh=self.curv, joints=self.ctrl_joints)
        elif self.bind_mesh_checkbox.isChecked() and not self.bind_curve_checkbox.isChecked():
            if not mesh_skin_cluster:
                logger.info("BIND MESH")
                bridgebuilder.bindJoints(mesh=self.mesh, joints=self.bind_joints)
        else:
            if not mesh_skin_cluster and not curve_skin_cluster:
                logger.info("BINDING CURVE AND MESH")
                bridgebuilder.bindJoints(mesh=self.curv, joints=self.ctrl_joints)
                bridgebuilder.bindJoints(mesh=self.mesh, joints=self.bind_joints)

    def createSupportRopes(self):
        support_meshes = cmds.ls(sl=1)
        # Turn on the rotation checkbox so the rotations on motion paths are enabled
        self.rotations_checkbox.setChecked(1)

        # Iterate through each selected mesh and create the support rope
        for i, v in enumerate(support_meshes):
            name = "{}_{}_{}".format(self.name_combo.currentText(), self.name_line.text(), i,
                                                                        self.type_combo.currentText())

            cmds.select(v)
            self.runSelectSpans()
            # Create the group for the locators
            loc_group = cmds.group(self.locators, name="{}_LOC_GRP".format(name))

            cmds.select(self.locators[0::2])
            self.runCreateCurve()
            # Run the build supports function
            new_ik_handle, new_ik_ctrl, new_pvector = bridgebuilder.buildSupport(self.ctrl_joints)

            self.runSetPositionPercentage()
            self.runAttachMotionPaths()

            bridgebuilder.addStretchyIK(self.ctrl_joints)

            support_ctrl_jnt_grps = [i for i in cmds.listRelatives(self.ctrl_joints[0::], p=1) if cmds.objectType(i) == "transform"]
            support_ik_GRP = cmds.listRelatives(new_pvector, ap=1, f=1)[0].split("|")[1]
            cmds.group(self.mesh, loc_group, support_ctrl_jnt_grps, self.curv, support_ik_GRP, name="{}_GRP".format(name))

            self.runBindJoints()
            self.runBindJoints()

        # Uncheck the rotations box for motion paths after the function completes so the UI is clean
        self.rotations_checkbox.setChecked(0)

    def checkCheckBoxes(self):
        '''
        Checks the "checked" status of each checkbox so they can be executed later
        Returns:
            rope_functions: A dictionary of each checkbox with the corresponding function
            button_functions: A list of all functions matched with checkboxes that are checked

        '''
        rope_functions = {
            self.select_checkbox: self.runSelectSpans,
            self.curve_checkbox: self.runCreateCurve,
            self.position_percent_checkbox: self.runSetPositionPercentage,
            self.motion_path_checkbox: self.runAttachMotionPaths,
            self.bind_curve_checkbox: self.runBindJoints,
            self.bind_mesh_checkbox: self.runBindJoints,
            self.support_rope_checkbox: self.createSupportRopes
        }
        self.button_functions = []

        for i in rope_functions:
            if i.isChecked():
                self.button_functions.append(rope_functions[i])
        return rope_functions, self.button_functions

    def runButtonFunctions(self):
        '''
        Goes through the button_functions list and runs each function

        '''
        self.checkCheckBoxes()

        for i in self.button_functions:
            logger.info(i)
            i()

    def toggleWidgetVisibility(self, show=None, hide=None):
        '''
        Toggles the visibility of widgets
        Args:
            show: The widget to show
            hide: The widget to hide

        '''
        # TODO Add error messages if type or hidden status isn't correct
        logger.debug("SHOW: {}".format(show))
        logger.debug("HIDE: {}".format(hide))
        logger.debug("CURRENT DATA: {}".format(self.type_combo.currentData()))
        logger.debug("ITEM DATA: {}".format(self.type_combo.itemData(self.type_combo.currentIndex())))
        if isinstance(show, QtWidgets.QWidget):
            logger.debug("SHOW: {}".format(show))
            show.show()
        if isinstance(hide, QtWidgets.QWidget):
            logger.debug("HIDE: {}".format(hide))
            hide.hide()

    def typecomboboxCallback(self, key):
        '''
        Sets the visibility of a widget when called after a combobox is activated
        Args:
            key: A key passed from the type_combobox dictionary

        '''
        logger.info(key)
        for key_index, key_name in enumerate(sorted(self.type_widgets)):
            self.type_widgets[key_name].setVisible(key_index == key)

        self.resize(QtWidgets.QWidget.minimumSizeHint(self))


def showUI():
    ui = RopeUI()
    ui.show()
    return ui