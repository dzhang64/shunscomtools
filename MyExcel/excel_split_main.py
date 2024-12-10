import os
import sys
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMessageBox, QDialog, QFileDialog
)

from MyExcel import excel_spliter
from MyExcel.excel_utils import MyExcel


class MyExcelSpliter(excel_spliter.Ui_ExcelSpliter, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()

        self.excel_path = []
        self.ExcelApp = MyExcel()
        self.pushButton_choose_excel.clicked.connect(
            self.do_choose_excel
        )

        self.output_dir = ""
        self.pushButton_choose_dir.clicked.connect(
            self.do_choose_dir
        )

        self.pushButton_do_split.clicked.connect(
            self.do_split
        )

    def do_split(self):
        if not self.excel_path:
            QMessageBox.warning(self, "信息提示", "请先选择excel文件")
            return

        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        if self.radioButton_context.isChecked():
            split_column = self.lineEdit_split_text.text()
            if not split_column:
                QMessageBox.warning(self, "信息提示", "请先选择拆分的列")
                return
            try:
                header_num = int(self.comboBox.currentText())
                self.ExcelApp.split_excels(self.excel_path, header_num, split_column, self.output_dir, on='text')
                QMessageBox.warning(self, "信息提示", "处理成功")
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")
        if self.radioButton_num.isChecked():
            split_size = int(self.lineEdit_split_size.text())
            if not split_size:
                QMessageBox.warning(self, "信息提示", "请输入要拆分的数目")
                return
            try:
                header_num = int(self.comboBox.currentText())
                self.ExcelApp.split_excels(self.excel_path, header_num, split_size, self.output_dir, on='num')
                QMessageBox.warning(self, "信息提示", "处理成功")
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_choose_dir(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        self.lineEdit_output_dir.setText(self.output_dir)

    def do_choose_excel(self):
        excel_paths, filetype = QFileDialog.getOpenFileNames(
            self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx *.csv *.xlsm *.xls)")

        self.listWidget.clear()
        self.listWidget.addItems(excel_paths)
        self.excel_path = excel_paths

        # df = self.ExcelApp.read_excels(self.excel_path)
        # columns = list(df.columns)
        # self.comboBox_split_column.clear()
        # self.comboBox_split_column.addItems(columns)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myExcelSpliter = MyExcelSpliter()
    myExcelSpliter.show()
    sys.exit(app.exec())
