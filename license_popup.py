# -*- coding: utf-8 -*-
#
# Created by: PyQt5 UI code generator 5.15.9, upgraded manually to PyQt6


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_licenseDialog(object):
    def setupUi(self, licenseDialog):
        licenseDialog.setObjectName("licenseDialog")
        licenseDialog.resize(1200, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(licenseDialog.sizePolicy().hasHeightForWidth())
        licenseDialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(licenseDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 440, 980, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.scrollArea = QtWidgets.QScrollArea(licenseDialog)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 1161, 421))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 959, 419))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(licenseDialog)
        self.buttonBox.rejected.connect(licenseDialog.close) # type: ignore
        self.buttonBox.accepted.connect(licenseDialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(licenseDialog)

    def retranslateUi(self, licenseDialog):
        _translate = QtCore.QCoreApplication.translate
        licenseDialog.setWindowTitle(_translate("licenseDialog", "Licensing"))
        self.label.setText(_translate("licenseDialog", "INIT"))
