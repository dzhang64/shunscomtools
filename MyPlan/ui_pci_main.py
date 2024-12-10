import os
import sys
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, QFileDialog, QMessageBox, QApplication)
from MyPlan.DoPCI import *
from OtherFunctions.myemail import SendMail
from MyPlan.ui_pci import *


class MyPCI(Ui_Dialog_PCI, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()
        self.num = 0
        self.pushButton_choosefile.clicked.connect(self.do_choose)
        self.pushButton_do.clicked.connect(self.do_plan)
        self.res = pd.DataFrame()

    def do_choose(self):
        filename, filetype = QFileDialog.getOpenFileName(self, '选择规划的excel表', os.getcwd(), '(*.xlsx)')
        self.lineEdit_choosefile.setText(filename)

    def do_plan(self):
        try:
            out_file, filetype = QFileDialog.getSaveFileName(self, '选择保存文件', os.getcwd(), '(*.xlsx)')
            in_file = self.lineEdit_choosefile.text()
            judge = 0
            # 方位角，根据方位角1进行更新
            m0 = int(self.lineEdit_M0.text())
            if m0 + 120 >= 360:
                m1 = m0 + 120 - 360
                self.lineEdit_M1.setText(str(m1))
            else:
                m1 = m0 + 120
                self.lineEdit_M1.setText(str(m1))
            if m0 + 240 > 360:
                m2 = m0 + 240 - 360
                self.lineEdit_M2.setText(str(m2))
            else:
                m2 = m0 + 240
                self.lineEdit_M2.setText(str(m2))

            pci_range = self.lineEdit_PCI0.text() + ',' + self.lineEdit_PCI1.text()
            dis = int(self.lineEdit_PCIdistance.text())
            res = pd.DataFrame()
            try:
                data1 = pd.read_excel(in_file)
                if self.radioButton.isChecked():
                    judge, res = plan_pci(PCI_range=pci_range, azimuth0_range=m1, dis=dis, infile=in_file)
                    self.textBrowser_log.append(f'PCI规划完成')
                    QApplication.processEvents()
                elif self.radioButton_2.isChecked():
                    res_lst = []
                    bands = set(list(data1['Band']))
                    for band in list(bands):
                        data_band = data1[data1['Band'] == band]
                        judge, res_band = plan_pci2(PCI_range=pci_range, azimuth0_range=m1, dis=dis, data=data_band)
                        if judge == 1:
                            res_lst.append(res_band)
                    res = pd.concat(res_lst)
                    judge1, tac = plan_tac(dis=dis, data=data1)
                    res = res.merge(tac[['CELLNAME', 'TAC_最近', 'TAC_最多']], how='left', on='CELLNAME')
                    self.textBrowser_log.append(f'PCI规划完成')
                    QApplication.processEvents()
                else:
                    res_lst = []
                    bands = set(list(data1['Carrier']))
                    for band in list(bands):
                        data_band = data1[data1['Carrier'] == band]
                        judge, res_band = plan_pci2(PCI_range=pci_range, azimuth0_range=m1, dis=dis, data=data_band)
                        if judge == 1:
                            res_lst.append(res_band)
                    res = pd.concat(res_lst)
                    judge1, tac = plan_tac(dis=dis, data=data1)
                    res = res.merge(tac[['CELLNAME', 'TAC_最近', 'TAC_最多']], how='left', on='CELLNAME')

                    self.textBrowser_log.append(f'PCI规划完成')
                    QApplication.processEvents()

            except Exception as e1:
                self.textBrowser_log.append(f'出错：{e1}\n{traceback.format_exc()}')
                QApplication.processEvents()
                QMessageBox.warning(self, '信息提示', f'程序运行出错，原因：{traceback.format_exc()}')
            if res.shape[0] != 0:
                f_prach = self.lineEdit_prachformat.text()
                d_prach = float(self.lineEdit_accessdiatance.text())
                if f_prach == '839':
                    ncs = 1.04875 * (6.67 * (d_prach / 1000) + 5 + 2)
                    ncs = greater_than_min(ncs, [0, 13, 15, 18, 22, 26, 32, 38, 46, 59, 76, 93, 119, 167, 279, 419])
                    self.lineEdit_ncs.setText(str(ncs))
                    ncs = int(838 / ncs)
                    ncs1 = int(64 / ncs) + 1
                    ncs2 = int(838 / ncs1)
                    res['rootsequencelndex'] = res['PlannedPCI'].apply(
                        lambda x: ncs1 * (x - int(x / ncs2) * ncs2) if x != '无可用PCI' else '无可用PCI')
                elif f_prach == '139':
                    ncs = 1.045 * (6.67 * (d_prach / 1000) + 5 + 2)
                    ncs = greater_than_min(ncs, [2, 4, 6, 8, 10, 12, 15])
                    self.lineEdit_ncs.setText(str(ncs))
                    ncs = int(138 / ncs)
                    ncs1 = int(64 / ncs) + 1
                    ncs2 = int(138 / ncs1)
                    res['rootsequencelndex'] = res['PlannedPCI'].apply(
                        lambda x: ncs1 * (x - int(x / ncs2) * ncs2) if x != '无可用PCI' else '无可用PCI')
                self.res = res
                res.to_excel(out_file, index=False)
                QApplication.processEvents()
                self.textBrowser_log.append(f'PRACH规划完成')
                email_str = self.lineEdit_email.text()
                if ',' in email_str:
                    em_lt = list(email_str.split(','))
                    em_lt1 = [i for i in em_lt if '@' in i]
                    em = SendMail()
                    bd = f"""<b><body>你好！</b><br>
                                     <b><body>你正在使用顺盛网优工具。PCI规划详细结果请查看附件。</b><br>
                                     <b><body>\n</b><br>
                                     <b><body>\n</b><br>
                                     <b><body>如有问题或新增功能，请联系邮箱wangxinyue@shunscom.com或电话18921790946(微信同号)</b><br>
                                 """
                    info = em.send(toAddrs=em_lt1,cc_list=[], subject="网优工具-PCI规划", msg=bd, file_path=[out_file])
                    QMessageBox.information(self, '信息提示', f"{info}")
                else:
                    QMessageBox.warning(self, '信息提示', f"""每个邮箱后加',' """)
            # self.accept()
        except Exception as e2:
            print(e2)
            QMessageBox.warning(self, '信息提示', f"""{traceback.format_exc()}""")
            QApplication.processEvents()
            self.textBrowser_log.append(f'{traceback.format_exc()}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyPCI()
    sys.exit(app.exec())
