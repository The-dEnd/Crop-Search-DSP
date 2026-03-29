from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from ClickableQLabel import ClickQLabel
from translator import tr
import os, sys, pathlib, ast

dict_types = tr("lMotifs")
reverse_dict_types = {v: k for k, v in dict_types.items()} #reverse dictionnary, used to find back where the user clicked

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
displaySize = config["displaySize"] #bolean to state if you want the application to display the size of all known dies (and the site on which the die was found) in the selector or not



with open("resources/data/sizes.conf", "r") as sizeFile: #adding the sizes to be displayed
    sizeSherd = dict(line.strip().split(':', 1) for line in sizeFile)

def addSize(name, sherdId): #adds the size of the sherds in the name
    global sizeSherd, displaySize
    if sherdId[-3:] == "000":
        return(tr("unknown"))
    try:
        if displaySize:
            [size, site] = sizeSherd[str(sherdId)].replace("\\n","\n").split("$",1)
            return(name +"\n("+ site+")\n"+size)
        else:
            return(name)
    except: #if the key is not present (e.g. size not provided), just display the name
        return(name)
        
        



class ForceTypePopup(QDialog):
    imageClicked = pyqtSignal(str, str, int, str) #message sent to parent when clicked
    def __init__(self, categ, parent=None):
        super().__init__(parent)
        cat = reverse_dict_types[categ] #cat is an integer that is bound to a category, see dict_types
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Pick a symbol")
        lPath = self.getItems(cat)
        nRows=int(len(lPath)/3)
        populator = ClickQLabel()
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(populator,nRows, 7) #force the gridLayout to its maximum extend, nRows rows and 8 columns: three displayed columns with text and picture and two vertical separators (3x2+2=8)
        self.setMinimumSize(1150, 760) #minimum size of the popup to display the window correctly; it is assumed today's computers are >= 2014*768
        

        
        i=0 #counter of %3, for repartition of columns
        
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setLayout(self.gridLayout)
        scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        for oneItem in lPath: # Populate the table with QLabel widgets
            numSubCat = int(oneItem.replace(".png","").replace(".jpg","").replace(".jpeg","")[-3:])
            fullNum = oneItem.replace(".png","").replace(".jpg","").replace(".jpeg","").split("\\")[-1]
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
        clicked_id = clicked_label.objectName()
        if clicked_label:
            self.imageClicked.emit(clicked, clicked_cat, clicked_num, clicked_id)
        
    def getItems(self, family): #lists the images related to forced type
        commonPath = pathlib.Path("resources/media/Die_types/")
        if family == 0: #if not type preselected, take them all
            prefix = ""
        else:
            prefix = str(family)
        lPaths = []
        for aPath in commonPath.glob("*"+prefix+"???.*"):
            lPaths.append(str(aPath))
        lPaths.sort()
        return(lPaths)

