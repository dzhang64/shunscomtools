# Form implementation generated from reading ui file 'Ui_Xml.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_XMLHand(object):
    def setupUi(self, XMLHand):
        XMLHand.setObjectName("XMLHand")
        XMLHand.resize(692, 519)
        self.gridLayout = QtWidgets.QGridLayout(XMLHand)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_choose_dir = QtWidgets.QPushButton(parent=XMLHand)
        self.pushButton_choose_dir.setStyleSheet("background-color: rgb(255, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_choose_dir.setObjectName("pushButton_choose_dir")
        self.verticalLayout.addWidget(self.pushButton_choose_dir)
        self.listWidget_xml_paths = QtWidgets.QListWidget(parent=XMLHand)
        self.listWidget_xml_paths.setObjectName("listWidget_xml_paths")
        self.verticalLayout.addWidget(self.listWidget_xml_paths)
        self.pushButton_remove_xml = QtWidgets.QPushButton(parent=XMLHand)
        self.pushButton_remove_xml.setStyleSheet("background-color: rgb(255, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_remove_xml.setObjectName("pushButton_remove_xml")
        self.verticalLayout.addWidget(self.pushButton_remove_xml)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_do_convert = QtWidgets.QPushButton(parent=XMLHand)
        self.pushButton_do_convert.setStyleSheet("background-color: rgb(255, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_do_convert.setObjectName("pushButton_do_convert")
        self.verticalLayout_2.addWidget(self.pushButton_do_convert)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.retranslateUi(XMLHand)
        QtCore.QMetaObject.connectSlotsByName(XMLHand)

    def retranslateUi(self, XMLHand):
        _translate = QtCore.QCoreApplication.translate
        XMLHand.setWindowTitle(_translate("XMLHand", "PDF处理"))
        self.pushButton_choose_dir.setText(_translate("XMLHand", "选择文件"))
        self.pushButton_remove_xml.setText(_translate("XMLHand", "移除文件"))
        self.pushButton_do_convert.setText(_translate("XMLHand", "转换"))