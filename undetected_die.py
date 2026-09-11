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
import ast #needed by load_preferences, copy-pasted below (same pattern used in display.py/force_sherd.py)

def load_preferences(): #will retrieve some custom setting from a conf file, that the users may want to change (e.g. presence of some features, colors, ...)
    config = {}
    with open("resources/data/preferences.conf", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if len(line)>0 and not line.startswith("#"): #not a comment or empty line
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                config[key] = ast.literal_eval(value)
    return config

config = load_preferences()
MAX_ZOOM = config["max_zoom"] #maximum zoom factor allowed on the die picture
MIN_ZOOM = 1.0 #minimum zoom factor: the default/initial (fit-to-widget) picture size; unzooming stops here so the picture never shrinks below its normal size
ZOOM_STEP = config["zoom_step"] #zoom multiplier applied per mouse wheel "notch" (120 units of angleDelta)



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
        
        self.unkTick = QtWidgets.QCheckBox(text=tr("unknown"))
        bottom_layout.addWidget(self.unkTick)
        self.newTick = QtWidgets.QCheckBox(text=tr("new"))
        bottom_layout.addWidget(self.newTick) #in case of multiple ticks, the order of priority will be unknown>new>actual value, to keep the most likely scenario as a priority
        
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
        self._view_rect = QtCore.QRectF(0, 0, self.original_pixmap.width(), self.original_pixmap.height()) #sub-rectangle of the picture (in ORIGINAL picture pixel coordinates) currently visible in the widget
        self._zoom = MIN_ZOOM #current zoom factor
        self._panning = False #True while a middle-click drag is in progress, used to pan the zoomed picture
        self._pan_last_pos = None #last mouse position seen during the current pan drag
        self.displayed_width = 0
        self.displayed_height = 0
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.updatePixmap()

    def resizeEvent(self, event): #Handle resize events to maintain square aspect ratio and track displayed size
        super().resizeEvent(event)
        self.updatePixmap()

    def updatePixmap(self): #Recompute the fit-to-widget display size; actual (possibly zoomed/panned) rendering happens in paintEvent
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
                if self.displayed_width>0 and self.displayed_height>0 and not self.original_pixmap.isNull():
                    frac_x = adjusted_x / self.displayed_width #position within the displayed square, as a fraction
                    frac_y = adjusted_y / self.displayed_height
                    orig_x = self._view_rect.x() + frac_x * self._view_rect.width() #same position, in ORIGINAL picture pixel coordinates, accounting for the current zoom/pan
                    orig_y = self._view_rect.y() + frac_y * self._view_rect.height()
                    # re-express it in the SAME (unzoomed, whole-image-fit) coordinate space that display.py's accept() already expects, so no change is needed there
                    adjusted_x = orig_x * (self.displayed_width / self.original_pixmap.width())
                    adjusted_y = orig_y * (self.displayed_height / self.original_pixmap.height())
                self.click_positions += [(adjusted_x, adjusted_y)]
                if len(self.click_positions) > 2: #keep only last 2 clicks
                    self.click_positions = [self.click_positions[-2], self.click_positions[-1]]
                self.update()
        elif event.button() == QtCore.Qt.MiddleButton:
            self._panning = True
            self._pan_last_pos = event.pos()

    #the following functions will handle the zoom
    def mouseMoveEvent(self, event): #drags the view around while zoomed in
        if self._panning:
            delta = event.pos() - self._pan_last_pos
            self._pan_last_pos = event.pos()
            self.pan_by(delta.x(), delta.y())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self._panning = False
            self._pan_last_pos = None

    def wheelEvent(self, event): #zooms in/out, centered on the cursor
        self.handle_zoom(event.pos(), event.angleDelta().y())
        event.accept()

    def handle_zoom(self, cursor_pos, angle_delta_y): #returns True if the zoom level actually changed
        global MAX_ZOOM, MIN_ZOOM, ZOOM_STEP
        if self.original_pixmap.isNull() or self.displayed_width==0 or self.displayed_height==0:
            return False
        offset_x = (self.width() - self.displayed_width) // 2
        offset_y = (self.height() - self.displayed_height) // 2
        frac_x = min(1.0, max(0.0, (cursor_pos.x() - offset_x) / self.displayed_width)) #cursor position within the displayed square, clamped to [0,1]
        frac_y = min(1.0, max(0.0, (cursor_pos.y() - offset_y) / self.displayed_height))

        img_w, img_h = self.original_pixmap.width(), self.original_pixmap.height()
        img_x = self._view_rect.x() + frac_x * self._view_rect.width() #same position, in ORIGINAL picture pixel coordinates
        img_y = self._view_rect.y() + frac_y * self._view_rect.height()

        steps = angle_delta_y / 120.0 #120 = one "notch" on most mice wheels
        new_zoom = self._zoom * (ZOOM_STEP ** steps)
        new_zoom = max(MIN_ZOOM, min(MAX_ZOOM, new_zoom))
        if new_zoom == self._zoom: #already at the min/max boundary
            return False
        self._zoom = new_zoom

        new_w = img_w / new_zoom
        new_h = img_h / new_zoom
        new_x = img_x - frac_x * new_w #re-position the view so the SAME picture point stays under the cursor
        new_y = img_y - frac_y * new_h
        new_x = max(0, min(new_x, img_w - new_w)) #keep the view rectangle within the picture bounds
        new_y = max(0, min(new_y, img_h - new_h))

        self._view_rect = QtCore.QRectF(new_x, new_y, new_w, new_h)
        self.update()
        return True

    def pan_by(self, dx_widget, dy_widget): #shifts the current view rectangle by a delta expressed in on-screen (widget) pixels
        if self.original_pixmap.isNull() or self.displayed_width==0 or self.displayed_height==0:
            return
        img_w, img_h = self.original_pixmap.width(), self.original_pixmap.height()
        scale_x = self._view_rect.width() / self.displayed_width #ratio between one on-screen pixel and one picture pixel, at the current zoom level
        scale_y = self._view_rect.height() / self.displayed_height
        new_x = self._view_rect.x() - dx_widget * scale_x #dragging right/down reveals picture content that was hidden on the left/top
        new_y = self._view_rect.y() - dy_widget * scale_y
        new_x = max(0, min(new_x, img_w - self._view_rect.width()))
        new_y = max(0, min(new_y, img_h - self._view_rect.height()))
        self._view_rect.moveTo(new_x, new_y)
        self.update()

    def _click_to_screen(self, stored_xy, offset_x, offset_y): #converts a stored click (in the unzoomed-display coordinate space) back to its current ON-SCREEN position, given the current zoom/pan
        if self.original_pixmap.isNull() or self.displayed_width==0 or self._view_rect.width()==0:
            return None
        sx, sy = stored_xy
        orig_x = sx * (self.original_pixmap.width() / self.displayed_width)
        orig_y = sy * (self.original_pixmap.height() / self.displayed_height)
        frac_x = (orig_x - self._view_rect.x()) / self._view_rect.width()
        frac_y = (orig_y - self._view_rect.y()) / self._view_rect.height()
        screen_x = int(round(offset_x + frac_x * self.displayed_width))
        screen_y = int(round(offset_y + frac_y * self.displayed_height))
        return (screen_x, screen_y)

    def paintEvent(self, event): #draws a crosshair at locations of self.click_positions
        painter = QtGui.QPainter(self)
        
        # Calculate offset to center the image
        offset_x = (self.width() - self.displayed_width) // 2
        offset_y = (self.height() - self.displayed_height) // 2
        
        
        # Draw the current zoom/pan crop of the picture, stretched to fill the displayed square
        if not self.original_pixmap.isNull() and self.displayed_width>0 and self._view_rect.width()>0:
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            target_rect = QtCore.QRectF(offset_x, offset_y, self.displayed_width, self.displayed_height)
            painter.drawPixmap(target_rect, self.original_pixmap, self._view_rect)
        
        
        # Draw crosshairs if present
        if self.click_positions and self.displayed_width > 0:
            pen = QtGui.QPen(QtGui.QColor("red"), 2)
            painter.setPen(pen)
            
            # Draw crosshairs only within the image bounds
            for position in self.click_positions:
                screen_pos = self._click_to_screen(position, offset_x, offset_y) #re-project the stored (unzoomed-space) click onto the CURRENT on-screen position
                if screen_pos is None:
                    continue
                adjusted_x, adjusted_y = screen_pos
                
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