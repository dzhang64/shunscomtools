# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(359, 260)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(login.sizePolicy().hasHeightForWidth())
        login.setSizePolicy(sizePolicy)
        login.setStyleSheet("font: 16pt \"Microsoft YaHei UI\";")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(login)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=login)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=login)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_username = QtWidgets.QLineEdit(parent=login)
        self.lineEdit_username.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.horizontalLayout.addWidget(self.lineEdit_username)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(parent=login)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_password = QtWidgets.QLineEdit(parent=login)
        self.lineEdit_password.setStyleSheet("font: 12pt \"Microsoft YaHei UI\";")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.horizontalLayout_2.addWidget(self.lineEdit_password)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_register = QtWidgets.QPushButton(parent=login)
        self.pushButton_register.setStyleSheet("\n"
"color: rgb(255, 0,0);\n"
"font: bold;\n"
"font: 12pt \"Microsoft YaHei UI\";")
        self.pushButton_register.setObjectName("pushButton_register")
        self.horizontalLayout_3.addWidget(self.pushButton_register)
        self.pushButton_login = QtWidgets.QPushButton(parent=login)
        self.pushButton_login.setStyleSheet("\n"
"background-color: rgb(0, 255, 0);\n"
"color: rgb(255, 255, 255);\n"
"font: bold;")
        self.pushButton_login.setObjectName("pushButton_login")
        self.horizontalLayout_3.addWidget(self.pushButton_login)
        self.pushButton_update = QtWidgets.QPushButton(parent=login)
        self.pushButton_update.setStyleSheet("\n"
"color: rgb(255, 0,0);\n"
"font: bold;\n"
"font: 12pt \"Microsoft YaHei UI\";")
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout_3.addWidget(self.pushButton_update)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "登录框"))
        self.label.setText(_translate("login", "请登录"))
        self.label_2.setText(_translate("login", "请输入账号"))
        self.label_4.setText(_translate("login", "请输入密码"))
        self.pushButton_register.setText(_translate("login", "注册"))
        self.pushButton_login.setText(_translate("login", "登录"))
        self.pushButton_update.setText(_translate("login", "修改密码"))