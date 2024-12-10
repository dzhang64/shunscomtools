import os
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QAbstractItemView
)

from MyHOUME.TMMHO import ho_tmm
from MyRS.para_check import Ui_ParaCheck


class MyHOCheckTMM(Ui_ParaCheck, QDialog):
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
            QMessageBox.warning(self, "信息提示", "要合并的列表为空")
            return
        excel_paths = []

        for idx in range(self.listWidget_excel_paths.count()):
            item = self.listWidget_excel_paths.item(idx)
            excel_paths.append(item.text())

        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return
        try:
            info = ho_tmm(excel_paths, self.output_dir)
            QMessageBox.warning(self, "信息提示", f"{info}")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_remove(self):
        selected_items = self.listWidget_excel_paths.selectedItems()
        for item in selected_items:
            row = self.listWidget_excel_paths.row(item)
            self.listWidget_excel_paths.takeItem(row)

    def do_choose_excel(self):
        self.excel_path, filetype = QFileDialog.getOpenFileNames(
            self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx *.csv)")
        self.listWidget_excel_paths.clear()
        self.listWidget_excel_paths.addItems(self.excel_path)
