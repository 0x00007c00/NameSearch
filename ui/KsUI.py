# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KsUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(731, 620)
        self.centralwidget = QtWidgets.QWidget(Widget)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 731, 609))
        self.centralwidget.setObjectName("centralwidget")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 10, 51, 31))
        self.label_1.setObjectName("label_1")
        self.queryEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.queryEdit.setGeometry(QtCore.QRect(70, 10, 551, 31))
        self.queryEdit.setObjectName("queryEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(630, 10, 93, 35))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 64, 35))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 450, 51, 16))
        self.label_3.setObjectName("label_3")
        self.logTextArea = QtWidgets.QTextBrowser(self.centralwidget)
        self.logTextArea.setGeometry(QtCore.QRect(10, 470, 711, 131))
        self.logTextArea.setObjectName("logTextArea")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 70, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.depth = QtWidgets.QComboBox(self.centralwidget)
        self.depth.setGeometry(QtCore.QRect(530, 70, 71, 31))
        self.depth.setObjectName("depth")
        self.depth.addItem("")
        self.depth.addItem("")
        self.depth.addItem("")
        self.depth.addItem("")
        self.listview_result = QtWidgets.QListView(self.centralwidget)
        self.listview_result.setEnabled(True)
        self.listview_result.setGeometry(QtCore.QRect(15, 121, 701, 311))
        self.listview_result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listview_result.setObjectName("listview_result")
        self.scan_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_button.setGeometry(QtCore.QRect(610, 70, 111, 31))
        self.scan_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.scan_button.setObjectName("scan_button")
        self.statusbar = QtWidgets.QStatusBar(Widget)
        self.statusbar.setGeometry(QtCore.QRect(0, 0, 3, 20))
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(Widget)
        self.depth.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "MainWindow"))
        self.label_1.setText(_translate("Widget", "关键字"))
        self.pushButton.setText(_translate("Widget", "搜索"))
        self.label_2.setText(_translate("Widget", "结果展示"))
        self.label_3.setText(_translate("Widget", "日志"))
        self.label.setText(_translate("Widget", "扫描深度"))
        self.depth.setItemText(0, _translate("Widget", "8"))
        self.depth.setItemText(1, _translate("Widget", "5"))
        self.depth.setItemText(2, _translate("Widget", "3"))
        self.depth.setItemText(3, _translate("Widget", "无限制"))
        self.scan_button.setText(_translate("Widget", "重新扫描磁盘"))
