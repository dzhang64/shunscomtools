import os
import sys
import traceback
from PyQt6.QtWidgets import (QDialog, QMessageBox, QFileDialog, QApplication, QAbstractItemView)

from MyPDF.Ui_PDF import Ui_PDFHand
from MyPDF.pdf_hand import MyPDF


class MyPdfHand(Ui_PDFHand, QDialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.show()
        self.output_dir = ""
        self.input = []
        self.step = int(self.lineEdit_step.text())
        self.pages = []
        self.start = 0
        self.end = None
        self.listWidget_pdf_paths.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.pushButton_choose_dir.clicked.connect(self.do_choose_dir)
        self.pushButton_remove_pdf.clicked.connect(self.do_remove_pdf)
        self.pushButton_do_split.clicked.connect(self.do_split)
        self.pushButton_do_merge.clicked.connect(self.do_merge)
        self.pushButton_do_convert.clicked.connect(self.do_convert)
        self.pushButton_pdf2word.clicked.connect(self.do_pdf2word)
        self.pushButton_pdf2low.clicked.connect(self.do_pdf2low)

    def do_convert(self):
        if self.listWidget_pdf_paths.count() == 0:
            QMessageBox.warning(self, "信息提示", "未选择PDF文件")
            return
        pdf_paths = []
        for idx in range(self.listWidget_pdf_paths.count()):
            item = self.listWidget_pdf_paths.item(idx)
            pdf_paths.append(item.text())
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        myPDF = MyPDF(pdf_paths, self.output_dir)

        if self.radioButton.isChecked():
            self.pages = self.lineEdit_list.text().split(',')
            print(self.pages)
            try:
                myPDF.pdf2doc(pages=self.pages)
                QMessageBox.warning(self, "信息提示", "处理成功")
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

        else:
            try:
                self.start = int(self.lineEdit_start.text())
                self.end = int(self.lineEdit_end.text())
            except Exception as e:
                print(e)
            try:
                myPDF.pdf2doc(self.start, self.end)
                QMessageBox.warning(self, "信息提示", "处理成功")
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_split(self):
        if self.listWidget_pdf_paths.count() == 0:
            QMessageBox.warning(self, "信息提示", "未选择PDF文件")
            return

        if not self.step:
            QMessageBox.warning(self, "信息提示", "请输入拆分步长")
            return
        pdf_paths = []
        for idx in range(self.listWidget_pdf_paths.count()):
            item = self.listWidget_pdf_paths.item(idx)
            pdf_paths.append(item.text())
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        myPDF = MyPDF(pdf_paths, self.output_dir)
        try:
            myPDF.split_pdf(self.step)
            QMessageBox.warning(self, "信息提示", "处理成功")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_merge(self):
        if self.listWidget_pdf_paths.count() == 0:
            QMessageBox.warning(self, "信息提示", "未选择PDF文件")
            return
        pdf_paths = []
        for idx in range(self.listWidget_pdf_paths.count()):
            item = self.listWidget_pdf_paths.item(idx)
            pdf_paths.append(item.text())
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        myPDF = MyPDF(pdf_paths, self.output_dir)
        try:
            myPDF.concat_pdf()
            QMessageBox.warning(self, "信息提示", "处理成功")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_pdf2word(self):
        if self.listWidget_pdf_paths.count() == 0:
            QMessageBox.warning(self, "信息提示", "未选择PDF文件")
            return
        pdf_paths = []
        for idx in range(self.listWidget_pdf_paths.count()):
            item = self.listWidget_pdf_paths.item(idx)
            pdf_paths.append(item.text())
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        myPDF = MyPDF(pdf_paths, self.output_dir)
        try:
            myPDF.pdf2word()
            QMessageBox.warning(self, "信息提示", "处理成功")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_pdf2low(self):
        if self.listWidget_pdf_paths.count() == 0:
            QMessageBox.warning(self, "信息提示", "未选择PDF文件")
            return
        pdf_paths = []
        for idx in range(self.listWidget_pdf_paths.count()):
            item = self.listWidget_pdf_paths.item(idx)
            pdf_paths.append(item.text())
        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        myPDF = MyPDF(pdf_paths, self.output_dir)
        try:
            myPDF.pdf2low()
            QMessageBox.warning(self, "信息提示", "处理成功")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_remove_pdf(self):
        selected_items = self.listWidget_pdf_paths.selectedItems()
        for item in selected_items:
            row = self.listWidget_pdf_paths.row(item)
            self.listWidget_pdf_paths.takeItem(row)

    def do_choose_dir(self):
        xml_paths, filetype = QFileDialog.getOpenFileNames(self, "请选择PDF文件", os.getcwd(), "(*.pdf)")
        self.listWidget_pdf_paths.clear()
        self.listWidget_pdf_paths.addItems(xml_paths)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    MyApp = MyPdfHand()

    sys.exit(app.exec())
