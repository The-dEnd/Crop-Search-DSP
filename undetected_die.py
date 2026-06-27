# -*- coding: utf-8 -*-


#
# Created by: PyQt5 UI code generator 5.15.9
#
# This file was first created with PyQt designer, then manually edited for a standard layout in fixed window size, then adapted by AI (Claude Sonnet 4.5) to adapt to window size


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from datetime import datetime
from force_sherd import ForceTypePopup
from translator import tr, current_language


class Ui_AddDieDialog(QtWidgets.QDialog):
    def setupUi(self, Dialog, path):
        Dialog.setObjectName("Dialog")
        Dialog.setMinimumSize(QtCore.QSize(782, 800))
        self.Dialog = Dialog
        self.path = path
        
        # Main vertical layout
        main_layout = QtWidgets.QVBoxLayout(Dialog)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Top label
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        main_layout.addWidget(self.label)
        
        # Picture container with centered square image
        picture_container = QtWidgets.QWidget(Dialog)
        picture_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        picture_layout = QtWidgets.QHBoxLayout(picture_container)
        picture_layout.setContentsMargins(0, 0, 0, 0)
        
        
        # Die picture (square, scales with window)
        self.die_picture = DrawablePictureLabel(self, self.path)
        self.die_picture.setMinimumSize(QtCore.QSize(400, 400))
        self.die_picture.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.die_picture.setText("")
        self.die_picture.setObjectName("die_picture")
        picture_layout.addWidget(self.die_picture)
        
        
        main_layout.addWidget(picture_container, 1)  # stretch factor 1 to take available space
        
        # Bottom controls layout
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.setSpacing(10)
        
        # Left group: set_type, set_number, HelpForce
        self.set_type = QtWidgets.QComboBox(Dialog)
        self.set_type.setMinimumSize(QtCore.QSize(150, 30))
        self.set_type.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.set_type.setProperty("placeholderText", "")
        self.set_type.setObjectName("set_type")
        self.set_type.addItem("")
        self.set_type.addItem("")
        self.set_type.addItem("")
        self.set_type.addItem("")
        self.set_type.addItem("")
        self.set_type.addItem("")
        self.set_type.addItem("")
        self.set_type.addItem("")
        bottom_layout.addWidget(self.set_type)
        
        self.set_number = QtWidgets.QLabel(Dialog)
        self.set_number.setMinimumSize(QtCore.QSize(137, 30))
        self.set_number.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.set_number.setText(tr("chooseRight"))
        self.set_number.setObjectName("set_number")
        bottom_layout.addWidget(self.set_number)
        
        self.HelpForce = QtWidgets.QPushButton(Dialog)
        self.HelpForce.setMinimumSize(QtCore.QSize(30, 30))
        self.HelpForce.setMaximumSize(QtCore.QSize(30, 30))
        self.HelpForce.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/media/magnifier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HelpForce.setIcon(icon)
        self.HelpForce.setObjectName("HelpForce")
        self.HelpForce.clicked.connect(self.force_finder) # type: ignore
        bottom_layout.addWidget(self.HelpForce)
        
        # Spacer between left and right groups
        bottom_layout.addStretch(1)
        
        # Right group: validate, cancel
        self.validate = QtWidgets.QPushButton(Dialog)
        self.validate.setMinimumSize(QtCore.QSize(131, 30))
        self.validate.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.validate.setObjectName("validate")
        self.validate.setDefault(True)
        self.validate.setAutoDefault(True)
        bottom_layout.addWidget(self.validate)
        
        self.cancel = QtWidgets.QPushButton(Dialog)
        self.cancel.setMinimumSize(QtCore.QSize(130, 30))
        self.cancel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.cancel.setObjectName("cancel")
        bottom_layout.addWidget(self.cancel)
        
        main_layout.addLayout(bottom_layout)
        
        self.retranslateUi(Dialog)
        self.cancel.clicked.connect(Dialog.exit) # type: ignore
        self.validate.clicked.connect(Dialog.accept) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", tr("falseNeg")))
        self.cancel.setText(_translate("Dialog", tr("cancel")))
        self.validate.setText(_translate("Dialog", tr("validate")))
        #self.set_number.setPlaceholderText(_translate("Dialog", tr("typeNr")))
        listChoices = tr("lMotifs")
        self.set_type.setCurrentText(_translate("Dialog", tr("lMotifs")[0]))
        for i in range(len(listChoices)):
            self.set_type.setItemText(i, _translate("Dialog", tr("lMotifs")[i]))
        self.set_type.setItemText(9, _translate("Dialog", tr("undet")))
        self.set_type.setItemText(10, _translate("Dialog", tr("new")))
        self.label.setText(_translate("Dialog", tr("falseNegIntro")))
        
    def force_finder(self): #the user clicks on the magnifier
        value = self.set_type.currentText()
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    Within false negative popup, force type popup opened with category \""+value+"\"\n")
        self.popupForceType = Force_Type_Class(dialog=self.Dialog, categ=value)

class DrawablePictureLabel(QtWidgets.QLabel):
    def __init__(self, parent=None, path=""):
        super().__init__(parent)
        self.click_positions=[]
        self.original_pixmap = QtGui.QPixmap(path)
        self.displayed_width = 0
        self.displayed_height = 0
        self.scaled_pixmap = None
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.updatePixmap()

    def resizeEvent(self, event):
        """Handle resize events to maintain square aspect ratio and track displayed size"""
        super().resizeEvent(event)
        self.updatePixmap()

    def updatePixmap(self):
        """Scale the pixmap to fit the widget while maintaining 1:1 aspect ratio"""
        if self.original_pixmap.isNull():
            return
        
        # Get the available size
        available_width = self.width()
        available_height = self.height()
        
        # Use the smaller dimension to maintain square (1:1) ratio
        size = min(available_width, available_height)
        
        # Store the displayed dimensions for coordinate scaling
        self.displayed_width = size
        self.displayed_height = size
        
        # Scale the pixmap
        self.scaled_pixmap = self.original_pixmap.scaled(
            size, size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # Calculate offset to center of the actual image
            offset_x = (self.width() - self.displayed_width) // 2
            offset_y = (self.height() - self.displayed_height) // 2
            
            # Adjust click position relative to the actual image
            adjusted_x = event.pos().x() - offset_x
            adjusted_y = event.pos().y() - offset_y
            
            # Only register clicks within the actual image bounds
            if 0 <= adjusted_x <= self.displayed_width and 0 <= adjusted_y <= self.displayed_height:
                self.click_positions += [(adjusted_x, adjusted_y)]
                if len(self.click_positions) > 2: #keep only last 2 clicks
                    self.click_positions = [self.click_positions[-2], self.click_positions[-1]]
                self.update()

    def paintEvent(self, event): #draws a crosshair at locations of self.click_positions
        painter = QtGui.QPainter(self)
        
        # Calculate offset to center the image
        offset_x = (self.width() - self.displayed_width) // 2
        offset_y = (self.height() - self.displayed_height) // 2
        
        # Draw the scaled pixmap centered
        if self.scaled_pixmap and not self.scaled_pixmap.isNull():
            painter.drawPixmap(offset_x, offset_y, self.scaled_pixmap)
        
        # Draw crosshairs if present
        if self.click_positions and self.displayed_width > 0:
            pen = QtGui.QPen(QtGui.QColor("red"), 2)
            painter.setPen(pen)
            
            # Draw crosshairs only within the image bounds
            for position in self.click_positions:
                x, y = position
                # Adjust positions by offset
                adjusted_x = x + offset_x
                adjusted_y = y + offset_y
                
                # Draw horizontal line
                painter.drawLine(offset_x, adjusted_y, offset_x + self.displayed_width, adjusted_y)
                # Draw vertical line
                painter.drawLine(adjusted_x, offset_y, adjusted_x, offset_y + self.displayed_height)
        
        painter.end()

class Force_Type_Class(QWidget):
    def __init__(self, dialog, categ):
        super().__init__()
        self.dialog = dialog
        self.ui = ForceTypePopup(categ, None)
        self.ui.imageClicked.connect(self.clicked)
        self.ui.show()

    def clicked(self, clickedName, clickedCat, clickedNum, clickedUid): #the arguments are the actual name and # of die type
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"     Within false negative popup, in force die type popup, user clicked on QLabel "+clickedCat+" "+str(clickedNum)+"\n")
        self.dialog.ui.set_type.setCurrentText(clickedCat)
        self.dialog.ui.set_number.setText(str(clickedNum))
        self.dialog.uid = clickedUid
        self.ui.close()