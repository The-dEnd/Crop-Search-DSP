#!/usr/bin/python3

import sys, glob, shutil
import os
os.environ["OPENCV_SKIP_LOAD"] = "1"
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QShortcut, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QFontDatabase, QKeySequence
from PyQt5.QtCore import pyqtSignal, Qt, QObject, QThread, pyqtSignal, QTimer
from main_layout import Ui_Poincons_selector, maxRecent, DrawingOverlay
from display_types import RIG_Type
from loading_screen import Ui_Loading
from license_popup import Ui_licenseDialog
from theme_popup import Ui_themeDialog
from undetected_die import Ui_AddDieDialog
from force_sherd import ForceTypePopup
import picCropper
import time, csv, re
from datetime import datetime
import imagesize
import PIL.Image, PIL.ImageDraw
from ClickableQLabel import ClickQLabel
from translator import tr
from measure_state import MeasureState
import logging.config
from numDecoRegisters import DecorativeRegisterPopup
import ast


import run_ML #HereChangeMLAlgo



#global variables that will be changed programmatically, do not edit
currentIndex = 0 #will keep track of the index of list die to stay in. Data is poped when filled with "suivant/next", but kept (and only this index is increased) when "passer/skip".
MeasureState.setMeasureState = False #boolean keeping track on whether the initial measure ruler is set or not
MeasureState.getMeasureState = False #boolean keeping track on whether the final measure ruler is set or not
sizeSherd = {} #dictionnary containing (existing) sizes of sherds
currentPicture = None #path to the current picture under review; used to check whether one should increas the sherd ID or not
decoRegStatus = {} #for current picture, dictionnary that contains the # of occurences of/decorative registries of a die; if die is not seen yet, it is not present; first time is 0; any number other than 0 means the number of decorative registries for this die (the number of different lines/circlesspirales/... with the same die on the sherd).
project = "" #name of current project

dict_types = tr("lMotifs")
reverse_dict_types = {v: k for k, v in dict_types.items()} #reverse dictionnary



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

normalColor = config["normalColor"] #color for non active dies on the sherd
highlightColor = config["highlightColor"] #color for active die on the sherd
displaySize = config["displaySize"] #bolean to state if you want the application to display the size of all known dies (and the site on which the die was found) in the selector or not

alternativeLogFile = config["alternativeLogFile"] #if main log file has a right access issue, create a specific alternative log file
finalFile = config["finalFile"] #suffix of the file into which output will be written
mlFile = config["mlFile"] #suffix of the file that will contain the output of ML algorithm



def writeLogs(stringToLog): #will handle most of the logging
    global alternativeLogFile
    try:
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+stringToLog)
    except: #if there is an error with the normal log file
        if alternativeLogFile == "": #create the alternative log file if it doesn't exist already
            alternativeLogFile = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"logs.txt"
            with open(alternativeLogFile, "w") as logFile:
                logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"Error writing to main file (to be investigated); resorting to alternative logFile")
        with open(alternativeLogFile, "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+stringToLog)



class TerminateExeption(Exception): #custom error class to be triggered in order to easiily catch and cancel functions that triger the error (e.g. the user clicks next without selecting a sherd type)
    pass


class Selector_Main(QWidget):
    def __init__(self):
        global rawData
        super().__init__()
        self.ui = Ui_Poincons_selector()
        self.ui.setupUi(self,)  
        self.overlay = DrawingOverlay(self)
        self.overlay.setGeometry(self.ui.die_picture.geometry())
        self.overlay.raise_()
        self.ui.die_picture.installEventFilter(self) #listen to die_picture modification, to adapt the overlay accordingly
        self.newPart()
        self.popupTypology = None #additional argument for child window (popups) that displays the shape/typology of pottery (RIG/CRAV)
        self.licensePopup = None #additional argument for child window (popups) that displays the license
        self.themePopup = None #additional argument for child window (popups) that displays the license
        self.undetectedPopup = None #additional argument for child window (popups) that displays the "untetected die?" dialog
        shortcutFind = QShortcut(QKeySequence("Ctrl+F"),self)
        shortcutFind.activated.connect(self.search)
        shortcutPrev = QShortcut(QKeySequence("Ctrl+Z"),self)
        shortcutPrev.activated.connect(self.previous)
        self.show() #show the window
        self.data = [rawData[0][0][0], rawData[0][0][1], rawData[0][0][2], rawData[0][0][3]] #minimum data necessary for child window (e.g. Undetected_Die)
        writeLogs("    Application started successfully\n")

    def eventFilter(self, watched, event): #monitor die_picture resize, to adapt overlay correspondingly
        if watched == self.ui.die_picture and event.type() in (QtCore.QEvent.Resize, QtCore.QEvent.Move):
            self.overlay.updateGeometry()
        return super().eventFilter(watched, event)


    def resizeEvent(self, event):#when window is resized, realigns visual items
        super().resizeEvent(event)

        window_width = self.width()
        proportional_max_width = int(window_width * 0.7)  #% of total width

        self.ui.center_panel.setMaximumWidth(proportional_max_width)


    def get_values(self): #retrieves the data from users input in the GUI
        writeLogs("    Retrieving values...\n")
        option1 = self.ui.option1.isChecked()
        option2 = self.ui.option2.isChecked()
        option3 = self.ui.option3.isChecked()
        option4 = self.ui.option4.isChecked()
        optionOriginal = self.ui.new_radio.isChecked()
        optionUnknown = self.ui.unknown.isChecked()
        optionForce = self.ui.force.isChecked()
        optionFalsePos = self.ui.false_pos.isChecked()
        typeDie = "" #type of the die (rouelle, palmette, ...)
        numberDie = "0" #number of the die type (1, 2, 3, ...)
        country = ""
        region = ""
        department = ""
        municipality = ""
        site = ""
        x = ""
        y = ""
        z = ""
        location = (False, False, False, False)#edge, belly, bottom, handle
        option = None #ticked radio button; it will be used in a case statement to retrieve sherd type and number
        resultML = None #indicator to remember if the ML algorithm was more or less correct in its assessment
        if option1:
            option = 1
            resultML = "1"
        if option2:
            option = 2
            resultML = "2"
        if option3:
            option = 3
            resultML = "3"
        if option4:
            option = 4
            resultML = "4"
        if optionOriginal:
            option = 9
            resultML = "unguessable"
        if optionUnknown:
            option = 0
            resultML = "unguessable"
        if optionForce:
            option = 8
            resultML = "other"
        if optionFalsePos:
            option = 10
            resultML = "FP"
        match option:
            case None:#there is no ticked radio button
                basicWarning(tr("noRadio"))
                writeLogs("    Next button clicked without any radio button on sherd type selected\n")
                raise TerminateExeption("No sherd type")
            case 1:
                typeDie = self.ui.option1_name.text().split(" ")[0]
                numberDie = self.ui.option1_name.text().split(" ")[1].split("\n")[0]
            case 2:
                typeDie = self.ui.option2_name.text().split(" ")[0]
                numberDie = self.ui.option2_name.text().split(" ")[1].split("\n")[0]
            case 3:
                typeDie = self.ui.option3_name.text().split(" ")[0]
                numberDie = self.ui.option3_name.text().split(" ")[1].split("\n")[0]
            case 4:
                typeDie = self.ui.option4_name.text().split(" ")[0]
                numberDie = self.ui.option4_name.text().split(" ")[1].split("\n")[0]
            case 0:#unkown
                if self.ui.new_type.currentIndex() != 0:
                    typeDie = self.ui.new_type.currentText()
                else:
                    typeDie = tr("unknown")
                numberDie = tr("unknown")
            case 8:#force
                typeDie = self.ui.force_type.currentText()
                numberDie = self.ui.force_number.text()
            case 9:#original (inedit) sherd for a type
                typeDie = self.ui.new_type.currentText()
                numberDie = tr("new")
            case 10: #false positive; actually not a sherd
                typeDie = "false positive (not a sherd)"
        comment = self.ui.comment_box.toPlainText().replace(";",",").replace("\n","\t").replace("\r","") #semi-collon are reserved as separators in output CSV, so we sanitize the field
        country = self.ui.country.toPlainText()
        region = self.ui.region.toPlainText()
        department = self.ui.department.toPlainText()
        municipality = self.ui.municipality.toPlainText()
        site = self.ui.site.toPlainText()
        x = self.ui.lambert_X.toPlainText()
        y = self.ui.lambert_Y.toPlainText()
        z = self.ui.lambert_Z.toPlainText()
        fait = self.ui.numFait.toPlainText()
        us = self.ui.numUs.toPlainText()
        craType = self.ui.mode_CRA.currentText()
        craNum = self.ui.rig_num.toPlainText()
        if self.ui.unknownCRA.isChecked():
            craNum = tr("otherType")
        author = self.ui.author.displayText()
        lLocations = []
        if self.ui.checkBox_edge.isChecked():
            lLocations.append(tr("edge"))
        if self.ui.checkBox_belly.isChecked():
            lLocations.append(tr("belly"))
        if self.ui.checkBox_handle.isChecked():
            lLocations.append(tr("handle"))
        if self.ui.checkBox_bottom.isChecked():
            lLocations.append(tr("bottom"))
        location = "/".join(lLocations)#merge the active parts of edge/belly/bottom/handle
        writeLogs("    Retrieved values"+";".join([typeDie, numberDie, comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author, resultML])+"\n")
        return(typeDie, numberDie, comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author, resultML)

    def search_clicked(self): #handles the "next" button: logs the files, processes the user inputs, and opens a new sherd
        global fold, currentIndex
        writeLogs("    Button \"Search\" clicked\n")
        self.search()

    def prev_clicked(self): #handles the "next" button: logs the files, processes the user inputs, and opens a new sherd
        global fold, currentIndex
        writeLogs("    Button \"Previous\" clicked\n")
        self.previous()


    def next_clicked(self): #handles the "next" button: logs the files, processes the user inputs, and opens a new sherd
        global fold, currentIndex
        writeLogs("    Button \"Next\" clicked\n")
        try: #the checks for data consistency is performed before any "destructive" action (e.g. poping lines from data) is performed
            output = self.get_values() #the data retrieved from the ticked boxes in GUI
        except:
            return() #if an error occurs (e.g. clicking "next" without selecting sherd type), pretend the user never clicked by stoping the function
        writeLogs("    Poppping item #"+str(currentIndex)+"\n")
        currentLine = rawData.pop(currentIndex) #remove the reviewed item from list of data to review
        numDie,numDecor,numPhoto,namePhoto,x1,y1,x2,y2 = currentLine[0][0],currentLine[0][1],currentLine[0][2],currentLine[0][3],currentLine[0][36],currentLine[0][37],currentLine[0][38],currentLine[0][39]
        if self.ui.sherdTxtId.text() != "":
            numDecor = self.ui.sherdTxtId.text()
        if self.ui.dieTxtId.text() != "":
            numDie = self.ui.dieTxtId.text()
        self.checkDecorativeRegister(output[0]+output[1], namePhoto) #checkDecorativeRegister checks whether there are multiple decorative registers for the same die, and updates the comment field accordinglydecoRegStatus
        writeLogs("    Line to write:\n"+str([output,numDie,numDecor,numPhoto,namePhoto,fold,[x1,y1,x2,y2]])+"\n")
        writeLogs("    Status of index: "+str(currentIndex)+" out of "+str(len(rawData))+"\n")
        output_application_files(output,numDie,numDecor,numPhoto,namePhoto)
        output_application_csv(output,numDie,numDecor,numPhoto,namePhoto,fold,[x1,y1,x2,y2])
        if self.ui.force_location.isChecked():
            self.set_location()
        self.updateRecent(output[0:2]) #add the newest RIG type to the recent file
        self.lastPicDecorativeRegister(namePhoto)
        self.newPart() #call next sherd


    def skip_clicked(self): #handles the "skip" button: logs the action and opens a new sherd
        global currentIndex
        currentIndex += 1 #do not erase the list, but ignore its index
        if self.ui.force_location.isChecked():
            self.set_location()
        writeLogs("    Button \"Skip\" clicked\n")
        writeLogs("    Status of index: "+str(currentIndex)+" out of "+str(len(rawData))+"\n")
        self.newPart() #call next sherd

    def exit_clicked(self): #handles the "exit" button: logs the action and closes the application
        writeLogs("    Button \"Exit\" clicked\n")
        QApplication.exit(200)

    def newPart(self):#initialization of a new die/sherd to review in the GUI
        global currentIndex, rawData, currentPicture, decoRegStatus
        writeLogs("    Status of index:"+str(currentIndex)+"out of "+str(rawData)+"\n")
        if len(rawData)==currentIndex: #check if the end of pictures list has been reached
            writeLogs("    End of pictures round, "+str(len(rawData))+"remaining to be resent\n")
            if len(rawData)>0:
                currentIndex = 0 #restart from beginning, to resend the skipped items
            else:
                writeLogs("    All data reviewed! End of batch.\n")
                warning_end_of_data = QMessageBox()
                warning_end_of_data.setText(tr("endMsg"))
                warning_end_of_data.exec()
                QApplication.exit(205) #restart the application
                return()
        sherdNum, dieNum, numPic, picture, option1id, option1, option1model, proba1, option2id, option2, option2model, proba2, option3id, option3, option3model, proba3, option4id, option4, option4model, proba4, commentML, xLeft, yBot, xRight, yTop, aux1 = prepareData()
        self.data = [sherdNum, dieNum, numPic, picture]
        self.picture = picture
        writeLogs("=======================================\n")
        writeLogs("    New picture loading:"+"tmp/"+os.path.basename(picture)+"\n")
        try:
            setCurrent("tmp/"+os.path.basename(picture),(xLeft, yBot, xRight, yTop)) #the picture displayed is not the OG picture, but a version altered to contain all sherds cornered
        except: #in case of a rollback of an "old" picture, it may not be in tmp anymore; in that case, we use the default pic
            writeLogs("    The picture was not found in tmp folder, defaulting to OG picture:"+picture+"\n")
            setCurrent(picture,(xLeft, yBot, xRight, yTop))
            pass
        self.ui.die_picture.setPixmap(QtGui.QPixmap("tmp/current.png"))
        self.overlay.raise_()
        self.ui.comment_box.setText("")
        self.ui.option1.setHidden(False)
        self.ui.option2.setHidden(False)
        self.ui.option3.setHidden(False)
        self.ui.option4.setHidden(False)
        self.ui.option1_name.setText(addSize(option1id))
        self.ui.option2_name.setText(addSize(option2id))
        self.ui.option3_name.setText(addSize(option3id))
        self.ui.option4_name.setText(addSize(option4id))
        self.ui.option1_model.setPixmap(QtGui.QPixmap(option1model))
        self.ui.option2_model.setPixmap(QtGui.QPixmap(option2model))
        self.ui.option3_model.setPixmap(QtGui.QPixmap(option3model))
        self.ui.option4_model.setPixmap(QtGui.QPixmap(option4model))
        self.ui.option1_percent.setText(proba1)
        self.ui.option2_percent.setText(proba2)
        self.ui.option3_percent.setText(proba3)
        self.ui.option4_percent.setText(proba4)
        self.ui.reference1.setText("")
        with open("resources/data/recent_rig.conf","r") as recentFile:
            self.ui.recentChoices.clear()
            self.ui.recentChoices.addItem(tr("recent"))
            i = 1 #index of the drop down list
            for oneItem in recentFile.readlines():
                self.ui.recentChoices.addItem(oneItem.replace("\n",""))
        if len(commentML)>0:
            self.ui.reference2.setText(tr("algoComm")+commentML)
        else:
            self.ui.reference2.setText("")
        self.ui.mode_CRA.setCurrentText(tr("undet")) #set CRA mode to "indéterminé" instead of the default index "A"
        self.ui.rig_num.setPlainText("")
        if proba1 == "": #if some suggestions have no proba, hide their options
            self.ui.option1.setHidden(True)
        if proba2 == "":
            self.ui.option2.setHidden(True)
        if proba3 == "":
            self.ui.option3.setHidden(True)
        if proba4 == "":
            self.ui.option4.setHidden(True)
        with open("resources/data/legal.conf","r") as file_legal: #legal mentions
            legal = file_legal.read()
        self.ui.LegalMentions.setText(legal)
        self.get_location()
        for aRadioButton in [self.ui.force_location,self.ui.option1,self.ui.option2,self.ui.option3,self.ui.option4,self.ui.force,self.ui.unknown,self.ui.new_radio,self.ui.false_pos]: #untick all radio buttons
            aRadioButton.setAutoExclusive(False)
            aRadioButton.setChecked(False)
            aRadioButton.setAutoExclusive(True)
        self.ui.force_type.setCurrentIndex(0)
        self.ui.force_number.setText("")
        if len(aux1)>0: #if the entry comes from a rollback, populate it with current information
            aux1list = aux1.split("$") #split all values from aux1 back into a list
            self.ui.comment_box.setPlainText(aux1list[0])
            self.ui.country.setPlainText(aux1list[1])
            self.ui.region.setPlainText(aux1list[2])
            self.ui.department.setPlainText(aux1list[3])
            self.ui.municipality.setPlainText(aux1list[4])
            self.ui.site.setPlainText(aux1list[5])
            self.ui.lambert_X.setPlainText(aux1list[6])
            self.ui.lambert_Y.setPlainText(aux1list[7])
            self.ui.lambert_Z.setPlainText(aux1list[8])
            self.ui.numFait.setPlainText(aux1list[9])
            self.ui.numUs.setPlainText(aux1list[10])
            self.ui.mode_CRA.setCurrentText(aux1list[11])
            self.ui.rig_num.setPlainText(aux1list[12])
            self.ui.author.setText(aux1list[14])
            locationsDie = aux1list[13].split("/")
            for x in locationsDie:
                if x == tr("edge"):
                    self.ui.checkBox_edge.setChecked(True)
                if x == tr("belly"):
                    self.ui.checkBox_belly.setChecked(True)
                if x == tr("handle"):
                    self.ui.checkBox_handle.setChecked(True)
                if x == tr("bottom"):
                    self.ui.checkBox_bottom.setChecked(True)
        if sherdNum == "" and currentPicture != picture:
            self.ui.sherdTxtId.setText(incrementId(self.ui.sherdTxtId.text()))
            self.ui.checkBox_edge.setChecked(False)
            self.ui.checkBox_belly.setChecked(False)
            self.ui.checkBox_handle.setChecked(False)
            self.ui.checkBox_bottom.setChecked(False)
        if dieNum == "":
            self.ui.dieTxtId.setText(incrementId(self.ui.dieTxtId.text()))
        if currentPicture != picture:
            decoRegStatus = {}
        currentPicture = picture

    
    def show_types(self):#open the popup with types/shapes of pottery (RIG/CRAV)
        writeLogs("    Button \"Display Types\" clicked\n")
        self.popupTypology = Display_Types(self)
        
    def force_RIG_type(self, typ): #a user clicked a text/picture in the Display_Types window; set the RIG type to it
        writeLogs("    Display_Types windows sends a message to change RIG/CRAV type to "+typ+"\n")
        self.ui.rig_num.setPlainText(typ)
    
    def popup_license(self):#open the popup with licenses
        writeLogs("    Button \"Show license\" clicked\n")
        self.licensePopup = License_Popup()
        with open("resources/data/licenses.conf", "r", encoding='utf-8') as license_file:
            lic = license_file.read()
        self.licensePopup.ui.label.setText(lic)
        self.licensePopup.show()
        
    def popup_theme(self):#open the popup with theme picker
        writeLogs("    Button \"Theme picker\" clicked\n")
        self.themePopup = Theme_Popup()
        
    def false_negative(self):#open the popup to report an undetected sherd
        writeLogs("    Button \"Undetected die\" clicked\n")
        self.undetectedPopup = Undetected_Die(self.picture, parent=self)
        self.undetectedPopup.show()

    def get_location(self):#retrieves the saved geographical location of reviewed site
        with open("resources/data/default_location.conf","r") as locFile:
            loc = locFile.read().split(",")
        self.ui.country.setPlainText(loc[0])
        self.ui.region.setPlainText(loc[1])
        self.ui.department.setPlainText(loc[2])
        self.ui.municipality.setPlainText(loc[3])
        self.ui.site.setPlainText(loc[4])
        self.ui.lambert_X.setPlainText(loc[5])
        self.ui.lambert_Y.setPlainText(loc[6])
        self.ui.lambert_Z.setPlainText(loc[7])
    
    def set_location(self):#overwrites the geographical location of reviewed site
        writeLogs("    New default location saved.")
        ctry = self.ui.country.toPlainText()
        rg = self.ui.region.toPlainText()
        dpt = self.ui.department.toPlainText()
        mnc = self.ui.municipality.toPlainText()
        st = self.ui.site.toPlainText()
        x = self.ui.lambert_X.toPlainText()
        y = self.ui.lambert_Y.toPlainText()
        z = self.ui.lambert_Z.toPlainText()
        with open("resources/data/default_location.conf","w") as locFile:
            locFile.write(",".join([ctry,rg,dpt,mnc,st,x,y,z]))

    def history_force(self): #the user uses an historical item from recent history list
        new_value = self.ui.recentChoices.currentText()
        if new_value != tr("recent"):
            writeLogs("    User picked an historical value "+new_value+"\n")
            rigNum = new_value.split(" ")[-1]
            rigType = " ".join(new_value.split(" ")[:-1])
            self.ui.force_number.setText(rigNum)
            self.ui.force_type.setCurrentText(rigType)
            self.ui.force.setChecked(True)

    def set_scale(self): #manage the displaying of the scale ruler on the picture
        self.ui.returnSizeButton.blockSignals(True) #prevent recursive signals while playing with checked/unchecked status
        self.ui.setScaleButton.blockSignals(True) #prevent recursive signals while playing with checked/unchecked status
        if self.ui.setScaleButton.isChecked():
            self.ui.setScaleButton.setChecked(False)
            MeasureState.setMeasureState = False
        else:
            self.ui.setScaleButton.setChecked(True)
            MeasureState.setMeasureState = True
        self.ui.returnSizeButton.setChecked(False)
        MeasureState.getMeasureState = False
        self.ui.returnSizeButton.blockSignals(False)
        self.ui.setScaleButton.blockSignals(False)
        writeLogs("    Set scale button clicked; status is GET "+str(MeasureState.getMeasureState)+"; SET "+str(MeasureState.setMeasureState)+"\n")
        
    def retrieve_scale(self): #manage the measurement ruler on the picture
        self.ui.returnSizeButton.blockSignals(True) #prevent recursive signals while playing with checked/unchecked status
        self.ui.setScaleButton.blockSignals(True) #prevent recursive signals while playing with checked/unchecked status
        if self.ui.returnSizeButton.isChecked():
            self.ui.returnSizeButton.setChecked(False)
            MeasureState.getMeasureState = False
        else:
            self.ui.returnSizeButton.setChecked(True)
            MeasureState.getMeasureState = True
        self.ui.setScaleButton.setChecked(False)
        MeasureState.setMeasureState = False
        self.ui.returnSizeButton.blockSignals(False)
        self.ui.setScaleButton.blockSignals(False)
        writeLogs("    Set scale button clicked; status is GET "+str(MeasureState.getMeasureState)+"; SET "+str(MeasureState.setMeasureState)+"\n")

    def edit_scale(self): #refreshes the display when scale value is updated
        self.overlay.refresh_length()

    def search(self): #users does a Ctrl+F to search for a previous item
        global currentIndex
        dialog = SearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            search_text = dialog.textEdit.text()
        found=False
        new_data = []
        try:
            with open(finalFile, "r", encoding='utf-8') as final_output:
                reader = csv.reader(final_output, delimiter=";")
                for row in reversed(list(reader)):
                    if len(row)>1 and row[1]==search_text and not(found): #only copy and remove the first occurence (from the end)
                        found=True
                        outputToTransform = row
                    else:
                        new_data.append(row)
            if not(found): #die number not found
                basicWarning(tr("searchNotFound"))
                return()
        except:
            basicWarning(tr("searchNotFound"))
            return()

        with open(finalFile, "w", encoding='utf-8') as final_output: #now we write back the file, minus the row we found
            writer = csv.writer(final_output, delimiter=";")
            for anItem in reversed(new_data):
                if len(anItem)>1: #remove empty lines if there are
                    writer.writerow(anItem)
        transformed_data = self.convert_finalOutput_to_MLOutput(outputToTransform)
        currentIndex = max(0, currentIndex-1)#rollback from one index
        rawData.insert(currentIndex, [transformed_data]) #insert the item in the index
        self.newPart()


    def previous(self): #users does a Ctrl+Z to search for a previous item
        global currentIndex
        new_data = []
        try:
            with open(finalFile, "r", encoding='utf-8') as final_output:
                output_read = final_output.readlines()
                if len(output_read) > 0:
                    outputToTransform = output_read[-1].split(";") #first row from the bottom was the last one your got
                    new_data.append(outputToTransform)
                else: 
                    basicWarning(tr("previousNotFound"))
                    return()
        except:
            basicWarning(tr("previousNotFound"))
            return()

        with open(finalFile, "w", encoding='utf-8') as final_output: #now we write back the file, minus the row we found
            writer = csv.writer(final_output, delimiter=";")
            for anItem in reversed(new_data):
                if len(anItem)>1: #remove empty lines if there are
                    writer.writerow(anItem)
        transformed_data = self.convert_finalOutput_to_MLOutput(outputToTransform)
        currentIndex = max(0, currentIndex-1)#rollback from one index
        rawData.insert(currentIndex, [transformed_data]) #insert the item in the index
        self.newPart()



    def convert_finalOutput_to_MLOutput(self, listFinalOutput): #converts back the final output to the ML output data file; this unfortunately stripes most of added information (e.g. location, ...) from the file
        #TODO: merge all other columns, put them in "Aux1" to keep track of e.g. location in case of a rollback, and change function newPart accordingly (if aux1<>"", then popuplate the view with this data)
        global reverse_dict_types
        listMLOutput = [''] * 40
        listMLOutput[0] = listFinalOutput[0]
        listMLOutput[1] = listFinalOutput[1]
        listMLOutput[2] = listFinalOutput[2]
        listMLOutput[3] = listFinalOutput[3]
        listMLOutput[5] = listFinalOutput[4]+" "+listFinalOutput[5]
        listMLOutput[6] = "1"
        listMLOutput[25] = tr("rollbackMsg")
        listMLOutput[36] = listFinalOutput[21]
        listMLOutput[37] = listFinalOutput[22]
        listMLOutput[38] = listFinalOutput[23]
        listMLOutput[39] = listFinalOutput[24]
        listMLOutput[26] = "$".join(listFinalOutput[6:21]) #populate field Aux1 with all the other informations
        #the following lines will convert listFinalOutput[4:5] to the 4-digits ML output format, e.g. ["rouelle","8"] => 1008
        codedType = str(reverse_dict_types[listFinalOutput[4]])
        exactDie = "000"+listFinalOutput[5] #left-zero-padding, to ensure that e.g. 8 => 008, and 22 => 022
        listMLOutput[4] = codedType+exactDie[-3:]
        return(listMLOutput)



    def force_finder(self): #the user clicks on the magnifier
        value = self.ui.force_type.currentText()
        writeLogs("    Force type popup opened with category \""+value+"\"\n")
        self.popupForceType = Force_Type_Class(self, value)

    def new_changed_type(self):#function to log user actions, and automatically switch radiobox accordingly
        value = self.ui.new_type.currentText()
        writeLogs("    Type of section \"inedit/indetermine\" changed to \""+value+"\"\n")
        if not(self.ui.new_radio.isChecked()) and not(self.ui.unknown.isChecked()): #if one of the 2 radio box related to this drop down list is not fixed
            self.ui.unknown.setChecked(True)

    def force_changed_type(self):#function to log user actions, and automatically switch radiobox accordingly
        value = self.ui.force_type.currentText()
        writeLogs("    Type of section \"force\" changed to \""+value+"\"\n")
        self.ui.force.setChecked(True)

    def force_changed_number(self):#function to log user actions, and automatically switch radiobox accordingly
        value = self.ui.force_number.text()
        writeLogs("    Number of section \"force\" changed to \""+value+"\"\n")
        self.ui.force.setChecked(True)

    def comment_edited(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.comment_box.toPlainText()
        writeLogs("    Comment box changed to \""+value+"\"\n")
            
    def false_positive(self):#open the popup to report an undetected sherd
        writeLogs("    Button \"Not a die\" clicked\n")
            
    def radioboxUnk_ticked(self):#function to log user actions; no direct fonctionnal use
        writeLogs("    Unkown radio button ticked\n")

    def radioboxFor_ticked(self):#function to log user actions; no direct fonctionnal use
        writeLogs("    Force radio button ticked\n")

    def radioboxNew_ticked(self):#function to log user actions; no direct fonctionnal use
        writeLogs("    Inedit/new radio button ticked\n")

    def radiobox1_ticked(self):#function to log user actions; no direct fonctionnal use
        writeLogs("    Option1 radio button ticked\n")

    def radiobox2_ticked(self):#function to log user actions; no direct fonctionnal use
        writeLogs("    Option2 radio button ticked\n")

    def radiobox3_ticked(self):#function to log user actions; no direct fonctionnal use
        writeLogs("    Option3 radio button ticked\n")

    def radiobox4_ticked(self):#function to log user actions; no direct fonctionnal use
        writeLogs("    Option4 radio button ticked\n")

    def cra_changed_type(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.mode_CRA.currentText()
        writeLogs("    CRA type changed to \""+value+"\"\n")

    def cra_changed_number(self):#function to log user actions, and automatically switch checkbox accordingly
        value = self.ui.rig_num.toPlainText()
        writeLogs("    CRA number changed to \""+value+"\"\n")
        self.ui.unknownCRA.setChecked(False)

    def country_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.country.toPlainText()
        writeLogs("    Country name changed to \""+value+"\"\n")

    def region_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.region.toPlainText()
        writeLogs("    Region name changed to \""+value+"\"\n")

    def department_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.department.toPlainText()
        writeLogs("    Department name changed to \""+value+"\"\n")

    def municipality_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.municipality.toPlainText()
        writeLogs("    Municipality name changed to \""+value+"\"\n")

    def site_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.site.toPlainText()
        writeLogs("    Site name changed to \""+value+"\"\n")

    def x_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.lambert_X.toPlainText()
        writeLogs("    Lambert-X changed to \""+value+"\"\n")

    def y_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.lambert_Y.toPlainText()
        writeLogs("    Lambert-Y changed to \""+value+"\"\n")

    def z_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.lambert_Z.toPlainText()
        writeLogs("    Lambert-Z changed to \""+value+"\"\n")
            
    def fait_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.numFait.toPlainText()
        writeLogs("    Fait # changed to \""+value+"\"\n")
            
            
    def us_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.numUs.toPlainText()
        writeLogs("    US # changed to \""+value+"\"\n")

    def location_changed(self):#function to log user actions; no direct fonctionnal use
        value = "edge-"+str(self.ui.checkBox_edge.isChecked())+", belly-"+str(self.ui.checkBox_belly.isChecked())+", bottom-"+str(self.ui.checkBox_bottom.isChecked())+", handle-"+str(self.ui.checkBox_handle.isChecked())
        writeLogs("    Sherd locations changed to \""+value+"\"\n")

    def unknownCRA_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.unknownCRA.isChecked()
        writeLogs("    CRA type unknown status changed to \""+str(value)+"\"\n")
        
    def author_changed(self):#function to log user actions; no direct fonctionnal use
        value = self.ui.author.displayText()
        writeLogs("    Author changed to \""+value+"\"\n")

    def updateRecent(self, lValues):#updates the recent_rig.conf file with latest value selected
        with open("resources/data/recent_rig.conf", "r") as recentFile:
            lines = recentFile.readlines()
        fancyName = (" ".join(lValues)+"\n").replace("é","e")
        if fancyName in lines:
            lines.remove(fancyName) #avoid duplicates
        lines.insert(0,fancyName) #add new item on top
        if "" in lines:
            lines.remove("")#remove empty lines
        while(len(lines)>maxRecent): #if too many items, remove last item
            a = lines.pop()
        with open("resources/data/recent_rig.conf", "w") as recentFile:
            recentFile.writelines(lines)
        writeLogs("    History updated to "+str(lines)+"\n")

    def checkDecorativeRegister(self, die, photo): #updates the decoRegStatus dictionnary
        global decoRegStatus
        if die not in decoRegStatus: #die not seen yet; initializing the dictionnary entry...
            decoRegStatus[die]=1
        else:
            decoRegStatus[die]+=1 #die already seen, and confirmed as a single decorative registry; nothing to do

    def lastPicDecorativeRegister(self, photo): #checks whether we are at the last die on the picture, and triggers final
        global rawData, currentIndex, decoRegStatus
        try:
            nextPic = rawData[currentIndex][0][3]
        except: #the above line will fail when rawData is empty
            nextPic = "Totally not the same file"
        writeLogs("    Checking whether this is the last die on the picture... "+str(nextPic)+" VS "+str(photo)+"\n")
        if photo != nextPic: #time to check the dictionnary
            for die, value in decoRegStatus.items():
                if value>1:
                    dialog = DecorativeRegisterPopup(die=die)
                    if dialog.exec() == QDialog.Accepted:
                        number = dialog.get_value()
                    writeLogs("    Die "+die+" present in "+str(number)+" decorative registry; rolling back to get its previous occurence...\n")
                    decoRegStatus[die] = number
                    message = str(number)
                    self.updateDecoReg(die, message, photo)
                else:
                    writeLogs("    No repetition of die in decorative registry.\n")
                    self.updateDecoReg(die, "1", photo)
        writeLogs("    Last die of picture check performed!\n")
                        
    def updateDecoReg(self, die, msg, photo): #updates the Final_Output.csv file with a message stating that there are multiple decorative registries on the same die
        global finalFile
        rowsOfReg = []
        with open(finalFile, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=";")
            data = list(reader)
        with open(finalFile, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=";")
            for row_index, row in enumerate(reader):
                if len(row) > 1:
                    if row[3] == photo and row[4]+row[5]==die:
                        rowsOfReg.append(row_index) #index of one line to be updated: the die is the same, and we are in the correct picture
        writeLogs("    During rollback, following rows were spotted as referring to the same sherd: "+str(rowsOfReg)+"; rewritting everything...\n")
        for oneIndex in rowsOfReg: #edit the cell with the message in previous occurences of same picture (i.e. same sherd) + same die
            if len(data[oneIndex])>=27: #if CSV list is not long enough, increase its size
                data[oneIndex][26]=msg
            else:
                data[oneIndex] +=[""]*(26) #blank padding, in case
                data[oneIndex][26]=msg
        with open(finalFile, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerows(data)



class Init_Window(QWidget):
    #following code is to open a folder selector, start the ML algorithm on its content, and display a loading window
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Loading()
        self.ui.setupUi(self,)
        self.thread = None
        self.worker = None
        
    def start(self): #the Qt window tends to initialise too slowly compared to the opening of select_files, which triggers problems; thus we add a listener for readiness befor starting select_files
        QTimer.singleShot(0, self.delayed_start)


    def nameProject(self): #popup that asks the user for a project name for the new project
        global mlFile, project
        nameDialog = QDialog()
        layout = QVBoxLayout()
        nameDialog.setLayout(layout)
        layout.addWidget(QLabel(tr("nameProject")))
        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        button = QPushButton("OK")
        button.clicked.connect(nameDialog.accept)
        layout.addWidget(button)
        newNameRaw = ""
        if nameDialog.exec_() == QDialog.Accepted:
            newNameRaw = "".join(line_edit.text())
        newNameClean = re.sub(r'[^a-zA-Z0-9_ ]+', '', newNameRaw.replace(" ", "_"))[0:25].strip("_")
        project = newNameClean
        writeLogs("    New project name: "+newNameClean+".\n")
        mlFile = newNameClean+"_"+mlFile #prepare a new file to store ML output
        writeLogs("    New project file: "+mlFile+".\n")


    def delayed_start(self): #the Qt window tends to initialise too slowly compared to the opening of select_files, which triggers problems; thus we add a listener for readiness before starting select_files
        self.show()
        resume = self.resumeConfirm()
        global fold, mlFile, project, finalFile
        if len(resume)>0: #we skip the ML part
            mlFile = resume
            finalFile = project.strip("_")+"_"+finalFile
            writeLogs("    Resuming case "+project.strip("_")+".\n")
            self.thread = QThread()
            self.thread.started.connect(self.on_ml_finished)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
        else:
            fold = self.select_files()
            lPaths = [] #list of pictures in the folder
            if len(fold)==0: #if user closed the popup without chosing a folder to handle
                writeLogs("    No folder chosen, application exits...\n")
                warning_exit = QMessageBox()
                warning_exit.setText(tr("errorNoFold"))
                warning_exit.exec()
                QApplication.exit(404)
                sys.exit()
            else:
                self.nameProject()
                finalFile = project+"_"+finalFile
                for aFile in os.listdir(fold): #get all pictures
                    if aFile.endswith((".png", ".jpg", ".PNG", ".JPG", ".jpeg", ".JPEG")):
                        lPaths.append(fold+"/"+aFile)
                if len(lPaths)==0:
                    writeLogs("    No picture in chosen folder root, application exits...\n")
                    warning_exit = QMessageBox()
                    warning_exit.setText(tr("errorNoPic"))
                    warning_exit.exec()
                    QApplication.exit(204)
                    sys.exit()
                else:
                    self.setup_loading_window()
                    self.show()
                    writeLogs("    ML algorithm started, for case "+mlFile+".\n")
                    self.loadML(lPaths)


                
    def resumeConfirm(self): #returns the ML_output file if the user wants to reload previous session (if it exists), and empty string else
        (output_ML_exists, lenCsv, dateModif, lMlFiles) = outputML_CSV_exists()
        if output_ML_exists: #if remaining data form last session, start by asking if the system should run this last session
            lFiles = [(lMlFiles[i], lenCsv[i], dateModif[i]) for i in range(len(lenCsv))]
            global project
            def formatMlFileList(aTuple):
                name, nrows, mod_date = aTuple
                name = name.replace("_output_ML.csv", "").replace("_"," ")
                project = name
                return(name + "; " + nrows + tr("startup2") + mod_date + tr("startup3"))
            
            askResume = QDialog()
            layout = QVBoxLayout(askResume)
            layout.addWidget(QLabel(tr("startup1")))
            combo = QComboBox()
            for f in lFiles:
                combo.addItem(formatMlFileList(f))
            layout.addWidget(combo)
            buttonContainer = QVBoxLayout()
            buttonNew = QPushButton(tr("startupNew"))
            buttonOpen = QPushButton(tr("startupOpen"))
            buttonContainer.addWidget(buttonNew)
            buttonContainer.addWidget(buttonOpen)
            layout.addLayout(buttonContainer)
            code_open = 1
            code_new = 0
            buttonOpen.clicked.connect(lambda: askResume.done(code_open))
            buttonNew.clicked.connect(lambda: askResume.done(code_new))
            result = askResume.exec_()
            
            if result == code_open:
                indexFile = combo.currentIndex()
                writeLogs("    Previous session reused "+lMlFiles[indexFile]+".\n")
                project = lMlFiles[indexFile].replace(mlFile, "")
                return(lMlFiles[indexFile])
            
            if result == code_new:
                writeLogs("    New session.\n")
                return ""
            
            return ""  #should never be triggered, but just in case...      
            
        else:
            writeLogs("    No previous session to reuse.\n")
            return ""
        return "" #should never be triggered, but just in case...      

    def setup_loading_window(self):
        self.movie = QtGui.QMovie("resources/media/loading.gif")
        self.ui.loading_symbol.setScaledContents(True)
        self.ui.loading_symbol.setMovie(self.movie)
        self.movie.start()
        
    def select_files(self):
        options = QFileDialog.Options()
        folderName = QFileDialog.getExistingDirectory(self, tr("folderSelector"))
        writeLogs("    Folder chosen: \""+folderName+"\"\n")
        return folderName

    def loadML(self, lFiles): #run the ML algorithm and displays the associated progressbar
        self.ui.progressBar.setValue(0)
        self.thread = QThread()
        self.worker = MLWorker(lFiles)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.ui.progressBar.setValue)
        self.worker.finished.connect(self.on_ml_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_ml_finished(self):
        writeLogs("    ML algorithm finished running.\n")
        self.hide()
        self.finished.emit()
        global initialisation
        initialisation.deleteLater()
        self.deleteLater()

class MLWorker(QObject): #Worker working in parallel with the loading windows of class Init_Window, to keep it responsive (notably to keep the progressbar running)
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        global mlFile
        run_ML.main(self.files, self.update_progress, mlFile) #HereChangeMLAlgo
        self.finished.emit()

    def update_progress(self, value):
        self.progress.emit(value)

class Display_Types(QWidget):
    setTypeTile = pyqtSignal(str) #signal triggered when the user sets the RIG type by clicking on a picture/text
    
    def __init__(self, parent=None):
        super().__init__()
        self.ui = RIG_Type()
        self.parent = parent
        self.ui = RIG_Type(None)
        self.ui.imageClicked.connect(self.clicked)
        self.ui.show()
        
    
    def clicked(self, clickedName, clickedNum):  #the arguments are the actual name and # of RIG type actual type
        writeLogs("    In RIG/CRAV type popup, user clicked on QLabel "+str(clickedName)+"\n")
        self.parent.force_RIG_type(str(clickedNum))
        self.ui.close()

class Force_Type_Class(QWidget):
    def __init__(self, parent, categ):
        super().__init__()
        self.parent = parent
        self.ui = ForceTypePopup(categ, None)
        self.ui.imageClicked.connect(self.clicked)
        self.ui.show()

    def clicked(self, clickedName, clickedCat, clickedNum): #the arguments are the actual name and # of die type actual type
        writeLogs("    In force die type popup, user clicked on QLabel "+clickedCat+" "+str(clickedNum)+"\n")
        self.parent.ui.force.setChecked(True)
        self.parent.ui.force_type.setCurrentText(clickedCat)
        self.parent.ui.force_number.setText(str(clickedNum))
        self.ui.close()

class License_Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_licenseDialog()
        self.ui.setupUi(self,)
        self.show()

class Theme_Popup():
    def __init__(self):
        super().__init__()
        self.ui = Ui_themeDialog()
        self.ui.themeClicked.connect(self.clicked)
        self.ui.exec_()

    def clicked(self, theme): #the arguments are the actual name and # of die type actual type
        writeLogs("    Theme has been set to  "+str(theme)+"\n")
        with open("resources/data/theme.conf", "w") as themeFile:
            themeFile.write(theme) #change default theme
        app.setStyleSheet(loadStylesheet(theme))

class Undetected_Die(QWidget):
    def __init__(self, pic, parent):
        super().__init__()
        self.parent = parent
        self.pic = pic
        self.ui = Ui_AddDieDialog()
        self.ui.setupUi(self, pic)
        self.show() # show the window
        
    def exit(self):
        writeLogs("    false negative (undetected die) cancelled\n")
        self.close()
        
    def accept(self): #get sherd data from parent, die data from current windows, write the record and leave
        global fold
        coord_raw = self.ui.die_picture.click_positions
        dispW = self.ui.die_picture.displayed_width
        dispH = self.ui.die_picture.displayed_height
        if len(coord_raw)<2:
            basicWarning(tr("noFalseNegTwoPoints"))
            writeLogs("    false negative (undetected die) FAILED: not enough coordinates provided "+str(coord_raw)+".\n")
            return(None)
        writeLogs("    false negative (undetected die) validated at (unreformatted) coordinates (X1,Y1),(X2,Y2): "+str(coord_raw)+"\n")
        width, heigth = imagesize.get(self.pic)
        [(x1,y1),(x2,y2)] = coord_raw
        final_frame = [int(min(x1, x2)*(float(width)/float(dispW))), int(min(y1, y2)*(float(heigth)/float(dispH))), int(max(x1, x2)*(float(width)/float(dispW))), int(max(y1, y2)*(float(heigth)/float(dispH)))]
        typeDie = self.ui.set_type.currentText()
        numberDie = self.ui.set_number.text()
        if typeDie == tr("selectPattern"):
            basicWarning(tr("noSelect"))
            writeLogs("    false negative (undetected die) FAILED: no die type/number provided "+str(coord_raw)+".\n")
            return(None)
        comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author = self.getParentAttributes()
        writeLogs("    false negative (undetected die) validated as "+str(typeDie)+" "+str(numberDie)+"\n")
        output = [typeDie, numberDie, comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author, "FN"]
        self.parent.checkDecorativeRegister(typeDie+numberDie, self.parent.data[3]) #checkDecorativeRegister checks whether there aremultiple decorative registers for the same die, and updates the comment field accordingly
        output_application_files(output,self.parent.data[0],self.parent.data[1],self.parent.data[2],self.parent.data[3])
        output_application_csv(output,self.parent.data[0],self.parent.data[1],self.parent.data[2],self.parent.data[3], fold, final_frame)
        self.close()
    
    def getParentAttributes(self):
        country = ""
        region = ""
        department = ""
        municipality = ""
        site = ""
        x = ""
        y = ""
        z = ""
        location = (False, False, False, False)#edge, belly, bottom, handle
        comment = self.parent.ui.comment_box.toPlainText().replace(";",",").replace("\n","\t").replace("\r","") #semi-collon are reserved as separators in output CSV, so we sanitize the field
        country = self.parent.ui.country.toPlainText()
        region = self.parent.ui.region.toPlainText()
        department = self.parent.ui.department.toPlainText()
        municipality = self.parent.ui.municipality.toPlainText()
        site = self.parent.ui.site.toPlainText()
        x = self.parent.ui.lambert_X.toPlainText()
        y = self.parent.ui.lambert_Y.toPlainText()
        z = self.parent.ui.lambert_Z.toPlainText()
        fait = self.parent.ui.numFait.toPlainText()
        us = self.parent.ui.numUs.toPlainText()
        craType = self.parent.ui.mode_CRA.currentText()
        craNum = self.parent.ui.rig_num.toPlainText()
        if self.parent.ui.unknownCRA.isChecked():
            craNum = tr("otherType")
        author = self.parent.ui.author.displayText()
        lLocations = []
        if self.parent.ui.checkBox_edge.isChecked():
            lLocations.append(tr("edge"))
        if self.parent.ui.checkBox_belly.isChecked():
            lLocations.append(tr("belly"))
        if self.parent.ui.checkBox_handle.isChecked():
            lLocations.append(tr("handle"))
        if self.parent.ui.checkBox_bottom.isChecked():
            lLocations.append(tr("bottom"))
        location = "/".join(lLocations)#merge the active parts of edge/belly/bottom/handle
        return(comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author)

'''def doSomething(filename):#TODO: remove when linked to ML algo
    with open("logs.txt", "a") as logFile:
        logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    ML loading started.\n")
    time.sleep(5)
    with open("logs.txt", "a") as logFile:
        logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    ML loading completed.\n")
    return()'''


def outputML_CSV_exists(): #check if the ML output CSV exists, and contains data; this allows user to skip the ML process if data remains from last asssessment; also returns number of lines (header excluded) and date of last modification
    file_path = mlFile
    files = glob.glob("*_"+mlFile) 
    if len(files)>0:
        outputList = [False, [], [], []]
        for aMlFile in files:
            fileObject = csv.reader(aMlFile)
            row_count = 0
            for row in open(aMlFile):
                row_count+= 1
            if row_count>1:
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(aMlFile)
                outputList[0] = True
                outputList[1] += [str(row_count-1)]
                outputList[2] += [time.ctime(mtime)]
                outputList[3] += ["".join(aMlFile)]
        return(outputList)
    else:
        return [False, [], [], []]

def output_application_csv(lOut,numDie,numDecor,numPhoto,namePhoto,path,coords):#writes manual review results in Final_Output.csv
    [typeDie, numberDie, comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author, resML] = lOut
    x1,y1,x2,y2 = coords
    writeLogs("    Writing CSV file... "+str(lOut)+"\n")
    for file_path in [finalFile]:
        if not(os.path.exists(file_path)): #create file and insert headers
            with open(file_path, "w", encoding='utf-8') as outputFile:
                outputFile.write("Numero de tesson;Numero de decor;Numero de photo;Nom photo;Type de motif identifie;Numero de motif identifie;Commentaire;Pays;Region;Departement;Commune;Site/Lieu-dit;Lambert-X;Lambert-Y;Lambert-Z;Numero de fait;Numero d'US;Type de CRA;Numero de CRA;Position du tesson;Auteur de l'identification;X gauche;Y bas;X droite;Y haut;retex ML (communiquer aux devs);Registre décoratif répété?\n")
        with open(file_path, "a", encoding='utf-8') as outputFile:
            outputFile.write(";".join([numDie,numDecor,numPhoto,namePhoto,typeDie, numberDie, comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author,str(x1),str(y1),str(x2),str(y2), resML])+"\n")
    writeLogs("    Written!\n")


def output_application_files(lOut,numDie,numDecor,numPhoto,namePhoto):#TODO pas encore fini
    [typeDie, numberDie, comment, country, region, department, municipality, site, x, y, z, fait, us, craType, craNum, location, author, resML] = lOut
    writeLogs("    Copying files... "+str(lOut)+"\n")
    path=os.path.dirname(namePhoto)
    if not(os.path.isdir(path+"/"+typeDie)):#if folder with die type does not exist already
        os.mkdir(path+"/"+typeDie)
    if (numberDie!="0") and not(os.path.isdir(path+"/"+typeDie+"/"+numberDie)):#if die number is set
        os.mkdir(path+"/"+typeDie+"/"+numberDie)
    if ((numberDie=="0") and (typeDie!=tr("undet")) and not(os.path.isdir(path+"/"+typeDie+"/inedit"))):#if inedit but not indetermine (indetermine will be sent to a specific folder)
        os.mkdir(path+"/"+typeDie+"/inedit")
    newPath = path+"/"+typeDie
    if typeDie!=tr("undet"):
        if numberDie!="0":
            newPath+="/"+numberDie
        else:
            newPath+="/inedit"
    photo_filename = os.path.basename(namePhoto).split('/')[-1]
    shutil.copy2(namePhoto, newPath+"/"+photo_filename)
    if len(comment)>0:
        with open(newPath+"/"+photo_filename+"_comment.txt", "w") as commentFile:
            commentFile.write(comment)


def cleanLogs():#stores a backup of the last 3 sessions, removes the previous sessions, and frees space for current session logs
    #the existing log files are "log.txt" for current session, and the 3 older "logs.txt.old", "logs.txt.older" and "logs.txt.oldest" files for the 3 previous sessions
    #removal of old logs after 3 sessions aims at reducing the impact of storage growth due to abusive logging
    try:
        os.remove("logs.txt.oldest")
    except:
        pass
    try:
        os.rename("logs.txt.older", "logs.txt.oldest")
    except:
        pass
    try:
        os.rename("logs.txt.old", "logs.txt.older")
    except:
        pass
    try:
        os.rename("logs.txt", "logs.txt.old")
    except:
        pass

def readDataCsvML(): #open the list of suggestions of die that was provided by ML algorithm
    global mlFile
    with open(mlFile) as csv_file:
        csv_read=csv.reader(csv_file, delimiter=';')
        header = next(csv_read, None)#skip header line, and keep it as a backup
        rawList = []
        cleanList = []
        for aRow in csv_read:
            rawList.append([aRow])
    return(header, rawList)

def prepareData(): #takes first item from list of ML output, and outputs the expected format for GUI
    try:
        aLine = rawData[currentIndex][0]
    except: #the above line will fail when rawData is empty
        aLine = [""]*40
    numSherd = aLine[0]
    numDie = aLine[1]
    picNum = aLine[2]
    picPath = aLine[3]
    choice1 = aLine[4]
    choice1pretty = aLine[5]
    path1 = "resources/media/Die_types/"+aLine[4]+".png"
    try:
        prob1 = str(int(100*float(aLine[6])))+"%"
    except:
        prob1 = ""
    choice2 = aLine[7]
    choice2pretty = aLine[8]
    path2 = "resources/media/Die_types/"+aLine[7]+".png"
    try:
        prob2 = str(int(100*float(aLine[9])))+"%"
    except:
        prob2 = ""
    choice3 = aLine[10]
    choice3pretty = aLine[11]
    path3 = "resources/media/Die_types/"+aLine[10]+".png"
    try:
        prob3 = str(int(100*float(aLine[12])))+"%"
    except:
        prob3 = ""
    choice4 = aLine[13]
    choice4pretty = aLine[14]
    path4 = "resources/media/Die_types/"+aLine[13]+".png"
    try:
        prob4 = str(int(100*float(aLine[15])))+"%"
    except:
        prob4 = ""
    comm = aLine[25]
    aux1 = aLine[26]
    xLeft = aLine[36]
    yBot = aLine[37]
    xRight = aLine[38]
    yTop = aLine[39]
    return(numSherd,numDie,picNum,picPath,choice1,choice1pretty,path1,prob1,choice2,choice2pretty,path2,prob2,choice3,choice3pretty,path3,prob3,choice4,choice4pretty,path4,prob4,comm,xLeft,yBot,xRight,yTop, aux1)

def preparePictures(dataList): #takes the raw ML output, and prepares temporary pictures for review, with die areas being cornered
    newList = dataList
    listPathPicture = list(set([x[0][3] for x in newList]))
    for aPic in listPathPicture: #TODO: this is a quadratic O(n²) approach, and should be improved
        writeLogs("    Starting to draw rectangle(s) on picture "+aPic+".\n")
        im = PIL.Image.open(aPic)
        newPath = "tmp/"+os.path.basename(aPic)
        w,l=im.size
        if w!=l: #if the picture is not square, crop it to a square
            cropArea = picCropper.cropToSquare(w,l)
            im2 = im.crop(cropArea)
        else:
            im2=im
        for i in range(len(newList)):
            aRecord = newList[i][0]
            if aRecord[3]==aPic and all([aRecord[36],aRecord[37],aRecord[38],aRecord[39]]):
                PIL.ImageDraw.Draw(im2).rectangle((min(int(aRecord[36]),int(aRecord[38])),min(int(aRecord[37]),int(aRecord[39])),max(int(aRecord[36]),int(aRecord[38])),max(int(aRecord[37]),int(aRecord[39]))), outline=normalColor, width=4) #colors adjusted to be recognizable by most colorblind people
        im2.save(newPath)
    return newList
    
def setCurrent(pic, xy): #prepares the current picture to be reviewed, by overwriting the green rectangle on current die in red
    im = PIL.Image.open(pic)
    PIL.ImageDraw.Draw(im).rectangle((min(int(xy[0]),int(xy[2])),min(int(xy[1]),int(xy[3])),(max(int(xy[0]),int(xy[2])),max(int(xy[1]),int(xy[3])))), outline=highlightColor, width=5) #colors adjusted to be recognizable by most colorblind people
    im.save("tmp/current.png")

def properClosure(): #application is closing; log the action, save the remaining unclassified die list for next session
    writeLogs("    Closure process started.\n")
    global mlFile
    with open(mlFile, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        merged = [[header]]+rawData
        out = [x for l in merged for x in l]
        writer.writerows(out)
    for f in glob.glob("tmp/*"): #empty tmp folder
        os.remove(f)

def basicWarning(txt):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(txt)
    msg.setWindowTitle("Information")
    msg.setStandardButtons(QMessageBox.Ok)  # Adds an "Ok" button
    msg.exec_()  # Show the message box

def loadStylesheet(theme): #loads a QSS file, for a theme, e.g. dark/light
    with open("resources/styles/"+theme+".qss", "r") as file:
        return file.read()

def loadFonts(): #loads all non-standard fonts in the correct directory, before applying style sheets to PyQt
    for font_file in os.listdir("resources/styles/fonts"):
        if font_file.lower().endswith((".ttf", ".otf")):
            font_id = QFontDatabase.addApplicationFont("resources/styles/fonts/"+font_file)
            if font_id == -1:
                with open("logs.txt", "a") as logFile:
                        logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    Font file "+font_file+" did not load correctly.\n")
            else:
                with open("logs.txt", "a") as logFile:
                        logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    Font file "+font_file+" loaded.\n")

def addSize(sherdId): #adds the size of the sherds in the name (and reuses the sherdId to assess a translated name)
    global displaySize, sizeSherd, dict_types

    if sherdId == "":
        return("")

    main_type = dict_types[int(sherdId[0])]
    cat_num = str(int(sherdId[1:]))
    if cat_num == "0":
        cat_num = "(?)"

    newName = main_type + " " + cat_num


    if not displaySize:
        return(newName)
    else:
        try:
            [size, site] = sizeSherd[str(sherdId)].replace("\\n", "\n").split("$",1)
            return(site +"\n"+ newName+"\n"+size)
        except: #if the key is not present (e.g. size not provided), just display the name
            return(newName)

def incrementId(s): #tries to identify a pattern in ID (sherd or die ID), and returns the increased version of the ID
    match = re.search(r'(\d+)$', s)
    if match:
        number_in_str = match.group(1)
        number_index = match.start(1)
        incremented = str(int(number_in_str) +1).zfill(len(number_in_str))
        return(s[:number_index] + incremented)
    else:
        return(s)

class SearchDialog(QDialog): #popup that allows to search for a previous sherd type
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("searchTitle"))
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.textEdit = QtWidgets.QLineEdit(self)
        self.textEdit.setPlaceholderText(tr("searchPlaceholder"))
        self.okButton = QtWidgets.QPushButton("OK", self)
        self.okButton.clicked.connect(self.accept)  # Close the dialog
        self.okButton.setDefault(True)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.okButton)
        self.setLayout(layout)

def launch_main_window():
    global main_window, header, rawData
    header, rawData = readDataCsvML()
    rawData = preparePictures(rawData) #prepare the pictures to make them fit as expected
    main_window = Selector_Main()
    main_window.show()


def run_app():
    global fold, sizeSherd, initialisation
    cleanLogs()
    app = QApplication(sys.argv)
    loadFonts()
    with open("resources/data/theme.conf", "r") as themeFile:
        app.setStyleSheet(loadStylesheet(themeFile.readline())) #set the initial theme to the saved theme
    fold = ""
    with open("resources/data/sizes.conf", "r") as sizeFile:
        sizeSherd = dict(line.strip().split(':', 1) for line in sizeFile)
    initialisation = Init_Window()
    initialisation.finished.connect(launch_main_window)
    QTimer.singleShot(0, initialisation.start)
    app.aboutToQuit.connect(properClosure) #start the "close" event listener, to save remaining unclassed pictures
    return app.exec()

if __name__ == '__main__':
    exit_code = run_app()
    if exit_code == 205: #restart code
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    sys.exit(exit_code)
    

