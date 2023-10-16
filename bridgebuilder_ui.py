from PySide2 import QtWidgets, QtCore, QtGui


class RopeUI(QtWidgets.QDialog):
    def __init__(self):
        super(RopeUI, self).__init__()

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
        name_combo = QtWidgets.QComboBox()
        name_combo.addItem("left")
        name_combo.addItem("right")

        name_line = QtWidgets.QLineEdit()
        type_combo = QtWidgets.QComboBox()
        type_combo.addItem("Support")
        type_combo.addItem("Main Rope")

        name_layout.addWidget(name_label, 0, 0)
        name_layout.addWidget(name_combo, 0, 1)
        name_layout.addWidget(name_line, 0, 2)
        name_layout.addWidget(type_combo, 0, 3)

        # selectSpans Section
        select_spans_widget = QtWidgets.QWidget()
        select_spans_layout = QtWidgets.QGridLayout(select_spans_widget)
        main_layout.addWidget(select_spans_widget)

        select_checkbox = QtWidgets.QCheckBox()
        select_checkbox.setText("Create Joints Along Cylinder")
        #select_checkbox.setFont(QtGui.QFont( 12))

        select_spans_layout.addWidget(select_checkbox, 0, 0)

        select_verts_text = QtWidgets.QLabel("Subdivision Axis: ")
        #select_verts_text.setAlignment(QtCore.Qt.Alignment(1))
        #select_verts_text.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        select_verts_text.setFont(QtGui.QFont("Arial", 7))
        print("Size Policy: {}".format(dir(QtWidgets.QSizePolicy())))


        # createCurve Section
        curve_widget = QtWidgets.QWidget()
        curve_layout = QtWidgets.QGridLayout(curve_widget)
        main_layout.addWidget(curve_widget)

        curve_checkbox = QtWidgets.QCheckBox()
        curve_checkbox.setText("Create Control Curve")

        curve_layout.addWidget(curve_checkbox, 0, 0)

        # Position Percentage section
        position_percent_widget = QtWidgets.QWidget()
        position_percent_layout = QtWidgets.QGridLayout(position_percent_widget)
        main_layout.addWidget(position_percent_widget)

        position_percent_checkbox = QtWidgets.QCheckBox()
        position_percent_checkbox.setText("Set Locator Curve Position Percentage")

        position_percent_layout.addWidget(position_percent_checkbox, 0, 0)

        # Attach to Motion Path section
        motion_path_widget = QtWidgets.QWidget()
        motion_path_layout = QtWidgets.QGridLayout(motion_path_widget)
        main_layout.addWidget(motion_path_widget)

        motion_path_checkbox = QtWidgets.QCheckBox()
        motion_path_checkbox.setText("Attach Locators to Motion Path")
        rotations_checkbox = QtWidgets.QCheckBox()
        rotations_checkbox.setText("Include Motion Path Rotations")
        rotations_checkbox.setStyleSheet("font-size: 12px")

        motion_path_layout.addWidget(motion_path_checkbox, 0, 0)
        motion_path_layout.addWidget(rotations_checkbox, 1, 0, 1, 4, alignment=QtCore.Qt.AlignCenter)

        # Bind section
        bind_widget = QtWidgets.QWidget()
        bind_layout = QtWidgets.QGridLayout(bind_widget)
        main_layout.addWidget(bind_widget)

        bind_curve_checkbox = QtWidgets.QCheckBox()
        bind_curve_checkbox.setText("Bind Curve to Control Joints")
        bind_mesh_checkbox = QtWidgets.QCheckBox()
        bind_mesh_checkbox.setText("Bind Mesh to Locator Joints")

        bind_layout.addWidget(bind_curve_checkbox, 0, 0)
        bind_layout.addWidget(bind_mesh_checkbox, 1, 0)

        # Run Button
        run_button = QtWidgets.QPushButton("Run")
        main_layout.addWidget(run_button)

        # Set font size for function widgets
        main_font_size = 18
        select_spans_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        curve_widget.setStyleSheet("font-size: {}px; background: red".format(main_font_size))
        position_percent_widget.setStyleSheet("font-size: {}px; background: blue".format(main_font_size))
        motion_path_checkbox.setStyleSheet("font-size: {}px".format(main_font_size))
        bind_widget.setStyleSheet("font-size: {}px".format(main_font_size))
        run_button.setStyleSheet("font-size: {}px".format(main_font_size))

        curve_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)



def showUI():
    ui = RopeUI()
    ui.show()
    return ui