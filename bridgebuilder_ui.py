from PySide2 import QtWidgets


class RopeUI(QtWidgets.QDialog):
    def __init__(self):
        super(RopeUI, self).__init__()

        self.setWindowTitle("Rope Builder")
        # self.rope = RopeUI()

        self.buildUI()
        #self-populateUI()

    def buildUI(self):
        # Create parent layout
        rope_layout = QtWidgets.QVBoxLayout(self)

        # Create the name section layout and add it to the main layout
        # Name Section
        name_widget = QtWidgets.QWidget()
        name_layout = QtWidgets.QHBoxLayout(name_widget)
        rope_layout.addWidget(name_widget)

        # Create the elements in the name section and add them to the section
        name_label = QtWidgets.QLabel("Name")

        name_combo = QtWidgets.QComboBox()
        name_combo.addItem("left")
        name_combo.addItem("right")

        name_line = QtWidgets.QLineEdit()

        type_combo = QtWidgets.QComboBox()
        type_combo.addItem("Support")
        type_combo.addItem("Main Rope")

        name_layout.addWidget(name_label)
        name_layout.addWidget(name_combo)
        name_layout.addWidget(name_line)
        name_layout.addWidget(type_combo)

        # selectSpans Section
        select_field_widget = QtWidgets.QWidget()
        select_field_layout = QtWidgets.QVBoxLayout(select_field_widget)
        rope_layout.addWidget(select_field_widget)

        select_spans_widget = QtWidgets.QWidget()
        select_spans_layout = QtWidgets.QHBoxLayout(select_spans_widget)
        select_field_layout.addWidget(select_spans_widget)

        select_checkbox = QtWidgets.QCheckBox()
        select_label = QtWidgets.QLabel("Create Joints Along Cylinder")
        select_button = QtWidgets.QPushButton("Run")

        select_spans_layout.addWidget(select_checkbox)
        select_spans_layout.addWidget(select_label)
        select_spans_layout.addWidget(select_button)

        select_verts_widget = QtWidgets.QWidget()
        select_verts_layout = QtWidgets.QHBoxLayout(select_verts_widget)

        select_verts_text = QtWidgets.QLabel("# of Vertices per Loop: ")
        select_verts_input = QtWidgets.QLineEdit()

        select_verts_layout.addWidget(select_verts_text)
        select_verts_layout.addWidget(select_verts_input)

        select_field_layout.addWidget(select_verts_widget)

        # createCurve Section
        # TODO: Figure out how to add a small caption underneath
        curve_widget = QtWidgets.QWidget()
        curve_layout = QtWidgets.QHBoxLayout(curve_widget)
        rope_layout.addWidget(curve_widget)

        curve_checkbox = QtWidgets.QCheckBox()
        curve_label = QtWidgets.QLabel("Create Control Curve")
        curve_button = QtWidgets.QPushButton("Run")

        curve_layout.addWidget(curve_checkbox)
        curve_layout.addWidget(curve_label)
        curve_layout.addWidget(curve_button)


def showUI():
    ui = RopeUI()
    ui.show()
    return ui