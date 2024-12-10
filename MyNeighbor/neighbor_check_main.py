import datetime
import sys
import shutil
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QApplication
)

from MyNeighbor.NeighborMain import *
from MyNeighbor.neighbor import Ui_neighbor


class MyNeighborCheck(Ui_neighbor, QDialog, neighbor_check):
    def __init__(self, fon):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()

        self.output_dir = ""
        self.excel_path = ""
        self.fon = fon

        self.pushButton_choose_cell.clicked.connect(self.do_choose_excel('cell'))
        self.pushButton_choose_ycell.clicked.connect(self.do_choose_excel('ycell'))
        self.pushButton_choose_nei.clicked.connect(self.do_choose_excel('nei'))
        self.pushButton_ex.clicked.connect(self.consistence)
        self.pushButton_dy.clicked.connect(self.redundance)
        self.pushButton_hx.clicked.connect(self.confusion)
        self.pushButton_ct.clicked.connect(self.conflict)
        self.pushButton_num.clicked.connect(self.num)
        self.pushButton_m3.clicked.connect(self.m3)
        self.pushButton_nei_red.clicked.connect(self.nei_redu)
        self.pushButton_cell_ex.clicked.connect(self.export('cell'))

    def export(self, ty):
        def func():
            if ty == 'cell':
                output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
                file_path = os.path.abspath(r'.\config\MyNeighbor\异厂家小区信息模板.xlsx')
                shutil.copy(file_path, os.path.join(output_dir, os.path.basename(file_path)))
                os.system(f'start {os.path.join(output_dir, os.path.basename(file_path))}')

            else:
                output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
                file_path = os.path.abspath(r'.\config\MyNeighbor\邻区对模板.xlsx')
                shutil.copy(file_path, os.path.join(output_dir, os.path.basename(file_path)))
                os.system(f'start {os.path.join(output_dir, os.path.basename(file_path))}')

        return func

    def do_choose_excel(self, ty):
        def func():
            if ty == 'cell':
                self.excel_path, filetype = QFileDialog.getOpenFileNames(
                    self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx)")
                self.textBrowser_log.append(f'{datetime.datetime.now()}:导入小区信息')
                QApplication.processEvents()
                for i in self.excel_path:
                    self.textBrowser_log.append(f'{datetime.datetime.now()}:导入小区信息-{i}')
                    QApplication.processEvents()
                    import_cell(i)
                self.textBrowser_log.append(f'{datetime.datetime.now()}:完成小区信息')
                QApplication.processEvents()
                QMessageBox.warning(self, "信息提示", f"完成小区信息")
            elif ty == 'ycell':
                self.excel_path, filetype = QFileDialog.getOpenFileNames(
                    self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx)")
                self.textBrowser_log.append(f'{datetime.datetime.now()}:导入小区信息')
                QApplication.processEvents()
                for i in self.excel_path:
                    self.textBrowser_log.append(f'{datetime.datetime.now()}:导入小区信息-{i}')
                    QApplication.processEvents()
                    import_y_cell(i)
                self.textBrowser_log.append(f'{datetime.datetime.now()}:完成小区信息')
                QApplication.processEvents()
                QMessageBox.warning(self, "信息提示", f"完成小区信息")
            else:
                try:
                    self.excel_path, filetype = QFileDialog.getOpenFileNames(
                        self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx)")
                    self.textBrowser_log.append(f'{datetime.datetime.now()}:导入邻区信息')
                    QApplication.processEvents()
                    for i in self.excel_path:
                        self.textBrowser_log.append(f'{datetime.datetime.now()}:导入邻区信息-{i}')
                        QApplication.processEvents()
                        import_neighbor(i, self.fon, dic[self.fon])
                    self.textBrowser_log.append(f'{datetime.datetime.now()}:完成邻区信息')
                    QApplication.processEvents()
                    QMessageBox.warning(self, "信息提示", f"完成邻区信息")
                except:
                    print(traceback.format_exc())
                    self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
                    QApplication.processEvents()

        return func

    def consistence(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            self.Consistency(self.fon, self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()

    def redundance(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            self.redundancy(self.fon, self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()

    def confusion(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            self.pci_Confusion(self.fon, self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()

    def conflict(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            self.pci_Conflict(self.fon, self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()

    def num(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            self.nei_num(self.fon, self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()

    def m3(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            self.m3_Conflict(self.fon, self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()

    def nei_redu(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            self.nei_redundance(self.fon, self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyNeighborCheck('icm')
    sys.exit(app.exec())
