# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(927, 814)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("scheduler (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 240, 651, 101))
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("font: 12pt \"Montserrat\"; color: black ; font-weight: bold;\n"
" font-weight:bold;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(310, 40, 331, 211))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("bigger.png"))
        self.label_2.setObjectName("label_2")
        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setGeometry(QtCore.QRect(300, 330, 281, 91))
        self.toolButton_3.setStyleSheet("font: 12pt \"Montserrat\"; outline-color: blue; font-weight: bold")
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_4.setGeometry(QtCore.QRect(300, 440, 281, 91))
        self.toolButton_4.setStyleSheet("font: 12pt \"Montserrat\"; outline-color: black;  font-weight: bold")
        self.toolButton_4.setObjectName("toolButton_4")
        self.toolButton_5 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_5.setGeometry(QtCore.QRect(300, 550, 281, 91))
        self.toolButton_5.setStyleSheet("font: 12pt \"Montserrat\";  font-weight: bold")
        self.toolButton_5.setObjectName("toolButton_5")
        self.toolButton_6 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_6.setGeometry(QtCore.QRect(300, 660, 281, 91))
        self.toolButton_6.setStyleSheet("font: 12pt \"Montserrat\";  font-weight: bold")
        self.toolButton_6.setObjectName("toolButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CPU Job Scheduler"))
        self.label.setText(_translate("MainWindow", "CHOOSE THE TYPE OF SCHEDULER TO GET STARTED:"))
        self.toolButton_3.setText(_translate("MainWindow", "FCFS Scheduler"))
        self.toolButton_4.setText(_translate("MainWindow", "SJF Scheduler"))
        self.toolButton_5.setText(_translate("MainWindow", "Priority Scheduler"))
        self.toolButton_6.setText(_translate("MainWindow", "Round Robin Scheduler"))
