# Form implementation generated from reading ui file 'para_check.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ParaCheck(object):
    def setupUi(self, ParaCheck):
        ParaCheck.setObjectName("ParaCheck")
        ParaCheck.resize(697, 566)
        ParaCheck.setStyleSheet("QPushButton {\n"
" font-size: 16px;\n"
" color: rgb(255, 255, 255);\n"
" background-color:rgb(255, 85, 255)\n"
"}\n"
"\n"
"QLabel {\n"
"  font-size: 12px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(ParaCheck)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=ParaCheck)
        self.label.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton_choose_dir = QtWidgets.QPushButton(parent=ParaCheck)
        self.pushButton_choose_dir.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(0, 170, 255);")
        self.pushButton_choose_dir.setObjectName("pushButton_choose_dir")
        self.horizontalLayout.addWidget(self.pushButton_choose_dir)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(parent=ParaCheck)
        self.label_2.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidget_excel_paths = QtWidgets.QListWidget(parent=ParaCheck)
        self.listWidget_excel_paths.setObjectName("listWidget_excel_paths")
        self.horizontalLayout_2.addWidget(self.listWidget_excel_paths)
        self.pushButton_remove_excel = QtWidgets.QPushButton(parent=ParaCheck)
        self.pushButton_remove_excel.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(0, 170, 255);")
        self.pushButton_remove_excel.setObjectName("pushButton_remove_excel")
        self.horizontalLayout_2.addWidget(self.pushButton_remove_excel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton_doandsave = QtWidgets.QPushButton(parent=ParaCheck)
        self.pushButton_doandsave.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";\n"
"background-color: rgb(0, 170, 255);")
        self.pushButton_doandsave.setObjectName("pushButton_doandsave")
        self.verticalLayout.addWidget(self.pushButton_doandsave)
        self.textBrowser_log = QtWidgets.QTextBrowser(parent=ParaCheck)
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.verticalLayout.addWidget(self.textBrowser_log)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 60)
        self.verticalLayout.setStretch(4, 1)

        self.retranslateUi(ParaCheck)
        QtCore.QMetaObject.connectSlotsByName(ParaCheck)

    def retranslateUi(self, ParaCheck):
        _translate = QtCore.QCoreApplication.translate
        ParaCheck.setWindowTitle(_translate("ParaCheck", "参数核查"))
        self.label.setText(_translate("ParaCheck", "请选择要核查的文件"))
        self.pushButton_choose_dir.setText(_translate("ParaCheck", "选择文件"))
        self.label_2.setText(_translate("ParaCheck", "请移除不需要的文件"))
        self.pushButton_remove_excel.setText(_translate("ParaCheck", "移除文件"))
        self.pushButton_doandsave.setText(_translate("ParaCheck", "执行并保存"))
