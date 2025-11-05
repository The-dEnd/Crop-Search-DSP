# -*- coding: utf-8 -*-


#
# Created by: PyQt5 UI code generator 5.15.9
#
# This file was first created with PyQt designer, then manually edited for a standard layout in fixed window size, then adapted by AI to adapt to window size


from PyQt5 import QtCore, QtGui, QtWidgets
from translator import tr, current_language
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt
import math, re
from measure_state import MeasureState
from datetime import datetime

maxRecent=5 #max number of items in the recent_rig.conf file
geometry = None #dimensions of the picture, to automatically align dimensions of the transparent layer for drawing and measuring lengths
setLineColor = (255, 190, 106) #color for defining a length
getLineColor = (64, 176, 166) #color for getting the length of a line, based on the set lined
#These colors have been picked to be easily distinguished by multiple categories of colorblindness, and by users of night-light screen filters; should you want to edit them, please ensure the new colors still guarantee accessibility. https://www.nceas.ucsb.edu/sites/default/files/2022-06/Colorblind%20Safe%20Color%20Schemes.pdf


unit = "" #the unit that has been set in setScale QLineEdit



def convertTxtToLength(someText): #will convert the value for size set in setScale QLineEdit to a tuple that contains the real number + unit
    if someText == None:
        return 0.0
    global unit
    result = re.search(r"^\s*^(\d+(?:[ ,.;]?\d+)?)(.*)$$", someText) #regex that parses the inputted text
    if result == None:
        return 0.0
    unit = result.group(2)
    with open("logs.txt", "a") as logFile:
        logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    inputed scale "+someText+" interpreted as"+str([result.group(1),result.group(2)])+"\n")
    try:
        return(float((result.group(1)).replace(" ",".").replace(",",".").replace(";",".")))
    except:
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    ERROR: could not interprete value \""+str(result.group(1))+"\" as float; defaulting to 0\n")
        return 0.0

class SquarePicture(QtWidgets.QLabel): #class for a picture (QLabel) with a 1:1 ration, and with a maximum size based on window size
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)

    def resizeWithParent(self): #resize to keep the height and ration
        if not self.parent():
            return
        parent_height = self.parent().height()
        max_side = int(parent_height) #max height
        side = min(max_side, self.parent().width()) #1:1 ratio
        self.setFixedSize(side, side)

    def resizeEvent(self, event):
        self.resizeWithParent()
        super().resizeEvent(event)




class Ui_Poincons_selector(object):
    def setupUi(self, Poincons_selector):
        global geometry
        Poincons_selector.setObjectName("Poincons_selector")
        Poincons_selector.resize(1497, 884)
        Poincons_selector.setMinimumSize(QtCore.QSize(1497, 884))
        Poincons_selector.setAccessibleName("")
        
        # Main central widget and layout
        central_widget = QtWidgets.QWidget(Poincons_selector)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Top section with 3 columns
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setSpacing(10)
        
        # ===== LEFT PANEL =====
        left_panel = QtWidgets.QWidget()
        left_panel.setMaximumWidth(350)
        left_panel.setMinimumWidth(320)
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Location data section
        self.type_findings = QtWidgets.QTableView()
        self.type_findings.setObjectName("type_findings")
        self.type_grid = QtWidgets.QGridLayout()
        self.type_grid.setVerticalSpacing(5)
        
        self.label_spot = QtWidgets.QLabel()
        self.label_spot.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_spot.setFont(font)
        self.label_spot.setObjectName("label_spot")
        self.type_grid.addWidget(self.label_spot, 0, 0, 1, 2)
        
        self.force_location = QtWidgets.QCheckBox()
        self.force_location.setMinimumSize(QtCore.QSize(0, 50))
        self.force_location.setMaximumSize(QtCore.QSize(150, 30))
        self.force_location.setObjectName("force_location")
        self.type_grid.addWidget(self.force_location, 0, 2, 1, 1)
        
        self.label_site = QtWidgets.QLabel()
        self.label_site.setObjectName("label_site")
        self.type_grid.addWidget(self.label_site, 2, 0, 1, 1)
        
        self.country = QtWidgets.QPlainTextEdit()
        self.country.setMaximumSize(QtCore.QSize(16777215, 30))
        self.country.setObjectName("country")
        self.type_grid.addWidget(self.country, 2, 1, 1, 2)
        
        self.region = QtWidgets.QPlainTextEdit()
        self.region.setMaximumSize(QtCore.QSize(16777215, 30))
        self.region.setObjectName("region")
        self.type_grid.addWidget(self.region, 3, 1, 1, 2)
        
        self.department = QtWidgets.QPlainTextEdit()
        self.department.setMaximumSize(QtCore.QSize(16777215, 30))
        self.department.setObjectName("department")
        self.type_grid.addWidget(self.department, 4, 1, 1, 2)
        
        self.municipality = QtWidgets.QPlainTextEdit()
        self.municipality.setMaximumSize(QtCore.QSize(16777215, 30))
        self.municipality.setObjectName("municipality")
        self.type_grid.addWidget(self.municipality, 5, 1, 1, 2)
        
        self.site = QtWidgets.QPlainTextEdit()
        self.site.setMaximumSize(QtCore.QSize(16777215, 30))
        self.site.setObjectName("site")
        self.type_grid.addWidget(self.site, 6, 1, 1, 2)
        
        self.label_X = QtWidgets.QLabel()
        self.label_X.setObjectName("label_X")
        self.type_grid.addWidget(self.label_X, 7, 0, 1, 1)
        
        self.lambert_X = QtWidgets.QPlainTextEdit()
        self.lambert_X.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lambert_X.setObjectName("lambert_X")
        self.type_grid.addWidget(self.lambert_X, 7, 1, 1, 2)
        
        self.label_Y = QtWidgets.QLabel()
        self.label_Y.setObjectName("label_Y")
        self.type_grid.addWidget(self.label_Y, 8, 0, 1, 1)
        
        self.lambert_Y = QtWidgets.QPlainTextEdit()
        self.lambert_Y.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lambert_Y.setObjectName("lambert_Y")
        self.type_grid.addWidget(self.lambert_Y, 8, 1, 1, 2)
        
        self.label_Z = QtWidgets.QLabel()
        self.label_Z.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_Z.setObjectName("label_Z")
        self.type_grid.addWidget(self.label_Z, 9, 0, 1, 1)
        
        self.lambert_Z = QtWidgets.QPlainTextEdit()
        self.lambert_Z.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lambert_Z.setObjectName("lambert_Z")
        self.type_grid.addWidget(self.lambert_Z, 9, 1, 1, 2)
        
        self.fait = QtWidgets.QLabel()
        self.fait.setObjectName("fait")
        self.type_grid.addWidget(self.fait, 10, 0, 1, 1)
        
        self.numFait = QtWidgets.QPlainTextEdit()
        self.numFait.setMaximumSize(QtCore.QSize(16777215, 30))
        self.numFait.setObjectName("numFait")
        self.type_grid.addWidget(self.numFait, 10, 1, 1, 2)
        
        self.us = QtWidgets.QLabel()
        self.us.setObjectName("us")
        self.type_grid.addWidget(self.us, 11, 0, 1, 1)
        
        self.numUs = QtWidgets.QPlainTextEdit()
        self.numUs.setMaximumSize(QtCore.QSize(16777215, 30))
        self.numUs.setObjectName("numUs")
        self.type_grid.addWidget(self.numUs, 11, 1, 1, 2)
        
        left_layout.addLayout(self.type_grid)
        
        # Ceramic data section
        self.tableView = QtWidgets.QTableView()
        self.tableView.setObjectName("tableView")
        self.gridLayout = QtWidgets.QGridLayout()
        
        self.label_type = QtWidgets.QLabel()
        self.label_type.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")
        self.gridLayout.addWidget(self.label_type, 0, 0, 1, 4)
        
        self.label_3 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 4)
        
        self.label_CRA = QtWidgets.QLabel()
        self.label_CRA.setObjectName("label_CRA")
        self.gridLayout.addWidget(self.label_CRA, 2, 0, 1, 1)
        
        self.mode_CRA = QtWidgets.QComboBox()
        self.mode_CRA.setObjectName("mode_CRA")
        self.mode_CRA.addItem("")
        self.mode_CRA.addItem("")
        self.mode_CRA.addItem("")
        self.gridLayout.addWidget(self.mode_CRA, 2, 2, 1, 2)
        
        self.label_location = QtWidgets.QLabel()
        self.label_location.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_location.setFont(font)
        self.label_location.setObjectName("label_location")
        self.gridLayout.addWidget(self.label_location, 3, 0, 1, 4)
        
        self.checkBox_edge = QtWidgets.QCheckBox()
        self.checkBox_edge.setEnabled(True)
        self.checkBox_edge.setMaximumSize(QtCore.QSize(100, 16777215))
        self.checkBox_edge.setObjectName("checkBox_edge")
        self.gridLayout.addWidget(self.checkBox_edge, 4, 0, 1, 2)
        
        self.checkBox_belly = QtWidgets.QCheckBox()
        self.checkBox_belly.setMaximumSize(QtCore.QSize(100, 16777215))
        self.checkBox_belly.setObjectName("checkBox_belly")
        self.gridLayout.addWidget(self.checkBox_belly, 4, 2, 1, 1)
        
        self.checkBox_bottom = QtWidgets.QCheckBox()
        self.checkBox_bottom.setMinimumSize(QtCore.QSize(100, 0))
        self.checkBox_bottom.setMaximumSize(QtCore.QSize(100, 16777215))
        self.checkBox_bottom.setObjectName("checkBox_bottom")
        self.gridLayout.addWidget(self.checkBox_bottom, 4, 3, 1, 1)
        
        self.label_location_2 = QtWidgets.QLabel()
        self.label_location_2.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_location_2.setFont(font)
        self.label_location_2.setObjectName("label_location_2")
        self.gridLayout.addWidget(self.label_location_2, 5, 0, 1, 4)
        
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 8, 0, 1, 2)
        
        self.rig_num = QtWidgets.QPlainTextEdit()
        self.rig_num.setMaximumSize(QtCore.QSize(16777215, 30))
        self.rig_num.setObjectName("rig_num")
        self.gridLayout.addWidget(self.rig_num, 8, 2, 1, 1)
        
        self.unknownCRA = QtWidgets.QCheckBox()
        self.unknownCRA.setObjectName("unknownCRA")
        self.gridLayout.addWidget(self.unknownCRA, 8, 3, 1, 1)
        
        self.display_types = QtWidgets.QPushButton()
        self.display_types.setMinimumSize(QtCore.QSize(0, 40))
        self.display_types.setObjectName("display_types")
        self.gridLayout.addWidget(self.display_types, 9, 0, 1, 4)
        
        left_layout.addLayout(self.gridLayout)
        left_layout.addStretch()
        
        top_layout.addWidget(left_panel)
        top_layout.setStretch(0, 0)
        
        # ===== CENTER PANEL =====
        self.center_panel = QtWidgets.QWidget()
        center_layout = QtWidgets.QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(5)
        
        # Measurement controls at top
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(5)
        
        self.reference1 = QtWidgets.QLabel()
        self.reference1.setMaximumSize(QtCore.QSize(16777215, 20))
        self.reference1.setObjectName("reference1")
        self.gridLayout_2.addWidget(self.reference1, 0, 0, 1, 1)
        
        self.measureGroup = QtWidgets.QGroupBox()
        self.measureGroup.setMinimumSize(QtCore.QSize(150, 50))
        self.measureGroup.setMaximumSize(QtCore.QSize(150, 50))
        self.measureGroup.setTitle("")
        self.measureGroup.setObjectName("measureGroup")
        
        self.setScaleButton = QtWidgets.QPushButton(self.measureGroup)
        self.setScaleButton.setGeometry(QtCore.QRect(30, 0, 92, 23))
        self.setScaleButton.setCheckable(True)
        self.setScaleButton.setObjectName("setScaleButton")
        
        self.returnSizeButton = QtWidgets.QPushButton(self.measureGroup)
        self.returnSizeButton.setGeometry(QtCore.QRect(30, 30, 92, 23))
        self.returnSizeButton.setCheckable(True)
        self.returnSizeButton.setObjectName("returnSizeButton")
        
        self.gridLayout_2.addWidget(self.measureGroup, 0, 1, 2, 1)
        
        self.setScale = QtWidgets.QTextEdit()
        self.setScale.setMaximumSize(QtCore.QSize(200, 20))
        self.setScale.setObjectName("setScale")
        self.setScale.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gridLayout_2.addWidget(self.setScale, 0, 2, 1, 1)
        
        self.reference2 = QtWidgets.QLabel()
        self.reference2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.reference2.setObjectName("reference2")
        self.gridLayout_2.addWidget(self.reference2, 1, 0, 1, 1)
        
        self.returnSize = QtWidgets.QTextEdit()
        self.returnSize.setMaximumSize(QtCore.QSize(200, 20))
        self.returnSize.setObjectName("returnSize")
        self.returnSize.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gridLayout_2.addWidget(self.returnSize, 1, 2, 1, 1)
        
        center_layout.addLayout(self.gridLayout_2)
        
        # Die picture with overlay - using QLabel with size policy
        picture_container = QtWidgets.QWidget()
        picture_layout = QtWidgets.QVBoxLayout(picture_container)
        picture_layout.setContentsMargins(0, 0, 0, 0)
        picture_layout.setAlignment(Qt.AlignCenter)
        
        self.die_picture = SquarePicture(self.center_panel)
        self.die_picture.setMinimumSize(QtCore.QSize(200, 200))
        self.die_picture.setText("")
        self.die_picture.setPixmap(QtGui.QPixmap("resources/media/empty.png"))
        self.die_picture.setScaledContents(True)
        self.die_picture.setObjectName("die_picture")
        # Keep square aspect ratio
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(True)
        self.die_picture.setSizePolicy(sizePolicy)
        
        picture_layout.addWidget(self.die_picture)
        center_layout.addWidget(picture_container, 1)  # Stretch factor 1
        
        # Store geometry for overlay
        geometry = self.die_picture.geometry()
        
        
        # Comment box at bottom
        self.comment_box = QtWidgets.QTextEdit()
        self.comment_box.setMaximumHeight(80)
        self.comment_box.setMinimumHeight(60)
        self.comment_box.setObjectName("comment_box")
        center_layout.addWidget(self.comment_box)
        
        top_layout.addWidget(self.center_panel)
        top_layout.setStretch(1, 1)
        
        # ===== RIGHT PANEL =====
        self.right_panel = QtWidgets.QWidget()
        self.right_panel.setMinimumWidth(450)
        self.right_panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        right_layout = QtWidgets.QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.die_findings = QtWidgets.QTableView()
        self.die_findings.setObjectName("die_findings")
        self.die_grid = QtWidgets.QGridLayout()
        self.die_grid.setVerticalSpacing(6)
        
        self.option1_name = QtWidgets.QLabel()
        self.option1_name.setMaximumSize(QtCore.QSize(150, 150))
        self.option1_name.setObjectName("option1_name")
        self.die_grid.addWidget(self.option1_name, 0, 0, 1, 1)
        
        self.option1_model = QtWidgets.QLabel()
        self.option1_model.setMinimumSize(QtCore.QSize(150, 150))
        self.option1_model.setMaximumSize(QtCore.QSize(150, 150))
        self.option1_model.setText("")
        self.option1_model.setPixmap(QtGui.QPixmap("resources/media/empty.png"))
        self.option1_model.setScaledContents(True)
        self.option1_model.setObjectName("option1_model")
        self.die_grid.addWidget(self.option1_model, 0, 1, 1, 1)
        
        self.option1_percent = QtWidgets.QLabel()
        self.option1_percent.setMaximumSize(QtCore.QSize(50, 50))
        self.option1_percent.setObjectName("option1_percent")
        self.die_grid.addWidget(self.option1_percent, 0, 2, 1, 1)
        
        self.option1 = QtWidgets.QRadioButton()
        self.option1.setMaximumSize(QtCore.QSize(30, 30))
        self.option1.setText("")
        self.option1.setObjectName("option1")
        self.die_grid.addWidget(self.option1, 0, 3, 1, 1)
        
        self.option2_name = QtWidgets.QLabel()
        self.option2_name.setMaximumSize(QtCore.QSize(150, 150))
        self.option2_name.setObjectName("option2_name")
        self.die_grid.addWidget(self.option2_name, 1, 0, 1, 1)
        
        self.option2_model = QtWidgets.QLabel()
        self.option2_model.setMinimumSize(QtCore.QSize(150, 150))
        self.option2_model.setMaximumSize(QtCore.QSize(150, 150))
        self.option2_model.setText("")
        self.option2_model.setPixmap(QtGui.QPixmap("resources/media/empty.png"))
        self.option2_model.setScaledContents(True)
        self.option2_model.setObjectName("option2_model")
        self.die_grid.addWidget(self.option2_model, 1, 1, 1, 1)
        
        self.option2_percent = QtWidgets.QLabel()
        self.option2_percent.setMaximumSize(QtCore.QSize(50, 50))
        self.option2_percent.setObjectName("option2_percent")
        self.die_grid.addWidget(self.option2_percent, 1, 2, 1, 1)
        
        self.option2 = QtWidgets.QRadioButton()
        self.option2.setMaximumSize(QtCore.QSize(30, 30))
        self.option2.setText("")
        self.option2.setObjectName("option2")
        self.die_grid.addWidget(self.option2, 1, 3, 1, 1)
        
        self.option3_name = QtWidgets.QLabel()
        self.option3_name.setMaximumSize(QtCore.QSize(150, 150))
        self.option3_name.setObjectName("option3_name")
        self.die_grid.addWidget(self.option3_name, 2, 0, 1, 1)
        
        self.option3_model = QtWidgets.QLabel()
        self.option3_model.setMinimumSize(QtCore.QSize(150, 150))
        self.option3_model.setMaximumSize(QtCore.QSize(150, 150))
        self.option3_model.setText("")
        self.option3_model.setPixmap(QtGui.QPixmap("resources/media/empty.png"))
        self.option3_model.setScaledContents(True)
        self.option3_model.setObjectName("option3_model")
        self.die_grid.addWidget(self.option3_model, 2, 1, 1, 1)
        
        self.option3_percent = QtWidgets.QLabel()
        self.option3_percent.setMaximumSize(QtCore.QSize(50, 50))
        self.option3_percent.setObjectName("option3_percent")
        self.die_grid.addWidget(self.option3_percent, 2, 2, 1, 1)
        
        self.option3 = QtWidgets.QRadioButton()
        self.option3.setMaximumSize(QtCore.QSize(30, 30))
        self.option3.setText("")
        self.option3.setObjectName("option3")
        self.die_grid.addWidget(self.option3, 2, 3, 1, 1)
        
        self.option4_name = QtWidgets.QLabel()
        self.option4_name.setMaximumSize(QtCore.QSize(150, 150))
        self.option4_name.setObjectName("option4_name")
        self.die_grid.addWidget(self.option4_name, 3, 0, 1, 1)
        
        self.option4_model = QtWidgets.QLabel()
        self.option4_model.setMinimumSize(QtCore.QSize(150, 150))
        self.option4_model.setMaximumSize(QtCore.QSize(150, 150))
        self.option4_model.setText("")
        self.option4_model.setPixmap(QtGui.QPixmap("resources/media/empty.png"))
        self.option4_model.setScaledContents(True)
        self.option4_model.setObjectName("option4_model")
        self.die_grid.addWidget(self.option4_model, 3, 1, 1, 1)
        
        self.option4_percent = QtWidgets.QLabel()
        self.option4_percent.setMaximumSize(QtCore.QSize(50, 50))
        self.option4_percent.setObjectName("option4_percent")
        self.die_grid.addWidget(self.option4_percent, 3, 2, 1, 1)
        
        self.option4 = QtWidgets.QRadioButton()
        self.option4.setMaximumSize(QtCore.QSize(30, 30))
        self.option4.setText("")
        self.option4.setObjectName("option4")
        self.die_grid.addWidget(self.option4, 3, 3, 1, 1)
        
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.die_grid.addWidget(self.line, 4, 0, 1, 4)
        
        self.new_radio = QtWidgets.QRadioButton()
        self.new_radio.setObjectName("new_radio")
        self.die_grid.addWidget(self.new_radio, 6, 0, 1, 1)
        
        self.new_type = QtWidgets.QComboBox()
        self.new_type.setObjectName("new_type")
        self.new_type.addItem("")
        self.new_type.addItem("")
        self.new_type.addItem("")
        self.new_type.addItem("")
        self.new_type.addItem("")
        self.new_type.addItem("")
        self.new_type.addItem("")
        self.new_type.addItem("")
        self.die_grid.addWidget(self.new_type, 6, 1, 1, 1)
        
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setObjectName("label_2")
        self.die_grid.addWidget(self.label_2, 6, 2, 1, 1)
        
        self.unknown = QtWidgets.QRadioButton()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(False)
        self.unknown.setFont(font)
        self.unknown.setObjectName("unknown")
        self.die_grid.addWidget(self.unknown, 6, 3, 1, 1)
        
        self.line_2 = QtWidgets.QFrame()
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.die_grid.addWidget(self.line_2, 7, 0, 1, 4)
        
        self.force = QtWidgets.QRadioButton()
        self.force.setObjectName("force")
        self.die_grid.addWidget(self.force, 8, 0, 1, 1)
        
        self.force_type = QtWidgets.QComboBox()
        self.force_type.setProperty("placeholderText", "")
        self.force_type.setObjectName("force_type")
        self.force_type.addItem("")
        self.force_type.addItem("")
        self.force_type.addItem("")
        self.force_type.addItem("")
        self.force_type.addItem("")
        self.force_type.addItem("")
        self.force_type.addItem("")
        self.force_type.addItem("")
        self.die_grid.addWidget(self.force_type, 8, 1, 1, 1)
        
        self.force_number = QtWidgets.QLineEdit()
        self.force_number.setMaximumSize(QtCore.QSize(82, 16777215))
        self.force_number.setText("")
        self.force_number.setObjectName("force_number")
        self.die_grid.addWidget(self.force_number, 8, 2, 1, 1)
        
        self.HelpForce = QtWidgets.QPushButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/media/magnifier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HelpForce.setIcon(icon)
        self.HelpForce.setObjectName("HelpForce")
        self.die_grid.addWidget(self.HelpForce, 8, 3, 1, 1)
        
        self.line_4 = QtWidgets.QFrame()
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.die_grid.addWidget(self.line_4, 9, 0, 1, 4)
        
        self.false_neg = QtWidgets.QPushButton()
        self.false_neg.setObjectName("false_neg")
        self.die_grid.addWidget(self.false_neg, 10, 0, 1, 2)
        
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setObjectName("label_4")
        self.die_grid.addWidget(self.label_4, 10, 2, 1, 1)
        
        self.false_pos = QtWidgets.QRadioButton()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(False)
        self.false_pos.setFont(font)
        self.false_pos.setObjectName("false_pos")
        self.die_grid.addWidget(self.false_pos, 10, 3, 1, 1)
        
        self.line_3 = QtWidgets.QFrame()
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.die_grid.addWidget(self.line_3, 11, 0, 1, 4)
        
        self.author = QtWidgets.QLineEdit()
        self.author.setObjectName("author")
        self.die_grid.addWidget(self.author, 12, 0, 1, 3)
        
        self.recentChoices = QtWidgets.QComboBox()
        self.recentChoices.setObjectName("recentChoices")
        self.recentChoices.addItem("")
        self.die_grid.addWidget(self.recentChoices, 12, 3, 1, 1)
        
        right_layout.addLayout(self.die_grid)
        right_layout.addStretch()
        
        top_layout.addWidget(self.right_panel)
        
        main_layout.addLayout(top_layout)
        top_layout.setStretch(2, 1)
        
        # ===== BOTTOM LINE =====
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.setSpacing(10)
        
        self.LegalMentions = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(6)
        self.LegalMentions.setFont(font)
        self.LegalMentions.setObjectName("LegalMentions")
        bottom_layout.addWidget(self.LegalMentions)
        
        self.licenses = QtWidgets.QPushButton()
        self.licenses.setMaximumWidth(100)
        self.licenses.setObjectName("licenses")
        bottom_layout.addWidget(self.licenses)
        
        self.switch_theme = QtWidgets.QPushButton()
        self.switch_theme.setMaximumWidth(30)
        self.switch_theme.setObjectName("switch_theme")
        bottom_layout.addWidget(self.switch_theme)
        
        bottom_layout.addStretch()
        
        self.sherdId = QtWidgets.QLabel()
        self.sherdId.setObjectName("sherdId")
        bottom_layout.addWidget(self.sherdId)
        
        self.sherdTxtId = QtWidgets.QLineEdit()
        self.sherdTxtId.setMaximumWidth(120)
        self.sherdTxtId.setObjectName("sherdTxtId")
        bottom_layout.addWidget(self.sherdTxtId)
        
        self.dieId = QtWidgets.QLabel()
        self.dieId.setObjectName("dieId")
        bottom_layout.addWidget(self.dieId)
        
        self.dieTxtId = QtWidgets.QLineEdit()
        self.dieTxtId.setMaximumWidth(120)
        self.dieTxtId.setObjectName("dieTxtId")
        bottom_layout.addWidget(self.dieTxtId)
        
        bottom_layout.addStretch()
        
        self.exit = QtWidgets.QPushButton()
        self.exit.setMinimumWidth(80)
        self.exit.setObjectName("exit")
        bottom_layout.addWidget(self.exit)
        
        self.skip = QtWidgets.QPushButton()
        self.skip.setMinimumWidth(80)
        self.skip.setObjectName("skip")
        bottom_layout.addWidget(self.skip)
        
        self.next = QtWidgets.QPushButton()
        self.next.setMinimumWidth(80)
        self.next.setObjectName("next")
        bottom_layout.addWidget(self.next)
        
        main_layout.addLayout(bottom_layout)
        
        # Set the central widget
        #Poincons_selector.setCentralWidget(central_widget)
        
        # Store references for overlay repositioning
        self.central_widget = central_widget
        self.picture_container = picture_container
        
        self.retranslateUi(Poincons_selector)
        self.next.clicked.connect(Poincons_selector.next_clicked) # type: ignore
        self.exit.clicked.connect(Poincons_selector.exit_clicked) # type: ignore
        self.skip.clicked.connect(Poincons_selector.skip_clicked) # type: ignore
        self.returnSizeButton.clicked.connect(Poincons_selector.retrieve_scale) # type: ignore
        self.setScaleButton.clicked.connect(Poincons_selector.set_scale) # type: ignore
        self.unknown.clicked.connect(Poincons_selector.radioboxUnk_ticked) # type: ignore
        self.force.clicked.connect(Poincons_selector.radioboxFor_ticked) # type: ignore
        self.new_radio.clicked.connect(Poincons_selector.radioboxNew_ticked) # type: ignore
        self.option1.clicked.connect(Poincons_selector.radiobox1_ticked) # type: ignore
        self.option2.clicked.connect(Poincons_selector.radiobox2_ticked) # type: ignore
        self.option3.clicked.connect(Poincons_selector.radiobox3_ticked) # type: ignore
        self.option4.clicked.connect(Poincons_selector.radiobox4_ticked) # type: ignore
        self.new_type.currentTextChanged['QString'].connect(Poincons_selector.new_changed_type) # type: ignore
        self.force_type.currentTextChanged['QString'].connect(Poincons_selector.force_changed_type) # type: ignore
        self.force_number.textChanged['QString'].connect(Poincons_selector.force_changed_number) # type: ignore
        self.display_types.clicked.connect(Poincons_selector.show_types) # type: ignore
        self.mode_CRA.currentTextChanged['QString'].connect(Poincons_selector.cra_changed_type) # type: ignore
        self.rig_num.textChanged.connect(Poincons_selector.cra_changed_number) # type: ignore
        self.country.textChanged.connect(Poincons_selector.country_changed) # type: ignore
        self.lambert_X.textChanged.connect(Poincons_selector.x_changed) # type: ignore
        self.lambert_Z.textChanged.connect(Poincons_selector.z_changed) # type: ignore
        self.lambert_Y.textChanged.connect(Poincons_selector.y_changed) # type: ignore
        self.checkBox_belly.clicked.connect(Poincons_selector.location_changed) # type: ignore
        self.checkBox_bottom.clicked.connect(Poincons_selector.location_changed) # type: ignore
        self.checkBox_edge.clicked.connect(Poincons_selector.location_changed) # type: ignore
        self.region.textChanged.connect(Poincons_selector.region_changed) # type: ignore
        self.department.textChanged.connect(Poincons_selector.department_changed) # type: ignore
        self.municipality.textChanged.connect(Poincons_selector.municipality_changed) # type: ignore
        self.site.textChanged.connect(Poincons_selector.site_changed) # type: ignore
        self.unknownCRA.stateChanged['int'].connect(Poincons_selector.unknownCRA_changed) # type: ignore
        self.author.textEdited['QString'].connect(Poincons_selector.author_changed) # type: ignore
        self.licenses.clicked.connect(Poincons_selector.popup_license) # type: ignore
        self.numFait.textChanged.connect(Poincons_selector.fait_changed) # type: ignore
        self.numUs.textChanged.connect(Poincons_selector.us_changed) # type: ignore
        self.comment_box.textChanged.connect(Poincons_selector.comment_edited) # type: ignore
        self.false_neg.clicked.connect(Poincons_selector.false_negative) # type: ignore
        self.false_pos.clicked.connect(Poincons_selector.false_positive) # type: ignore
        self.HelpForce.clicked.connect(Poincons_selector.force_finder) # type: ignore
        self.switch_theme.clicked.connect(Poincons_selector.popup_theme) # type: ignore
        self.recentChoices.currentIndexChanged['QString'].connect(Poincons_selector.history_force) # type: ignore
        self.setScale.textChanged.connect(Poincons_selector.edit_scale) # type: ignore
        self.setScaleButton.toggled['bool'].connect(Poincons_selector.set_scale) # type: ignore
        self.returnSizeButton.toggled['bool'].connect(Poincons_selector.retrieve_scale) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Poincons_selector)

    def retranslateUi(self, Poincons_selector):
        _translate = QtCore.QCoreApplication.translate
        Poincons_selector.setWindowTitle(_translate("Poincons_selector", tr("mainTitle")))
        self.force.setText(_translate("Poincons_selector", tr("force")))
        self.option3_percent.setText(_translate("Poincons_selector", "INI"))
        listChoices = tr("lMotifs")
        self.force_type.setCurrentText(_translate("Dialog", tr("lMotifs")[0]))
        for i in range(len(listChoices)):
            self.force_type.setItemText(i, _translate("Dialog", tr("lMotifs")[i]))
        self.option2_percent.setText(_translate("Poincons_selector", "INI"))
        self.force_number.setPlaceholderText(_translate("Poincons_selector", tr("typeNr")))
        self.option4_percent.setText(_translate("Poincons_selector", "INI"))
        self.label_2.setText(_translate("Poincons_selector", "ou"))
        self.option4_name.setText(_translate("Poincons_selector", "INIT"))
        self.false_neg.setText(_translate("Poincons_selector", tr("falseNeg")))
        self.option1_name.setText(_translate("Poincons_selector", "INIT"))
        self.new_radio.setText(_translate("Poincons_selector", "Inédit"))
        self.option2_name.setText(_translate("Poincons_selector", "INIT"))
        self.option3_name.setText(_translate("Poincons_selector", "INIT"))
        self.false_pos.setText(_translate("Poincons_selector", tr("falsePos")))
        self.label_4.setText(_translate("Poincons_selector", "ou"))
        self.author.setPlaceholderText(_translate("Poincons_selector", tr("author")))
        self.unknown.setText(_translate("Poincons_selector", tr("undet")))
        self.option1_percent.setText(_translate("Poincons_selector", "INI"))
        self.new_type.setProperty("placeholderText", _translate("Poincons_selector", tr("selectPattern")))
        listChoices = tr("lMotifs")
        self.new_type.setCurrentText(_translate("Dialog", tr("lMotifs")[0]))
        for i in range(len(listChoices)):
            self.new_type.setItemText(i, _translate("Dialog", tr("lMotifs")[i]))
        self.exit.setText(_translate("Poincons_selector", tr("exit")))
        self.skip.setText(_translate("Poincons_selector", tr("skip")))
        self.next.setText(_translate("Poincons_selector", tr("next")))
        self.fait.setText(_translate("Poincons_selector", tr("featureNr")))
        self.label_site.setText(_translate("Poincons_selector", "Site"))
        self.municipality.setPlaceholderText(_translate("Poincons_selector", tr("city")))
        self.country.setPlaceholderText(_translate("Poincons_selector", tr("country")))
        self.lambert_Y.setPlaceholderText(_translate("Poincons_selector", "Lambert 93 - Y"))
        self.us.setText(_translate("Poincons_selector", tr("contextNr")))
        self.numUs.setPlaceholderText(_translate("Poincons_selector", tr("contextPrompt")))
        self.label_X.setText(_translate("Poincons_selector", "X"))
        self.label_spot.setText(_translate("Poincons_selector", tr("loca")))
        self.label_Y.setText(_translate("Poincons_selector", "Y"))
        self.department.setPlaceholderText(_translate("Poincons_selector", tr("dpt")))
        self.region.setPlaceholderText(_translate("Poincons_selector", tr("region")))
        self.lambert_Z.setPlaceholderText(_translate("Poincons_selector", "Lambert 93 - Z"))
        self.numFait.setPlaceholderText(_translate("Poincons_selector", tr("featurePrompt")))
        self.site.setPlaceholderText(_translate("Poincons_selector", tr("place")))
        self.label_Z.setText(_translate("Poincons_selector", "Z"))
        self.lambert_X.setPlaceholderText(_translate("Poincons_selector", "Lambert 93 - X"))
        self.force_location.setText(_translate("Poincons_selector", tr("forceLocation")))
        self.sherdId.setText(tr("sherdNr"))
        self.dieId.setText(tr("dieNr"))
        self.mode_CRA.setCurrentText(_translate("Poincons_selector", "A"))
        self.mode_CRA.setItemText(0, _translate("Poincons_selector", "A"))
        self.mode_CRA.setItemText(1, _translate("Poincons_selector", "B"))
        self.mode_CRA.setItemText(2, _translate("Poincons_selector", tr("undet")))
        self.display_types.setText(_translate("Poincons_selector", tr("displayTypes")))
        self.checkBox_belly.setText(_translate("Poincons_selector", tr("belly")))
        self.label_CRA.setText(_translate("Poincons_selector", tr("cratype")))
        self.label_type.setText(_translate("Poincons_selector", tr("ceramData")))
        self.checkBox_edge.setText(_translate("Poincons_selector", tr("edge")))
        self.rig_num.setPlaceholderText(_translate("Poincons_selector", tr("typeNrHere")))
        self.label_location.setText(_translate("Poincons_selector", tr("sherdLoc")))
        self.checkBox_bottom.setText(_translate("Poincons_selector", tr("bottom")))
        self.unknownCRA.setText(_translate("Poincons_selector", tr("otherType")))
        self.label_location_2.setText(_translate("Poincons_selector", tr("shape")))
        self.label.setText(_translate("Poincons_selector", tr("typeNum")))
        self.label_3.setText(_translate("Poincons_selector", tr("category")))
        self.reference1.setText(_translate("Poincons_selector", "INIT INIT INIT INIT INIT INIT"))
        self.reference2.setText(_translate("Poincons_selector", "INIT INIT INIT INIT INIT INIT"))
        self.LegalMentions.setText(_translate("Poincons_selector", "INIT"))
        self.licenses.setText(_translate("Poincons_selector", tr("displayLicense")))
        self.comment_box.setPlaceholderText(_translate("Poincons_selector", tr("typeComment")))
        self.switch_theme.setText(_translate("Poincons_selector", "☀️"))
        self.setScaleButton.setText(_translate("Poincons_selector", tr("setScale")))
        self.returnSizeButton.setText(_translate("Poincons_selector", tr("measureLength")))
        self.setScale.setPlaceholderText(_translate("Poincons_selector", tr("typeLength")))

class DrawingOverlay(QtWidgets.QLabel): #handles the measures of size in the 2 buttons + 2 QLineEdit above the die picture 
    def __init__(self, main_parent):
        super().__init__(main_parent.ui.picture_container)
        self.main_parent = main_parent
        global geometry
        self.setGeometry(geometry)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.overlay_pixmap = QtGui.QPixmap(geometry.width(), geometry.height())
        self.overlay_pixmap.fill(QtCore.Qt.transparent)
        self.setPixmap(self.overlay_pixmap)
        self.statusLine = {"set": None, "get": None, "none": None} #dictionnary keeping track of the boolean with coordinates of lines to be drawn for set and get; "none" attribute will be a "trah" value, never read, for when the user tries to draw a line without get/set before
        self.start_point = None
        self.end_point = None
        self.drawing = False
        self.updateGeometry
        
    def updateGeometry(self): #updates overlay geometry to match die_picture
        die_pic_geometry = self.main_parent.ui.die_picture.geometry()
        self.setGeometry(die_pic_geometry)
        # recreate pixmap with new size
        self.overlay_pixmap = QtGui.QPixmap(die_pic_geometry.width(), die_pic_geometry.height())
        self.overlay_pixmap.fill(QtCore.Qt.transparent)
        self.setPixmap(self.overlay_pixmap)
        # redraw existing lines scaled to new size
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            #now we will clear the previous line with current status from the statusLine
            state = self.getLineState()
            self.statusLine[state] = None
            self.drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.update()  #calls paintEvent to refresh the line display

    def getLineState(self):
        setMeasureState = MeasureState.setMeasureState
        getMeasureState = MeasureState.getMeasureState
        if not(getMeasureState) and not(setMeasureState): #no button selected => no display => transparent line
            return("none")
        if setMeasureState:
            return("set")
        if getMeasureState:
            return("get")

    def mouseReleaseEvent(self, event): #end of the line
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.end_point = event.pos()
            self.update()
            currentState = self.getLineState()
            if self.start_point and self.end_point:
                self.statusLine[currentState] = (self.start_point, self.end_point)
                with open("logs.txt", "a") as logFile:
                    logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    new line "+currentState+" drawn; status is:"+str(self.statusLine)+"\n")
                self.refresh_length()
            #print(self.statusLine, self.start_point, self.end_point) #for debug purpose only

    def refresh_length(self): #refreshes the displayed length, if the length of set_scale or retrieve_scale changes, or if the QLineEdit SetScale value changes
        global unit
        lSet = 0.0000001 #prevent divide by 0
        lGet = 0.0000001 #prevent divide by 0
        for state, line in self.statusLine.items():
            if line is None:
                continue
            if state == "set":
                lSet = self.calculate_length(line[0], line[1])
            if state == "get":
                lGet = self.calculate_length(line[0], line[1])
        setSize = self.main_parent.ui.setScale.toPlainText()
        lCm = convertTxtToLength(setSize)
        if lCm == 0.0 or lGet == 0 or lGet == None or lSet == 0 or lSet == None:
            self.main_parent.ui.returnSize.setPlainText("")
        ratio = float(lCm)/(float(lSet)+0.001)
        self.main_parent.ui.returnSize.setPlainText(str(round(float(lGet*ratio),2))+" "+unit)

    def paintEvent(self, event):#draws the line being currently measured
        if self.start_point and self.end_point:
            painter = QPainter(self)
            try:
                for state, line in self.statusLine.items(): #pick a color
                    if line is None:
                        continue
                    if state == "none": #no button selected => no display => transparent line
                        pen = QPen(QColor(Qt.transparent))
                    if state == "set":
                        pen = QPen(QColor(setLineColor[0], setLineColor[1], setLineColor[2]), 3)
                    if state == "get":
                        pen = QPen(QColor(getLineColor[0], getLineColor[1], getLineColor[2]), 3)

                    painter.setPen(pen)
                    painter.drawLine(line[0], line[1])
                    
                if self.drawing and self.start_point and self.end_point: #draw actual line
                    state = self.getLineState()
                    if state == "none": #no button selected => no display => transparent line
                        pen = QPen(QColor(Qt.transparent))
                    if state == "set":
                        pen = QPen(QColor(setLineColor[0], setLineColor[1], setLineColor[2]), 3)
                    if state == "get":
                        pen = QPen(QColor(getLineColor[0], getLineColor[1], getLineColor[2]), 3)
                    painter.setPen(pen)
                    painter.drawLine(self.start_point, self.end_point)
            
            finally:
                painter.end()


    def calculate_length(self, p1: QtCore.QPoint, p2: QtCore.QPoint) -> float:
        return math.hypot(p2.x() - p1.x(), p2.y() - p1.y())