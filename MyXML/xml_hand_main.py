import os
import sys
import traceback
from PyQt6.QtWidgets import (QDialog, QMessageBox, QFileDialog, QApplication, QAbstractItemView)

from MyXML.Ui_Xml import Ui_XMLHand
from MyXML.xml_hand import MyXml


class MyXmlHand(Ui_XMLHand, QDialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.show()
        self.output_dir = ""
        self.listWidget_xml_paths.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.pushButton_choose_dir.clicked.connect(self.do_choose_dir)

        self.pushButton_remove_xml.clicked.connect(self.do_remove_xml)

        self.pushButton_do_convert.clicked.connect(self.do_convert)

    def do_convert(self):
        if self.listWidget_xml_paths.count() == 0:
            QMessageBox.warning(self, "信息提示", "要合并的列表为空")
            return
        xml_paths = []

        for idx in range(self.listWidget_xml_paths.count()):
            item = self.listWidget_xml_paths.item(idx)
            xml_paths.append(item.text())

        self.output_dir = QFileDialog.getExistingDirectory(self, "请选择保存目录", os.getcwd())
        print(self.output_dir)
        if not os.path.exists(self.output_dir):
            QMessageBox.warning(self, "信息提示", "请先选择输出目录")
            return

        try:
            myXml = MyXml(xml_paths, self.output_dir)
            myXml.xml2excel()
            QMessageBox.warning(self, "信息提示", "处理成功")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "信息提示", f"{traceback.format_exc()}")

    def do_remove_xml(self):
        selected_items = self.listWidget_xml_paths.selectedItems()
        for item in selected_items:
            row = self.listWidget_xml_paths.row(item)
            self.listWidget_xml_paths.takeItem(row)

    def do_choose_dir(self):
        xml_paths, filetype = QFileDialog.getOpenFileNames(self, "请选择excel文件", os.getcwd(), "(*.xml)")
        self.listWidget_xml_paths.clear()
        self.listWidget_xml_paths.addItems(xml_paths)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myExcelMerger = MyXmlHand()

    # home = MyHomeScreen(myExcelMerger.username)
    # home.show()
    # myExcelMerger.show()
    sys.exit(app.exec())
