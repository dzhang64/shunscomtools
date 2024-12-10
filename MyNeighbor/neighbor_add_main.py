import datetime
import sys
import shutil
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QApplication
)

from MyNeighbor.add_nei import *
from MyNeighbor.add_neighbor import Ui_add_neighbor


class MyNeighborAdd(Ui_add_neighbor, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()

        self.output_dir = ""
        self.excel_path = ""

        self.pushButton_choose_cell.clicked.connect(self.do_choose_excel('cell'))
        self.pushButton_choose_nei.clicked.connect(self.do_choose_excel('nei'))
        self.pushButton_cell_ex.clicked.connect(self.export('cell'))
        self.pushButton_nei_ex.clicked.connect(self.export('nei'))
        self.pushButton_add.clicked.connect(self.add)

    def export(self, ty):
        def func():
            if ty == 'cell':
                output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
                file_path = os.path.abspath(r'.\config\MyNeighbor\小区信息模板.xlsx')
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
                self.excel_path, filetype = QFileDialog.getOpenFileName(self, "请选择excel文件", os.getcwd(),
                                                                        "Excel files (*.xlsx)")
                self.textBrowser_log.append(f'{datetime.datetime.now()}:导入小区信息')
                import_cell(self.excel_path)
                self.textBrowser_log.append(f'{datetime.datetime.now()}:完成小区信息导入')
                QApplication.processEvents()

            else:

                self.excel_path, filetype = QFileDialog.getOpenFileName(self, "请选择excel文件", os.getcwd(),
                                                                        "Excel files (*.xlsx)")
                self.textBrowser_log.append(f'{datetime.datetime.now()}:导入邻区对')
                QApplication.processEvents()
                import_nei(self.excel_path)
                self.textBrowser_log.append(f'{datetime.datetime.now()}:完成邻区对导入')
                QApplication.processEvents()

        return func

    def add(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            do_add_nei(self.output_dir)
            self.textBrowser_log.append(f'{datetime.datetime.now()}:保存路径{self.output_dir}')
            QApplication.processEvents()
        except:
            self.textBrowser_log.append(f'{datetime.datetime.now()}:{traceback.format_exc()}')
            QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyNeighborAdd()
    sys.exit(app.exec())
