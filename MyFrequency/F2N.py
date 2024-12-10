import os
import sys
import traceback
from decimal import Decimal
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMessageBox, QDialog, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
)

from MyFrequency import Frequency
from MyFrequency.F_function import gscn_print, rb_print, ssb_print, step_print, Band_print


class MyF2N(Frequency.Ui_Dialog_F2N, QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.setupUi(self)
        self.show()

        self.lte_f = [[1.0, 2110.0, 0.0, 1920.0, 18000.0, 599.0],
                      [2.0, 1930.0, 600.0, 1850.0, 18600.0, 599.0],
                      [3.0, 1805.0, 1200.0, 1710.0, 19200.0, 749.0],
                      [4.0, 2110.0, 1950.0, 1710.0, 19950.0, 449.0],
                      [5.0, 869.0, 2400.0, 824.0, 20400.0, 249.0],
                      [6.0, 875.0, 2650.0, 830.0, 20650.0, 99.0],
                      [7.0, 2620.0, 2750.0, 2500.0, 20750.0, 699.0],
                      [8.0, 925.0, 3450.0, 880.0, 21450.0, 349.0],
                      [9.0, 1844.9, 3800.0, 1749.9, 21800.0, 349.0],
                      [10.0, 2110.0, 4150.0, 1710.0, 22150.0, 599.0],
                      [11.0, 1475.9, 4750.0, 1427.9, 22750.0, 199.0],
                      [12.0, 729.0, 5010.0, 699.0, 23010.0, 169.0],
                      [13.0, 746.0, 5180.0, 777.0, 23180.0, 99.0],
                      [14.0, 758.0, 5280.0, 788.0, 23280.0, 99.0],
                      [17.0, 734.0, 5730.0, 704.0, 23730.0, 119.0],
                      [18.0, 860.0, 5850.0, 815.0, 23850.0, 149.0],
                      [19.0, 875.0, 6000.0, 830.0, 24000.0, 149.0],
                      [20.0, 791.0, 6150.0, 832.0, 24150.0, 299.0],
                      [21.0, 1495.9, 6450.0, 1447.9, 24450.0, 149.0],
                      [22.0, 3510.0, 6600.0, 3410.0, 24600.0, 799.0],
                      [23.0, 2180.0, 7500.0, 2000.0, 25500.0, 199.0],
                      [24.0, 1525.0, 7700.0, 1626.5, 25700.0, 339.0],
                      [25.0, 1930.0, 8040.0, 1850.0, 26040.0, 649.0],
                      [26.0, 859.0, 8690.0, 814.0, 26690.0, 349.0],
                      [27.0, 852.0, 9040.0, 807.0, 27040.0, 169.0],
                      [28.0, 758.0, 9210.0, 703.0, 27210.0, 449.0],
                      [33.0, 1900.0, 36000.0, 1900.0, 36000.0, 199.0],
                      [34.0, 2010.0, 36200.0, 2010.0, 36200.0, 149.0],
                      [35.0, 1850.0, 36350.0, 1850.0, 36350.0, 599.0],
                      [36.0, 1930.0, 36950.0, 1930.0, 36950.0, 599.0],
                      [37.0, 1910.0, 37550.0, 1910.0, 37550.0, 199.0],
                      [38.0, 2570.0, 37750.0, 2570.0, 37750.0, 499.0],
                      [39.0, 1880.0, 38250.0, 1880.0, 38250.0, 399.0],
                      [40.0, 2300.0, 38650.0, 2300.0, 38650.0, 999.0],
                      [41.0, 2496.0, 39650.0, 2496.0, 39650.0, 1939.0],
                      [42.0, 3400.0, 41590.0, 3400.0, 41590.0, 1999.0],
                      [43.0, 3600.0, 43590.0, 3600.0, 43590.0, 1999.0],
                      [44.0, 703.0, 45590.0, 703.0, 45590.0, 999.0]]
        self.Frequency = None

        self.pushButton_f2n_lte.clicked.connect(
            self.f2n_lte)
        self.pushButton_n2f_lte.clicked.connect(
            self.n2f_lte)
        self.pushButton_f2n_nr.clicked.connect(
            self.Nref_point)
        self.pushButton_n2f_nr.clicked.connect(
            self.Fref_point)

    def Fref_point(self):
        self.clear()
        # 判断用户输入的中心频率是否合法
        try:
            Nref = float(self.lineEdit_pd_nr.text())
        except:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return

        if not int(float(Nref)) > 0:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return


        # 判断用户输入的小区带宽是否合法
        try:
            bandwidth = int(self.lineEdit_bandwidth.text())
        except:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return
        if not bandwidth in [5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 200, 400]:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")

        # 判断用户输入的子载波间隔是否合法
        try:
            Scs = int(self.lineEdit_scs.text())
        except:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return
        while True:

            if int(bandwidth) < 51 and int(Scs) == 15:
                break
            elif int(bandwidth) < 101 and int(Scs) == 30:
                break
            elif int(bandwidth) > 11 and int(bandwidth) < 101 and int(Scs) == 60:
                break
            elif int(bandwidth) > 51 and int(bandwidth) < 101 and int(Scs) == 120:
                break
            else:
                QMessageBox.warning(self, "信息提示", "不合规请重新输入")
                return




        if int(Nref) < 599999:
            F_global = 5 * 10 ** -3
            Fref_offs = 0
            Nref_offs = 0
        elif int(Nref) < 2016666:
            F_global = 15 * 10 ** -3
            Fref_offs = 3000
            Nref_offs = 600000

        elif int(Nref) < 3279167:
            F_global = 60 * 10 ** -3
            Fref_offs = 24250
            Nref_offs = 2016667
        else:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")

        Band = Band_print(int(Nref))  # 频带获取

        Step_size = int(step_print(int(Scs), Band))  # 频点栅格步长获取

        Fref = round(float(Decimal(str(Fref_offs)) + Decimal(str(F_global)) * (Decimal(str(Nref)) - Decimal(str(Nref_offs)))), 2) # 中心频率计算

        Rb_number = rb_print(int(Scs), str(int(bandwidth)))  # NRB数据获取

        SSB_ref = ssb_print(Rb_number, int(Nref), int(Scs), F_global)  # SSB频点获取

        Gscn = gscn_print(int(Fref))  # GSCN获取

        # print('\n计算结果如下：')
        # print('    中心频率：', Fref, 'MHz')
        # print('    小区带宽：', bandwidth, 'MHz')
        # print('    载波间隔：', Scs, 'KHz')
        # print('    NRB个数：', Rb_number)
        # print('    频点栅格：', int(F_global * 10 ** 3), 'KHz')
        # print('    中心频点:', int(Nref))
        # print('    SSB频点:', int(SSB_ref))
        # print('    GSCN频点:', Gscn)
        # print('    小区频带:', Band)
        # print('    频点步长:', Step_size)
        res = [Fref, bandwidth, Scs, Rb_number, int(Nref), int(SSB_ref), Band]

        self.tableWidget.setColumnCount(len(res))
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["中心频率", "小区带宽", "载波间隔", "NRB个数", "中心频点", 'SSB频点', '小区频带'])
        if res:
            try:
                for i in range(1):
                    for j in range(len(res)):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(f"{res[j]}"))
            except:
                print(traceback.format_exc())

    def Nref_point(self):


        self.clear()
        # 判断用户输入的中心频率是否合法
        try:
            Fref = float(self.lineEdit_pd_nr.text())
        except:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return

        if not int(float(Fref)) > 0:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return


        # 判断用户输入的小区带宽是否合法
        try:
            bandwidth = int(self.lineEdit_bandwidth.text())
        except:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return
        if not bandwidth in [5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 200, 400]:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")

        # 判断用户输入的子载波间隔是否合法
        try:
            Scs = int(self.lineEdit_scs.text())
        except:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")
            return
        while True:

            if int(bandwidth) < 51 and int(Scs) == 15:
                break
            elif int(bandwidth) < 101 and int(Scs) == 30:
                break
            elif int(bandwidth) > 11 and int(bandwidth) < 101 and int(Scs) == 60:
                break
            elif int(bandwidth) > 51 and int(bandwidth) < 101 and int(Scs) == 120:
                break
            else:
                QMessageBox.warning(self, "信息提示", "不合规请重新输入")
                return


        if int(Fref) < 3000:
            F_global = 5 * 10 ** -3
            Fref_offs = 0
            Nref_offs = 0
        elif int(Fref) < 24250:
            F_global = 15 * 10 ** -3
            Fref_offs = 3000
            Nref_offs = 600000
        elif int(Fref) < 100000:
            F_global = 60 * 10 ** -3
            Fref_offs = 24250
            Nref_offs = 2016667
        else:
            QMessageBox.warning(self, "信息提示", "不合规请重新输入")

        try:
            Nref = float((Decimal(str(Fref)) - Decimal(str(Fref_offs))) / Decimal(str(F_global)) + Decimal(str(Nref_offs)))  # 中心频点计算

            Band = Band_print(Nref)  # 频带获取
            print(Band)

            Step_size = int(step_print(int(Scs), Band))  # 频点栅格步长获取
            print(Step_size)

            # 中心频点修正
            # while int(Nref) % Step_size != 0:
            #     Nref += 1
            #     print(Nref)

            Rb_number = rb_print(int(Scs), str(int(bandwidth)))  # NRB数据获取

            SSB_ref = ssb_print(Rb_number, Nref, int(Scs), F_global)  # SSB频点获取

            Gscn = gscn_print(float(Fref))  # GSCN获取
        except:
            print(traceback.format_exc())
            return

        # print('\n计算结果如下：')
        # print('    中心频率：', Fref, 'MHz')
        # print('    小区带宽：', bandwidth, 'MHz')
        # print('    载波间隔：', Scs, 'KHz')
        # print('    NRB个数：', Rb_number)
        # print('    频点栅格：', int(F_global * 10 ** 3), 'KHz')
        # print('    中心频点:', int(Nref))
        # print('    SSB频点:', int(SSB_ref))
        # print('    GSCN频点:', Gscn)
        # print('    小区频带:', Band)
        # print('    频点步长:', Step_size)
        res = [Fref, bandwidth, Scs, Rb_number, int(Nref), int(SSB_ref), Band]

        self.tableWidget.setColumnCount(len(res))
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["中心频率", "小区带宽", "载波间隔", "NRB个数", "中心频点", 'SSB频点', '小区频带'])
        if res:
            try:
                for i in range(1):
                    for j in range(len(res)):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(f"{res[j]}"))
            except:
                print(traceback.format_exc())


    def n2f_lte(self):
        self.clear()
        self.Frequency = float(self.lineEdit_pd_lte.text())
        if not self.Frequency:
            QMessageBox.warning(self, "信息提示", "请输入频率或者频点号")
            return
        res = self.n2f(self.Frequency, self.lte_f)
        # print(res)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(["Band", "下行频率", "下行频点", "上行频率", "上行频点"])

        if res:
            try:
                for i in range(len(res)):
                    for j in range(5):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(f"{res[i][j]}"))
            except:
                print(traceback.format_exc())

    def n2f(self, f, lte):
        res = []
        for i in lte:
            if i[2] <= f <= i[2] + i[-1]:
                band = int(i[0])
                DL = self.float2int(float((Decimal(str(f)) - Decimal(str(i[2]))) / 10 + Decimal(str(i[1]))))
                DL_N = self.float2int(float(Decimal(str(f))))
                UL = self.float2int(float((Decimal(str(f)) - Decimal(str(i[2]))) / 10 + Decimal(str(i[3]))))
                UL_N = self.float2int(float(Decimal(str(f)) - Decimal(str(i[2])) + Decimal(str(i[4]))))
                if DL == UL:
                    re = [band, DL, DL_N, '-', '-']
                else:
                    re = [band, DL, DL_N, UL, UL_N]
                if re not in res:
                    res.append(re)
            if i[4] <= f <= i[4] + i[-1]:
                band = int(i[0])
                DL = self.float2int(float((Decimal(str(f)) - Decimal(str(i[4]))) / 10 + Decimal(str(i[1]))))
                DL_N = self.float2int(float(Decimal(str(f)) - Decimal(str(i[4])) + Decimal(str(i[2]))))
                UL = self.float2int(float((Decimal(str(f)) - Decimal(str(i[4]))) / 10 + Decimal(str(i[3]))))
                UL_N = self.float2int(float(Decimal(str(f))))

                if DL == UL:
                    re = [band, DL, DL_N, '-', '-']
                else:
                    re = [band, DL, DL_N, UL, UL_N]
                if re not in res:
                    res.append(re)
        return res

    def f2n_lte(self):
        self.clear()
        self.Frequency = float(self.lineEdit_pd_lte.text())
        if not self.Frequency:
            QMessageBox.warning(self, "信息提示", "请输入频率或者频点号")
            return
        res = self.f2n(self.Frequency, self.lte_f)
        print(res)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(["Band", "下行频率", "下行频点", "上行频率", "上行频点"])

        if res:
            try:
                for i in range(len(res)):
                    for j in range(5):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(f"{res[i][j]}"))
            except:
                print(traceback.format_exc())

    def clear(self):
        row_count = self.tableWidget.rowCount()
        # 循环删除每一行
        for row in range(row_count):
            self.tableWidget.removeRow(0)

    def f2n(self, f, lte):
        res = []
        for i in lte:
            if i[1] <= f <= i[1] + i[-1] * 0.1:
                band = int(i[0])
                DL = self.float2int(float(Decimal(str(f))))
                DL_N = self.float2int(float((Decimal(str(f)) - Decimal(str(i[1]))) * 10 + Decimal(str(i[2]))))
                UL = self.float2int(float(Decimal(str(f)) - Decimal(str(i[1])) + Decimal(str(i[3]))))
                UL_N = self.float2int(float((Decimal(str(f)) - Decimal(str(i[1]))) * 10 + Decimal(str(i[4]))))
                if DL == UL:
                    re = [band, DL, DL_N, '-', '-']
                else:
                    re = [band, DL, DL_N, UL, UL_N]
                if re not in res:
                    res.append(re)
            if i[3] <= f <= i[3] + i[-1] * 0.1:
                band = int(i[0])
                DL = self.float2int(float(Decimal(str(f)) - Decimal(str(i[3])) + Decimal(str(i[1]))))
                DL_N = self.float2int(float((Decimal(str(f)) - Decimal(str(i[3]))) * 10 + Decimal(str(i[2]))))
                UL = self.float2int(float(Decimal(str(f))))
                UL_N = self.float2int(float((Decimal(str(f)) - Decimal(str(i[3]))) * 10 + Decimal(str(i[4]))))

                if DL == UL:
                    re = [band, DL, DL_N, '-', '-']
                else:
                    re = [band, DL, DL_N, UL, UL_N]
                if re not in res:
                    res.append(re)
        return res

    @staticmethod
    def float2int(f):
        if str(f).split('.')[-1] == '0':
            # print(str(f).split('.')[-1])
            return int(f)
        else:
            return f


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myExcelSpliter = MyF2N()
    # myExcelSpliter.show()
    sys.exit(app.exec())
