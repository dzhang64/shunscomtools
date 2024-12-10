import sys
import pandas
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, QFileDialog, QMessageBox)
import MyPlan.ui_neighbor
from MyPlan.Neighbor import *
from OtherFunctions.myemail import *


class MyNeighbor(MyPlan.ui_neighbor.Ui_Dialog_neighbor, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()
        self.num = 0
        self.res = pandas.DataFrame()
        self.pushButton_choosefile.clicked.connect(self.do_choose('choosefile'))
        self.pushButton_cellinfo.clicked.connect(self.do_choose('cellinfo'))
        self.pushButton_do.clicked.connect(self.do_neighbor)

    def do_neighbor(self):
        out, filetype = QFileDialog.getSaveFileName(self, '选择保存路径', os.getcwd(), '(*.xlsx)')
        output = [out]
        file1 = self.lineEdit_choosefile.text()
        file2 = self.lineEdit_cellinfo.text()
        Abandon_D = float(self.lineEdit_abandom.text())
        TA_R = float(self.lineEdit_ta.text())
        HBWD_R = float(self.lineEdit_angle.text())
        try:
            judge, res = plan_neighbor(file1, file2, output[0], Abandon_D, TA_R, HBWD_R)
            self.res = res
            self.textBrowser_log.append('邻区规划完成')
        except Exception as e1:
            self.textBrowser_log.append(f'出错：{e1}\n{sys.exc_info()}')
            QMessageBox.warning(self, '信息提示', f'{e1}')
            judge = 0
        if judge == 1:
            email_str = self.lineEdit_email.text()
            if ',' in email_str:
                em_lt = list(email_str.split(','))
                em_lt1 = [i for i in em_lt if '@' in i]
                em = SendMail()
                bd = f"""<b><body>你好！</b><br>
                                    <b><body>你正在使用顺盛网优工具。邻区规划详细结果请查看附件。</b><br>
                                    <b><body>\n</b><br>
                                    <b><body>\n</b><br>
                                    <b><body>如有问题或新增功能，请联系邮箱wangxinyue@shunscom.com或电话18921790946(微信同号)</b><br>
                                """
                info = em.send(toAddrs=em_lt1, subject="网优工具-邻区规划", msg=bd, file_path=output)
                QMessageBox.information(self, '信息提示', f'{info}')
            elif not email_str:
                return
            else:
                QMessageBox.warning(self, '信息提示', f"每个邮箱后加','")
        self.num += 1
        self.accept()

    def do_choose(self, operation):
        def func():
            if operation == 'choosefile':
                filename, filetype = QFileDialog.getOpenFileName(self, '选择规划的excel表', os.getcwd(), '(*.xlsx)')
                self.lineEdit_choosefile.setText(filename)
            elif operation == 'cellinfo':
                filename, filetype = QFileDialog.getOpenFileName(self, '选择全网工参', os.getcwd(), '(*.xlsx)')
                self.lineEdit_cellinfo.setText(filename)
        return func
