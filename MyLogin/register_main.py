import sys
from PyQt6.QtWidgets import (QApplication, QMessageBox, QDialog, QLineEdit)
from MyLogin import register
from MyLogin.ShunscomLogin import ShunscomToolRegister


class MyRegister(register.Ui_Dialog_register, QDialog):
    def __init__(self, operate):
        super().__init__()
        self.setupUi(self)
        self.operate = operate
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)  # 隐藏密码
        self.lineEdit_confirmpassword.setEchoMode(QLineEdit.EchoMode.Password)  # 隐藏密码
        self.show()
        self.pushButton_submit.clicked.connect(self.do_submit)
        self.state = 0

    def do_submit(self):

        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        password_confirm = self.lineEdit_confirmpassword.text()
        if not username:
            QMessageBox.warning(self, '信息提示', '请输入账号')
            return
        if not username.endswith('@shunscom.com'):
            QMessageBox.warning(self, '信息提示', '请输入注册的账号必须为公司邮箱')
            return
        if not password:
            QMessageBox.warning(self, '信息提示', '请输入密码')
            return
        if not password_confirm:
            QMessageBox.warning(self, '信息提示', '请确认密码')
            return
        if password != password_confirm:
            QMessageBox.warning(self, '信息提示', '密码不一致')
            return
        try:
            myRegister = ShunscomToolRegister(userName=username, passWord=password, passWordConfirm=password_confirm)

            myRegister.register(self.operate)
        except Exception as e:
            print(e)
        info = myRegister.info
        self.state = myRegister.state
        QMessageBox.warning(self, '信息提示', f'{info}')
        if self.state:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyApp = MyRegister('update')
    sys.exit(app.exec())
