import os
import sys
import traceback
import pandas as pd

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QAbstractItemView, QApplication
)

from OtherFunctions.association import north_cm
from MyHOUME.HO_UME import Ui_HO_UME


class MyHOCheckUME(Ui_HO_UME, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()

        self.output_dir = ""
        self.excel_path = ""
        self.listWidget_excel_paths.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.pushButton_choose_dir.clicked.connect(self.do_choose_excel)
        self.pushButton_remove_excel.clicked.connect(self.do_remove)
        self.pushButton_doandsave.clicked.connect(self.do_ho)

    def do_ho(self):

        if self.listWidget_excel_paths.count() == 0:
            QMessageBox.warning(self, "信息提示", "文件为空")
            return
        excel_paths = []

        for idx in range(self.listWidget_excel_paths.count()):
            item = self.listWidget_excel_paths.item(idx)
            excel_paths.append(item.text())

        if not self.lineEdit_ho.text():
            QMessageBox.warning(self, "信息提示", "切换的对象标识未填写")
            return
        if not self.lineEdit_A1A2.text():
            QMessageBox.warning(self, "信息提示", "A1A2的对象标识未填写")
            return

        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return

        if excel_paths:
            try:
                MyNorth = north_cm(excel_paths, self.output_dir)
                if self.radioButton_nr.isChecked():
                    MyNorth.hand_nr_nr_ho(self.lineEdit_ho.text(), self.lineEdit_A1A2.text())
                    MyNorth.hand_nr_nr_res()
                else:
                    MyNorth.hand_nr_lte_ho(self.lineEdit_ho.text(), self.lineEdit_A1A2.text())
                    MyNorth.hand_nr_lte_res()
            except:
                QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_remove(self):
        selected_items = self.listWidget_excel_paths.selectedItems()
        for item in selected_items:
            row = self.listWidget_excel_paths.row(item)
            self.listWidget_excel_paths.takeItem(row)

    def do_choose_excel(self):
        self.excel_path, filetype = QFileDialog.getOpenFileNames(
            self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx)")
        self.listWidget_excel_paths.clear()
        self.listWidget_excel_paths.addItems(self.excel_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyHOCheckUME()
    sys.exit(app.exec())
