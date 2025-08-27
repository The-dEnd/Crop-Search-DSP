from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from ClickableQLabel import ClickQLabel
import os, sys, pathlib
from translator import tr, current_language


class RIG_Type(QDialog):
    imageClicked = pyqtSignal(str, str) #messaged sent to parent when clicked
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1020, 760) #minimum size of the popup to display the window correctly; it is assumed today's computers are >= 1024*768
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(tr("pickRIG"))
        self.setStyleSheet("""background-color: #f0f0f0;""") #the RIG pictures have no background; we thus force the background to white, even with global dark mode
        lPath = self.getItems()
        nRows=int(len(lPath)/2)
        populator = ClickQLabel()
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(populator,nRows, 5) #force the gridLayout to its maximum extend, nRows rows and 5 columns: two displayed columns with text and picture and one vertical separator
        
        
        i=0 #counter of %2, for repartition of columns
        
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setLayout(self.gridLayout)
        scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        for anItem in lPath: # Populate the table with QLabel widgets
            oneItem = anItem[1]#remove the index
            typeRIG = oneItem.replace(".png","").replace(".jpg","").replace(".jpeg","").replace("\\","/").split("/")[-1][3:]#remove the index from filename
            oneTextMsg = ClickQLabel(self.scrollAreaWidgetContents)
            oneTextMsg.setText(typeRIG)
            oneTextMsg.setObjectName("txt"+typeRIG)
            oneTextMsg.setStyleSheet("""color: #000000;""")
            oneTextMsg.clicked.connect(self.handle_click)
            onePicMsg = ClickQLabel(self.scrollAreaWidgetContents)
            pixmap = QtGui.QPixmap(oneItem)
            scaled_pixmap = pixmap.scaledToWidth(300, Qt.SmoothTransformation)
            onePicMsg.setPixmap(QtGui.QPixmap(scaled_pixmap))
            onePicMsg.setObjectName("pic"+typeRIG)
            onePicMsg.clicked.connect(self.handle_click)
            
            
            match i%2:
                case 0:
                    self.gridLayout.addWidget(oneTextMsg,int(i/2),0)
                    self.gridLayout.addWidget(onePicMsg,int(i/2),1)
                case 1:
                    self.gridLayout.addWidget(oneTextMsg,int(i/2),3)
                    self.gridLayout.addWidget(onePicMsg,int(i/2),4)
            self.gridLayout.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.VLine), int(i/2), 2) #vertical line
            i+=1
        main_layout = QVBoxLayout()
        main_layout.addWidget(scrollArea)
        self.setLayout(main_layout)
        
    def handle_click(self): #manages the clicked event
        clicked_label = self.sender()  # Get the label that was clicked
        clicked = clicked_label.objectName()[3:]
        clicked_num = clicked.replace(".","").replace("CRAV","").replace("RIG","")
        if clicked_label:
            self.imageClicked.emit(clicked, clicked_num)
        
    def getItems(self): #lists the images related to RIG; images filenames start with a 3-digits index to sert them properly
        commonPath = pathlib.Path("resources/media/RIG_types/")
        lPaths = []
        for aPath in commonPath.glob("*"):
            indexItem = int(str(aPath).replace("\\","/").split("/")[-1][0:3])
            lPaths.append((indexItem,str(aPath)))#add an index for sorting the list
        lPaths.sort(key=lambda x: x[0])
        return(lPaths)
