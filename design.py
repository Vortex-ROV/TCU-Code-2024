# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.cameraFrame = QtWidgets.QFrame(self.centralwidget)
        self.cameraFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cameraFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraFrame.setObjectName("cameraFrame")
        self.verticalLayout_camera = QtWidgets.QVBoxLayout(self.cameraFrame)
        self.verticalLayout_camera.setObjectName("verticalLayout_camera")
        self.camera = QtWidgets.QLabel(self.cameraFrame)
        self.camera.setText("")
        self.camera.setAlignment(QtCore.Qt.AlignCenter)
        self.camera.setObjectName("camera")
        self.verticalLayout_camera.addWidget(self.camera)
        self.verticalLayout_main.addWidget(self.cameraFrame)
        self.buttonFrame = QtWidgets.QFrame(self.centralwidget)
        self.buttonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonFrame.setObjectName("buttonFrame")
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout(self.buttonFrame)
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.saveFrame = QtWidgets.QPushButton(self.buttonFrame)
        self.saveFrame.setObjectName("saveFrame")
        self.horizontalLayout_buttons.addWidget(self.saveFrame)
        self.record = QtWidgets.QPushButton(self.buttonFrame)
        self.record.setObjectName("record")
        self.horizontalLayout_buttons.addWidget(self.record)
        self.verticalLayout_main.addWidget(self.buttonFrame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.saveFrame.setText(_translate("MainWindow", "Aruco Marker"))
        self.record.setText(_translate("MainWindow", "Record"))
