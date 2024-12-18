# Form implementation generated from reading ui file 'add_neighbor.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_add_neighbor(object):
    def setupUi(self, add_neighbor):
        add_neighbor.setObjectName("add_neighbor")
        add_neighbor.resize(697, 566)
        add_neighbor.setStyleSheet("QPushButton {\n"
" font-size: 16px;\n"
" color: rgb(255, 255, 255);\n"
" background-color:rgb(255, 85, 255)\n"
"}\n"
"\n"
"QLabel {\n"
"  font-size: 12px;\n"
"}")
        self.gridLayout_3 = QtWidgets.QGridLayout(add_neighbor)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 3, 0, 1, 1)
        self.textBrowser_log = QtWidgets.QTextBrowser(parent=add_neighbor)
        self.textBrowser_log.setEnabled(True)
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.gridLayout_3.addWidget(self.textBrowser_log, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=add_neighbor)
        self.label_3.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.pushButton_choose_nei = QtWidgets.QPushButton(parent=add_neighbor)
        self.pushButton_choose_nei.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(0, 170, 255);")
        self.pushButton_choose_nei.setObjectName("pushButton_choose_nei")
        self.gridLayout_2.addWidget(self.pushButton_choose_nei, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=add_neighbor)
        self.label.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton_choose_cell = QtWidgets.QPushButton(parent=add_neighbor)
        self.pushButton_choose_cell.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(0, 170, 255);")
        self.pushButton_choose_cell.setObjectName("pushButton_choose_cell")
        self.horizontalLayout.addWidget(self.pushButton_choose_cell)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.pushButton_nei_ex = QtWidgets.QPushButton(parent=add_neighbor)
        self.pushButton_nei_ex.setObjectName("pushButton_nei_ex")
        self.gridLayout_2.addWidget(self.pushButton_nei_ex, 1, 2, 1, 1)
        self.pushButton_cell_ex = QtWidgets.QPushButton(parent=add_neighbor)
        self.pushButton_cell_ex.setObjectName("pushButton_cell_ex")
        self.gridLayout_2.addWidget(self.pushButton_cell_ex, 0, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 2)
        self.gridLayout_2.setColumnStretch(1, 2)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_add = QtWidgets.QPushButton(parent=add_neighbor)
        self.pushButton_add.setEnabled(True)
        self.pushButton_add.setAccessibleName("")
        self.pushButton_add.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(0, 170, 255);")
        self.pushButton_add.setObjectName("pushButton_add")
        self.gridLayout.addWidget(self.pushButton_add, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.gridLayout_3.setRowStretch(0, 1)

        self.retranslateUi(add_neighbor)
        QtCore.QMetaObject.connectSlotsByName(add_neighbor)

    def retranslateUi(self, add_neighbor):
        _translate = QtCore.QCoreApplication.translate
        add_neighbor.setWindowTitle(_translate("add_neighbor", "邻区核查"))
        self.label_3.setText(_translate("add_neighbor", "请选择要导入的邻区信息excel"))
        self.pushButton_choose_nei.setText(_translate("add_neighbor", "导入邻区对"))
        self.label.setText(_translate("add_neighbor", "请选择要导入的小区信息excel"))
        self.pushButton_choose_cell.setText(_translate("add_neighbor", "导入小区信息"))
        self.pushButton_nei_ex.setText(_translate("add_neighbor", "邻区模板导出"))
        self.pushButton_cell_ex.setText(_translate("add_neighbor", "小区模板导出"))
        self.pushButton_add.setText(_translate("add_neighbor", "邻区添加脚本"))
