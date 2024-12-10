import os
import sys
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QDialog, QFileDialog, QMessageBox
)

from MyExcel import excel_merger
from MyExcel.excel_utils import MyExcel


class MyExcelMerger(excel_merger.Ui_ExcelMerger, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()
        self.ExcelApp = MyExcel()
        self.pushButton_choose_dir.clicked.connect(
            self.do_choose_dir
        )

        self.pushButton_remove_excel.clicked.connect(
            self.do_remove_excel
        )

        self.pushButton_domerge_andsave.clicked.connect(
            self.do_merge_and_save
        )

    def do_merge_and_save(self):
        try:
            if self.listWidget_excel_paths.count() == 0:
                QMessageBox.warning(self, "信息提示", "要合并的列表为空")
                return
            excel_paths = []
            for idx in range(self.listWidget_excel_paths.count()):
                item = self.listWidget_excel_paths.item(idx)
                excel_paths.append(item.text())

            output_path, filetype = QFileDialog.getSaveFileName(
                self, "请保存文件", os.getcwd(), "Excel files (*.xlsx *.csv *.xlsm *.xls)"
            )
            header_num = int(self.comboBox.currentText())
            if self.radioButton.isChecked():
                print(1)
                self.ExcelApp.merge_excel_sheets(excel_paths, header_num, output_path)
            else:
                print(2)
                self.ExcelApp.merge_excel_sheet(excel_paths, header_num, output_path)
                # self.ExcelApp.merge_excels(excel_paths, output_path)
            QMessageBox.warning(self, "信息提示", "执行成功")
        except Exception as e:
            print(e, traceback.format_exc())

    def do_remove_excel(self):
        item = self.listWidget_excel_paths.currentItem()
        if item:
            row = self.listWidget_excel_paths.row(item)
            self.listWidget_excel_paths.takeItem(row)

    def do_choose_dir(self):
        # file_dir = QFileDialog.getExistingDirectory(self, "请选择目录", os.getcwd())
        excel_paths, filetype = QFileDialog.getOpenFileNames(
            self, "请选择excel文件", os.getcwd(), "Excel files (*.xlsx *.csv *.xlsm *.xls)")
        # self.lineEdit_dirpath.setText(file_dir)
        self.listWidget_excel_paths.clear()
        self.listWidget_excel_paths.addItems(excel_paths)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myExcelMerger = MyExcelMerger()
    myExcelMerger.show()
    sys.exit(app.exec())
