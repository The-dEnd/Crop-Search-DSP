from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
import sys
from translator import tr, current_language

class DecorativeRegisterPopup(QDialog):
    def __init__(self, default_value="1", min_value=1, parent = None, die=""):
        super(DecorativeRegisterPopup, self).__init__(parent)
        self.setWindowTitle(tr("numDecoRegTitle"))
        self.value = default_value
        layout = QVBoxLayout(self)
        self.label = QLabel(tr("numDecoReg").replace("$",die))
        layout.addWidget(self.label)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText(str(default_value))
        layout.addWidget(self.lineEdit)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        self.lineEdit.selectAll()
        self.lineEdit.setFocus()
        
    def get_value(self): #tries to correct most usual typos in name (for AZERTY and QWERTY layouts)
        value = self.lineEdit.text()
        value = value.replace("&","1")
        value = value.replace("é","2")
        value = value.replace('"',"3")
        value = value.replace("'","4")
        value = value.replace("(","5")
        value = value.replace("-","6")
        value = value.replace("è","7")
        value = value.replace("_","8")
        value = value.replace("ç","8")
        value = value.replace("à","9")
        value = value.replace("!","1")
        value = value.replace("@","2")
        value = value.replace("#","3")
        value = value.replace("$","4")
        value = value.replace("%","5")
        value = value.replace("^","6")
        value = value.replace("*","8")
        try:
            return int(value)
        except:
            return 1