from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from ClickableQLabel import ClickQLabel
from translator import tr
import os, sys, pathlib

dict_types = tr("lMotifs")
reverse_dict_types = {v: k for k, v in dict_types.items()} #reverse dictionnary, used to find back where the user clicked

with open("resources/data/sizes.conf", "r") as sizeFile: #adding the sizes to be displayed
    sizeSherd = dict(line.strip().split(':', 1) for line in sizeFile)

def addSize(name, sherdId): #adds the size of the sherds in the name
    global sizeSherd
    try:
        return(name+"\n"+sizeSherd[str(sherdId)])
    except: #if the key is not present (e.g. size not provided), just display the name
        return(name)

class ForceTypePopup(QDialog):
    imageClicked = pyqtSignal(str, str, int) #messaged sent to parent when clicked
    def __init__(self, categ, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1020, 760) #minimum size of the popup to display the window correctly; it is assumed today's computers are >= 2014*768
        cat = reverse_dict_types[categ] #cat is an integer that is bound to a category, see dict_types
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Pick a symbol")
        lPath = self.getItems(cat)
        nRows=int(len(lPath)/3)
        populator = ClickQLabel()
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(populator,nRows, 7) #force the gridLayout to its maximum extend, nRows rows and 8 columns: three displayed columns with text and picture and two vertical separators (3x2+2=8)
        

        
        i=0 #counter of %3, for repartition of columns
        
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setLayout(self.gridLayout)
        scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        for oneItem in lPath: # Populate the table with QLabel widgets
            numSubCat = int(oneItem.replace(".png","").replace(".jpg","").replace(".jpeg","")[-3:])
            fullNum = int(oneItem.replace(".png","").replace(".jpg","").replace(".jpeg","")[-4:])
            strCategory = dict_types.get(int(oneItem.replace(".png","").replace(".jpg","").replace(".jpeg","")[-4]))
            oneTextMsg = ClickQLabel(self.scrollAreaWidgetContents)
            oneTextMsg.setText(addSize(strCategory+" "+str(numSubCat),fullNum))
            oneTextMsg.setObjectName("txt"+str(fullNum))
            oneTextMsg.clicked.connect(self.handle_click)
            onePicMsg = ClickQLabel(self.scrollAreaWidgetContents)
            onePicMsg.setPixmap(QtGui.QPixmap(oneItem))
            onePicMsg.setMinimumSize(QtCore.QSize(156, 156))
            onePicMsg.setMaximumSize(QtCore.QSize(156, 156))
            onePicMsg.setScaledContents(True)
            onePicMsg.setObjectName("pic"+str(fullNum))
            onePicMsg.clicked.connect(self.handle_click)
            
            
            match i%3:
                case 0:
                    self.gridLayout.addWidget(oneTextMsg,int(i/3),0)
                    self.gridLayout.addWidget(onePicMsg,int(i/3),1)
                case 1:
                    self.gridLayout.addWidget(oneTextMsg,int(i/3),3)
                    self.gridLayout.addWidget(onePicMsg,int(i/3),4)
                case 2:
                    self.gridLayout.addWidget(oneTextMsg,int(i/3),6)
                    self.gridLayout.addWidget(onePicMsg,int(i/3),7)
            self.gridLayout.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.VLine), int(i/3), 2) #vertical line
            self.gridLayout.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.VLine), int(i/3), 5) #vertical line
            i+=1
        main_layout = QVBoxLayout()
        main_layout.addWidget(scrollArea)
        self.setLayout(main_layout)
        
    def handle_click(self): #manages the clicked event
        clicked_label = self.sender()  # Get the label that was clicked
        clicked = clicked_label.objectName()[-4:]
        clicked_cat = dict_types[int(clicked[0])]
        clicked_num = int(clicked[-3:])
        if clicked_label:
            self.imageClicked.emit(clicked, clicked_cat, clicked_num)
        
    def getItems(self, family): #lists the images related to forced type
        commonPath = pathlib.Path("resources/media/Die_types/")
        if family == 0: #if not type preselected, take them all
            prefix = ""
        else:
            prefix = str(family)
        lPaths = []
        for aPath in commonPath.glob(prefix+"*"):
            lPaths.append(str(aPath))
        lPaths.sort()
        return(lPaths)

