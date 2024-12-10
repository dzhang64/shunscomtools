import sys

from PyQt6.QtWidgets import (
    QApplication
)

from MyLogin.login_main import MyLogin

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyLogin()
    myApp.exec()
    if myApp.state:
        from HomeScreen.ShunscomTool_main import MyHomeScreen
        l1 = MyHomeScreen(myApp.username)
    sys.exit(app.exec())
