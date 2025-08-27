from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from ClickableQLabel import ClickQLabel
import os, sys, pathlib
from translator import tr, current_language

def loadStylesheet(theme): #loads a QSS file, for a theme, e.g. dark/light
    with open("resources/styles/"+theme+".qss", "r") as file:
        return file.read()

class Ui_themeDialog(QDialog):
    themeClicked = pyqtSignal(str, str) #messaged sent to parent when clicked
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(tr("themeSelector"))
        lPath = self.getItems()
        nRows=int(len(lPath)/2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        i=0 #counter of rows
        
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setLayout(self.gridLayout)
        scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        for anItem in lPath: # Populate the table with QLabel widgets
            basicName = anItem[0]
            fullPath = anItem[1]
            
            oneTheme = ClickQLabel(self.scrollAreaWidgetContents)
            oneTheme.setText(basicName)
            oneTheme.setObjectName(basicName)
            if basicName != "default": #the default theme is empty; if we do not "cheat" with it, it will be displayed with current style, instead of its real default value
                oneTheme.setStyleSheet(loadStylesheet(basicName))
            else:
                oneTheme.setStyleSheet("""color: palette(window-text);background: palette(window);""")
            oneTheme.clicked.connect(self.handle_click)

            self.gridLayout.addWidget(oneTheme,i,0)
            i+=1
        self.gridLayout.update()
        main_layout = QVBoxLayout()
        main_layout.addWidget(scrollArea)
        self.setLayout(main_layout)
        
    def handle_click(self): #manages the clicked event
        clicked_label = self.sender()  # Get the label that was clicked
        clicked = clicked_label.objectName()
        if clicked_label:
             self.themeClicked.emit(clicked, clicked_label.styleSheet())
        
    def getItems(self): #lists the available themes
        commonPath = pathlib.Path("resources/styles/")
        lPaths = []
        for aPath in commonPath.glob("*.qss"):
            fancyName = str(aPath).replace("\\","/").split("/")[-1].replace(".qss","")
            lPaths.append((fancyName,str(aPath)))#add an index for sorting the list
        lPaths.sort(key=lambda x: x[0])
        return(lPaths)
