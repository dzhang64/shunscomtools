import sys

from PyQt6.QtWidgets import (QDialog, QMessageBox, QMainWindow, QApplication, QLineEdit)

from MyLogin.ShunscomLogin import ShunscomToolLogin
from MyLogin.login import Ui_login
from MyLogin.register_main import MyRegister


class MyLogin(Ui_login, QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化界面
        self.show()  # 展现界面
        self.tool_id = ''  # 工具ID
        self.username = ''
        self.num = 0
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)  # 隐藏密码
        self.pushButton_login.clicked.connect(self.do_login)
        self.pushButton_register.clicked.connect(self.do_register('register'))
        self.pushButton_update.clicked.connect(self.do_register('update'))
        self.state = 0

    @staticmethod
    def do_register(operation):
        """
        注册界和修改密码窗口
        :param operation: register 或 update
        :return:
        """

        def func():
            myregister = MyRegister(operation)
            myregister.exec()

        return func

    def do_login(self):
        """
        登录
        :return:
        """
        self.username = self.lineEdit_username.text()  # 获取用户名
        password = self.lineEdit_password.text()  # 获取密码
        # 登录工具
        myLogin = ShunscomToolLogin(userName=self.username, passWord=password)
        myLogin.login()
        info = myLogin.info
        QMessageBox.warning(self, '信息提示', f'{info}')
        self.state = myLogin.state
        if self.state:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myExcelMerger = MyLogin()
    print(myExcelMerger.state)
    # home = MyHomeScreen(myExcelMerger.username)
    # home.show()
    # myExcelMerger.show()
    sys.exit(app.exec())
