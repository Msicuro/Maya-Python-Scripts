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

        select_spans_layout.addWidget(select_checkbox, 0, 0)

        select_verts_text = QtWidgets.QLabel("Subdivision Axis: ")
        #select_verts_text.setAlignment(QtCore.Qt.Alignment(1))
        #select_verts_text.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        select_verts_text.setFont(QtGui.QFont("Arial", 7))
        print("Size Policy: {}".format(dir(QtWidgets.QSizePolicy())))


        # createCurve Section
        # TODO: Figure out how to add a small caption underneath
        curve_widget = QtWidgets.QWidget()
        curve_layout = QtWidgets.QGridLayout(curve_widget)
        main_layout.addWidget(curve_widget)

        curve_checkbox = QtWidgets.QCheckBox()
        curve_checkbox.setText("Create Control Curve")

        curve_layout.addWidget(curve_checkbox, 0, 0)


def showUI():
    ui = RopeUI()
    ui.show()
    return ui