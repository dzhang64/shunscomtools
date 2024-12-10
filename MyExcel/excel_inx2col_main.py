import os
import traceback
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QAbstractItemView, QApplication
)

from MyExcel.excel_inx2col import Ui_Excelinx2col
from MyExcel.excel_utils import MyExcel


class MyExcelInx2Col(Ui_Excelinx2col, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()
        self.ExcelApp = MyExcel()
        self.output_dir = ""
        self.excel_path = ""
        self.listWidget_value.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.listWidget_inx.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.pushButton_choose_excel.clicked.connect(self.do_choose_excel)
        self.pushButton_choose_dir.clicked.connect(self.do_choose_dir)

        self.pushButton_remove_inx.clicked.connect(self.do_remove('inx'))
        self.pushButton_remove_col.clicked.connect(self.do_remove('col'))

        self.pushButton_do_inx2col.clicked.connect(self.do_inx2col)
        self.pushButton_do_col2inx.clicked.connect(self.do_col2inx)

    def do_col2inx(self):
        if not self.lineEdit_excel_path:
            QMessageBox.warning(self, "信息提示", "未选择excel文件")
            return
        if not self.lineEdit_output_dir:
            QMessageBox.warning(self, "信息提示", "未选择保存路径")
            return

        inx_v = []
        for idx in range(self.listWidget_inx.count()):
            item = self.listWidget_inx.item(idx)
            inx_v.append(item.text())
        val = []
        for idx in range(self.listWidget_value.count()):
            item = self.listWidget_value.item(idx)
            val.append(item.text())
        if not inx_v:
            QMessageBox.warning(self, "信息提示", "inx不能为空")
            return
        if not val:
            QMessageBox.warning(self, "信息提示", "value不能为空")
            return
        try:
            self.ExcelApp.do_col2inx(self.excel_path, self.output_dir, inx_v, val)
            QMessageBox.warning(self, "信息提示", "处理成功")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_inx2col(self):
        if not self.lineEdit_excel_path:
            QMessageBox.warning(self, "信息提示", "未选择excel文件")
            return
        if not self.lineEdit_output_dir:
            QMessageBox.warning(self, "信息提示", "未选择保存路径")
            return

        inx_v = []
        for idx in range(self.listWidget_inx.count()):
            item = self.listWidget_inx.item(idx)
            inx_v.append(item.text())
        val = []
        for idx in range(self.listWidget_value.count()):
            item = self.listWidget_value.item(idx)
            val.append(item.text())
        if not inx_v:
            QMessageBox.warning(self, "信息提示", "inx不能为空")
            return
        if not val:
            QMessageBox.warning(self, "信息提示", "value不能为空")
            return
        if len(val) > 1:
            QMessageBox.warning(self, "信息提示", "value只能为一列")
            return
        try:
            self.ExcelApp.do_inx2col(self.excel_path, self.output_dir, inx_v, val[0])
            QMessageBox.warning(self, "信息提示", "处理成功")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_remove(self, para):
        def func():
            if para == 'col':
                selected_items = self.listWidget_value.selectedItems()
                for item in selected_items:
                    row = self.listWidget_value.row(item)
                    self.listWidget_value.takeItem(row)
            else:
                selected_items = self.listWidget_inx.selectedItems()
                for item in selected_items:
                    row = self.listWidget_inx.row(item)
                    self.listWidget_inx.takeItem(row)

        return func

    def do_choose_excel(self):
        try:
            self.excel_path, filetype = QFileDialog.getOpenFileName(
                self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx *.csv)")
            self.lineEdit_excel_path.setText(self.excel_path)

            df = self.ExcelApp.read_excels(self.excel_path)
            columns = [str(i) for i in df.columns]
            self.listWidget_inx.clear()
            self.listWidget_inx.addItems(columns)
            self.listWidget_value.clear()
            self.listWidget_value.addItems(columns)
        except:
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")
            print(traceback.format_exc())

    def do_choose_dir(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        self.lineEdit_output_dir.setText(self.output_dir)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myExcelMerger = MyExcelInx2Col()
    myExcelMerger.show()
    sys.exit(app.exec())
