# Form implementation generated from reading ui file 'ui_neighbor.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_neighbor(object):
    def setupUi(self, Dialog_neighbor):
        Dialog_neighbor.setObjectName("Dialog_neighbor")
        Dialog_neighbor.resize(688, 511)
        Dialog_neighbor.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.gridLayout = QtWidgets.QGridLayout(Dialog_neighbor)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_choosefile = QtWidgets.QPushButton(parent=Dialog_neighbor)
        self.pushButton_choosefile.setObjectName("pushButton_choosefile")
        self.horizontalLayout.addWidget(self.pushButton_choosefile)
        self.lineEdit_choosefile = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_choosefile.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_choosefile.setObjectName("lineEdit_choosefile")
        self.horizontalLayout.addWidget(self.lineEdit_choosefile)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_cellinfo = QtWidgets.QPushButton(parent=Dialog_neighbor)
        self.pushButton_cellinfo.setObjectName("pushButton_cellinfo")
        self.horizontalLayout_2.addWidget(self.pushButton_cellinfo)
        self.lineEdit_cellinfo = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_cellinfo.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_cellinfo.setObjectName("lineEdit_cellinfo")
        self.horizontalLayout_2.addWidget(self.lineEdit_cellinfo)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=Dialog_neighbor)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_distance = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_distance.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_distance.setObjectName("lineEdit_distance")
        self.horizontalLayout_3.addWidget(self.lineEdit_distance)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=Dialog_neighbor)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_strong = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_strong.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_strong.setObjectName("lineEdit_strong")
        self.horizontalLayout_4.addWidget(self.lineEdit_strong)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(parent=Dialog_neighbor)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.lineEdit_angle = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_angle.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_angle.setObjectName("lineEdit_angle")
        self.horizontalLayout_5.addWidget(self.lineEdit_angle)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_10.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(parent=Dialog_neighbor)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.lineEdit_ratio = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_ratio.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_ratio.setObjectName("lineEdit_ratio")
        self.horizontalLayout_8.addWidget(self.lineEdit_ratio)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(parent=Dialog_neighbor)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.lineEdit_abandom = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_abandom.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_abandom.setObjectName("lineEdit_abandom")
        self.horizontalLayout_7.addWidget(self.lineEdit_abandom)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(parent=Dialog_neighbor)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.lineEdit_ta = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_ta.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_ta.setObjectName("lineEdit_ta")
        self.horizontalLayout_6.addWidget(self.lineEdit_ta)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel(parent=Dialog_neighbor)
        self.label_9.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.lineEdit_email = QtWidgets.QLineEdit(parent=Dialog_neighbor)
        self.lineEdit_email.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.horizontalLayout_9.addWidget(self.lineEdit_email)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.pushButton_do = QtWidgets.QPushButton(parent=Dialog_neighbor)
        self.pushButton_do.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: bold;")
        self.pushButton_do.setObjectName("pushButton_do")
        self.verticalLayout_3.addWidget(self.pushButton_do)
        self.textBrowser_log = QtWidgets.QTextBrowser(parent=Dialog_neighbor)
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.verticalLayout_3.addWidget(self.textBrowser_log)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Dialog_neighbor)
        QtCore.QMetaObject.connectSlotsByName(Dialog_neighbor)

    def retranslateUi(self, Dialog_neighbor):
        _translate = QtCore.QCoreApplication.translate
        Dialog_neighbor.setWindowTitle(_translate("Dialog_neighbor", "邻区规划框"))
        self.pushButton_choosefile.setText(_translate("Dialog_neighbor", "选择待规划表"))
        self.pushButton_cellinfo.setText(_translate("Dialog_neighbor", "选择全网工参"))
        self.label_3.setText(_translate("Dialog_neighbor", "规划小区覆盖半径"))
        self.lineEdit_distance.setText(_translate("Dialog_neighbor", "3000"))
        self.label_4.setText(_translate("Dialog_neighbor", "     强相关半径     "))
        self.lineEdit_strong.setText(_translate("Dialog_neighbor", "1000"))
        self.label_6.setText(_translate("Dialog_neighbor", "半功率角修正参数"))
        self.lineEdit_angle.setText(_translate("Dialog_neighbor", "1.5"))
        self.label_8.setText(_translate("Dialog_neighbor", "重叠比例门限"))
        self.lineEdit_ratio.setText(_translate("Dialog_neighbor", "0.1"))
        self.label_5.setText(_translate("Dialog_neighbor", "   丢弃半径   "))
        self.lineEdit_abandom.setText(_translate("Dialog_neighbor", "5000"))
        self.label_7.setText(_translate("Dialog_neighbor", " TA修正参数 "))
        self.lineEdit_ta.setText(_translate("Dialog_neighbor", "1"))
        self.label_9.setText(_translate("Dialog_neighbor", "收件人邮箱"))
        self.pushButton_do.setText(_translate("Dialog_neighbor", "执行"))