import xlwings as xw
import glob
import os
import pandas as pd


# pd.read_excel('',skiprows=1,)
def merge_xlsm(excel_paths, ):
    """
    合并不同的excel的不同sheet进行合并到一个
    :param excel_paths: 列表，多个excel路径
    :param output_path: 合并后的excel路径
    """
    # 获取指定目录中的所有xlsm文件路径
    excel_paths = glob.glob(os.path.join(excel_paths, '*.xlsm'))

    if excel_paths:
        app = xw.App(visible=False, add_book=False)
        wb1 = app.books.add()

        for path in excel_paths:
            print()
            wb = app.books.open(path)
            print(wb.sheets)


# merge_xlsm(r'F:\shunscomtools\IntegrationTool\MyExcel')


def split_excel(file_path, header_num, split_name):
    """
    按条件将一个工作表拆分为多个工作表
    :param file_path: 给出来源工作簿的文件路径及工作簿名称
    :param header_num: 表头行数
    :param split_name: 拆分列名称
    :return:
    """
    app = xw.App(visible=False, add_book=False)
    workbook = app.books.open(file_path)
    sheet_names = list(reversed([j.name for j in workbook.sheets]))

    result_dic = {}  # {index:{sheetName:pandas}}
    result_dic_NON = {}  # {sheetName:pandas}
    for sheet_name in sheet_names:
        worksheet = workbook.sheets[sheet_name]
        # 以DataFrame格式读取要拆分的工作表数据
        value = worksheet.range(worksheet.used_range).options(pd.DataFrame).value  # 读取要拆分的工作表中的所有数据
        value_header = value.iloc[0:header_num - 1, :]  # 获取表头
        value_data = value.iloc[header_num - 1:value.shape[0], :]  # 获取表格内容
        # 将数据按照“名称”分组
        if split_name in value_data.columns:
            data = value_data.groupby(split_name)
            for idx, group in data:
                print(idx)
                # 如果工作簿的工作表名不存在，则新增，否则替换
                if idx not in result_dic.keys():
                    result_dic[idx] = {}
                    result_dic[idx][sheet_name] = pd.concat([value_header, group], join='outer', axis=0)
                else:
                    if sheet_name not in result_dic[idx].keys():
                        result_dic[idx][sheet_name] = pd.concat([value_header, group], join='outer', axis=0)
                    else:
                        result_dic[idx][sheet_name] = pd.concat([result_dic[idx][sheet_name], group], join='outer',
                                                                axis=0)

        else:
            if sheet_name not in result_dic_NON.keys():
                result_dic_NON[sheet_name] = pd.concat([value_header, value_data], join='outer', axis=0)
            else:
                result_dic_NON[sheet_name] = pd.concat([result_dic_NON[sheet_name], value_data], join='outer', axis=0)

    workbook.close()
    app.quit()

    if result_dic:
        for idx, sheetName in result_dic.items():
            new = xw.App(visible=False, add_book=False)

            na = list(sheetName.keys())+list(result_dic_NON.keys())
            print(na)
            new_wb = new.books.add()

            if sheetName:
                for sheet1, value1 in sheetName.items():
                    new_worksheet = new_wb.sheets.add(sheet1)  # 在工作簿中新增工作表并命名为当前的产品名称
                    new_worksheet.range('A1').options(index=False).value = value1  # 将按分组好的数据添加到新增的工作表
            if result_dic_NON:
                for sheet_NON, value_NON in result_dic_NON.items():
                    new_worksheet = new_wb.sheets.add(sheet_NON)  # 在工作簿中新增工作表并命名为当前的产品名称
                    new_worksheet.range('A1').options(index=False).value = value_NON  # 将按分组好的数据添加到新增的工作表

            Activate_worksheet = new_wb.sheets['Sheet1']
            Activate_worksheet.delete()

            new_wb.save(
                f"{os.path.basename(file_path).rsplit('.',1)[0]}-{idx}.{os.path.basename(file_path).rsplit('.',1)[-1]}")
            new_wb.sheets[new_wb.sheets.count-1].delete()
            # delete_sheet.delete()
            new_wb.close()
            new.quit()


def merge_excel_sheets(file_paths: list, header_num, save_name):
    """
    把各文件中Worksheet名相同的表格合并到一个sheet中
    :param file_paths: 给出来源工作簿的文件路径,list
    :param header_num: 表头行数
    :param save_name: 保存路径以及名称
    :return:
    """

    result_dic = {}  # {sheetName:pandas}
    for file_path in file_paths:
        app = xw.App(visible=False, add_book=False)
        workbook = app.books.open(file_path)
        sheet_names = list(reversed([j.name for j in workbook.sheets]))
        for sheet_name in sheet_names:
            worksheet = workbook.sheets[sheet_name]
            # 以DataFrame格式读取要合并的工作表数据
            if worksheet.used_range.address.rsplit("$", 2)[1] == 'A':
                address1 = worksheet.used_range.address.rsplit("$", 2)[0] + 'B' \
                           + worksheet.used_range.address.rsplit("$", 2)[-1]
                value = worksheet.range(address1).options(pd.DataFrame).value  # 读取要拆分的工作表中的所有数据
            else:
                value = worksheet.range(worksheet.used_range).options(pd.DataFrame).value  # 读取要拆分的工作表中的所有数据
            value_header = value.iloc[0:header_num - 1, :]  # 获取表头
            value_data = value.iloc[header_num - 1:value.shape[0], :]  # 获取表格内容

            # 如果工作簿的工作表名不存在，则新增，否则合并替换
            if sheet_name not in result_dic.keys():
                result_dic[sheet_name] = pd.concat([value_header, value_data], join='outer', axis=0)
            else:
                result_dic[sheet_name] = pd.concat([result_dic[sheet_name], value_data], join='outer', axis=0)
        workbook.close()
        app.quit()

    if result_dic:
        new = xw.App(visible=False, add_book=False)
        new_wb = new.books.add()
        for sheetName, value1 in result_dic.items():
            print(sheetName)
            print(value1)
            new_worksheet = new_wb.sheets.add(sheetName)  # 在工作簿中新增工作表并命名为当前的产品名称
            new_worksheet.range('A1').options(index=True).value = value1  # 将按分组好的数据添加到新增的工作表

        Activate_worksheet = new_wb.sheets['Sheet1']
        Activate_worksheet.delete()
        new_wb.save(save_name)
        new_wb.close()
        new.quit()


def merge_excel_sheet(file_paths: list, header_num, save_name):
    """
    把各文件中Worksheet名相同的表格合并到一个sheet中
    :param file_paths: 给出来源工作簿的文件路径,list
    :param header_num: 表头行数
    :param save_name: 保存路径以及名称
    :return:
    """

    result_dic = {}
    for file_path in file_paths:
        app = xw.App(visible=False, add_book=False)
        workbook = app.books.open(file_path)
        sheet_names = [j.name for j in workbook.sheets]
        for sheet_name in sheet_names:
            worksheet = workbook.sheets[sheet_name]
            # 以DataFrame格式读取要合并的工作表数据
            if worksheet.used_range.address.rsplit("$", 2)[1] == 'A':
                address1 = worksheet.used_range.address.rsplit("$", 2)[0] + 'B' \
                           + worksheet.used_range.address.rsplit("$", 2)[-1]
                value = worksheet.range(address1).options(pd.DataFrame).value  # 读取要拆分的工作表中的所有数据
            else:
                value = worksheet.range(worksheet.used_range).options(pd.DataFrame).value  # 读取要拆分的工作表中的所有数据
            value_header = value.iloc[0:header_num - 1, :]  # 获取表头
            value_data = value.iloc[header_num - 1:value.shape[0], :]  # 获取表格内容

            # 如果工作簿的工作表名不存在，则新增，否则合并替换
            if 'merge' not in result_dic.keys():
                result_dic['merge'] = pd.concat([value_header, value_data], join='outer', axis=0)
            else:
                result_dic['merge'] = pd.concat([result_dic['merge'], value_data], join='outer', axis=0)
        workbook.close()
        app.quit()

    if result_dic:
        new = xw.App(visible=False, add_book=False)
        new_wb = new.books.add()
        for sheetName, value1 in result_dic.items():
            print(sheetName)
            print(value1)
            new_worksheet = new_wb.sheets.add(sheetName)  # 在工作簿中新增工作表并命名为当前的产品名称
            new_worksheet.range('A1').options(index=True).value = value1  # 将按分组好的数据添加到新增的工作表

        Activate_worksheet = new_wb.sheets['Sheet1']
        Activate_worksheet.delete()
        new_wb.save(save_name)
        new_wb.close()
        new.quit()


file_path1 = [r'Excel-SAA1-FDD_CM_PLAN_FDD_RADIO_20240227095207-9701.xlsm',r'Excel-SAA1-FDD_CM_PLAN_FDD_RADIO_20240227095207-9702.xlsm']  # 给出来源工作簿的文件路径及工作簿名称

merge_excel_sheet(file_path1, 5, 'heb.xlsm')

#
# header_num = 5
# '''
# 按条件将一个工作表拆分为多个工作表
# '''
# file_path = r'Excel-SAA1-FDD_CM_PLAN_FDD_RADIO_20240227095207.xlsm'  # 给出来源工作簿的文件路径及工作簿名称
# sheet_name = 'ECellEquipmentFunction'  # 给出要拆分的工作表的名称
# app = xw.App(visible=False, add_book=False)
# workbook = app.books.open(file_path)
#
# worksheet = workbook.sheets[sheet_name]
# sheet_names = [j.name for j in workbook.sheets]
# print(sheet_names)
# # 以DataFrame格式读取要拆分的工作表数据
# value = worksheet.range(worksheet.used_range).options(pd.DataFrame).value  # 读取要拆分的工作表中的所有数据
#
# value_header = value.iloc[0:header_num - 1, :]  # 获取表头
# value_data = value.iloc[header_num - 1:value.shape[0], :]  # 获取表格内容
# value_data.to_excel('11.xlsx')
# # 将数据按照“名称”分组
# data = value_data.groupby('SubNetwork')
# print(data)
# for idx, group in data:
#     print(idx)
#     print(group)
#     # 如果工作簿的工作表名不存在，则新增，否则替换
#     if idx not in sheet_names:
#         # 在工作簿中新增工作表并命名为当前的产品名称
#         new_worksheet = workbook.sheets.add(idx)
#         # 将按分组好的数据添加到新增的工作表
#         new_worksheet.range('A1').options(index=False).value = pd.concat([value_header, group], join='outer', axis=0)
#     workbook.sheets[idx].range('A1').options(index=False).value = pd.concat([value_header, group], join='outer', axis=0)
# workbook.save('sss.xlsm')
# workbook.close()
# app.quit()
