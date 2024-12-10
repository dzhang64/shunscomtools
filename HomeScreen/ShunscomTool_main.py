import os
import sys
import traceback
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QMessageBox
)

from HomeScreen.ShunscomTools import Ui_shunscomtools


class MyHomeScreen(Ui_shunscomtools, QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, True)
        self.setupUi(self)  # 初始化界面
        self.show()  # 展现界面

        self.username = username
        # self.wcLabel = QLabel()
        self.wcLabel = QLabel(f'欢迎登录! 账号：{self.username},日期：{str(datetime.now()).split(" ")[0]}')
        self.statusbar.addPermanentWidget(self.wcLabel)

        self.action_PCI.triggered.connect(self.do_pci)
        self.action_Neighbor.triggered.connect(self.do_neighbor)
        self.action_RS_ICM.triggered.connect(self.do_rs_icm)
        self.action_RS_UME.triggered.connect(self.do_rs_ume)
        self.action_HO_ICM.triggered.connect(self.do_ho_icm)
        self.action_HO_UME.triggered.connect(self.do_ho_ume)
        self.action_HO_TMM.triggered.connect(self.do_ho_tmm)
        self.action_excel_split.triggered.connect(self.do_excel_split)
        self.action_excel_merge.triggered.connect(self.do_excel_merge)
        self.action_excel_index2col.triggered.connect(self.do_index2col)
        self.action_PDFs.triggered.connect(self.do_pdf)
        self.action_xml2excel.triggered.connect(self.xml2excel)
        self.action_guid.triggered.connect(self.read_guidance)
        self.action_pd.triggered.connect(self.f2n_n2f)
        self.action_EPMS.triggered.connect(self.epms)
        self.action_nei_nr.triggered.connect(self.do_nei_nr)
        self.action_nei_tmm.triggered.connect(self.do_nei_tmm)
        self.action_nei_icm.triggered.connect(self.do_nei_icm)
        self.action_clear_db.triggered.connect(self.clear_db)
        self.action_addnei_dl.triggered.connect(self.add_nei)

    def add_nei(self):
        try:
            from MyNeighbor.neighbor_add_main import MyNeighborAdd
            myApp = MyNeighborAdd()
            myApp.setWindowTitle('邻区添加')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def clear_db(self):
        from MyNeighbor.NeighborMain import my_sqlite
        my_sqlite1 = my_sqlite('cell_work.db')
        my_sqlite1.clear_database()
        my_sqlite1 = my_sqlite('icm_neighbor_work.db')
        my_sqlite1.clear_database()
        my_sqlite1 = my_sqlite('nr_neighbor_work.db')
        my_sqlite1.clear_database()
        my_sqlite1 = my_sqlite('tmm_neighbor_work.db')
        my_sqlite1.clear_database()

    def do_nei_icm(self):
        try:
            from MyNeighbor.neighbor_check_main import MyNeighborCheck
            myApp = MyNeighborCheck('icm')
            myApp.setWindowTitle('邻区核查-ICM')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_nei_tmm(self):
        try:
            from MyNeighbor.neighbor_check_main import MyNeighborCheck
            myApp = MyNeighborCheck('tmm')
            myApp.setWindowTitle('邻区核查-TMM')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_nei_nr(self):
        try:
            from MyNeighbor.neighbor_check_main import MyNeighborCheck
            myApp = MyNeighborCheck('nr')
            myApp.setWindowTitle('邻区核查-NR')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_ho_ume(self):
        try:
            from MyHOUME.ho_check_ume_main import MyHOCheckUME
            myApp = MyHOCheckUME()
            myApp.setWindowTitle('互操作核查-NR')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_ho_tmm(self):
        try:
            from MyHOUME.ho_tmm_main import MyHOCheckTMM
            myApp = MyHOCheckTMM()
            myApp.setWindowTitle('互操作核查-TMM')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def epms(self):
        try:
            from MyEpms.epms_main import MyEpmsAnalyse
            myApp = MyEpmsAnalyse()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')
            return

    def f2n_n2f(self):
        try:
            from MyFrequency.F2N import MyF2N
            myApp = MyF2N()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    @staticmethod
    def read_guidance():
        file_path = r'./guidance/guidance.docx'
        os.system(f'start {file_path}')

    def xml2excel(self):
        try:
            from MyXML.xml_hand_main import MyXmlHand
            myApp = MyXmlHand()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_pdf(self):
        try:
            from MyPDF.pdf_hand_main import MyPdfHand
            myApp = MyPdfHand()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_index2col(self):
        try:
            from MyExcel.excel_inx2col_main import MyExcelInx2Col
            myApp = MyExcelInx2Col()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_excel_merge(self):
        try:
            from MyExcel.excel_merger_main import MyExcelMerger
            myApp = MyExcelMerger()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_excel_split(self):
        try:
            from MyExcel.excel_split_main import MyExcelSpliter
            myApp = MyExcelSpliter()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_ho_icm(self):
        try:
            from MyHO.ho_check_main import MyHOCheckICM
            myApp = MyHOCheckICM()
            myApp.setWindowTitle('互操作核查')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_rs_ume(self):
        try:
            from MyRS.rs_check_main import MyRSCheckUME
            myApp = MyRSCheckUME()
            myApp.setWindowTitle('功率核查')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_rs_icm(self):
        try:
            from MyRS.rs_check_main import MyRSCheckICM
            myApp = MyRSCheckICM()
            myApp.setWindowTitle('功率核查')
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_neighbor(self):
        try:
            from MyPlan.ui_neighbor_main import MyNeighbor
            myApp = MyNeighbor()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')

    def do_pci(self):
        try:
            from MyPlan.ui_pci_main import MyPCI
            myApp = MyPCI()
            myApp.exec()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '信息提示', f'{traceback.format_exc()}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyHomeScreen('')
    sys.exit(app.exec())
