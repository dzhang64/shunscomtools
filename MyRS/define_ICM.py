# -*- coding: utf-8 -*-
import os
import time
import traceback

from MyRS.define_func import *
from OtherFunctions.logdefine import MyLogging

t = time.strftime("%Y%m%d")
mlogger = MyLogging(file=f"./log.log")


def rs_icm(icm_workbooks: list, savepath):
    # start = time.monotonic()
    # input_path=input('输入路径:')
    # input_path = path
    # t = time.strftime("%m%d")

    sheet_list = ['ECellEquipmentFunction', 'ECellEquipmentFunctionTDD', 'ECellEquipFuncFDDLTE', 'ECellEquipFuncTDDLTE',
                  'EUtranCellFDD', 'EUtranCellTDD', 'EUtranCellFDDLTE',
                  'EUtranCellTDDLTE', 'RfDevice', 'BpDevice', 'GCellEquipmentFunction', 'GCell',
                  'ECellEquipmentFunctionNB',
                  'CarrierNB']
    sheet_col = {
        'eq': ['MOI', 'refRfDevice', 'refBpDevice', 'maxCPTransPwr', 'cpTransPwr', 'cpSpeRefSigPwr', 'antMapDlSeq'],
        'cell': ['SubNetwork', 'MEID', 'ENBFunction', 'userLabel', 'cellLocalId', 'refECellEquip', 'pci', 'tac',
                 'BandInd', 'earfcn', 'pb', 'bandWidth', 'cellRSPortNum'],
        'RRU': ["refRfDevice_split", "Rack", "portNo", "RRU_type"], 'Bp': ['refBpDevice', 'Bp_type'],
        'gsm_eq': ['MOI', 'gCellEquipmentFuncNo', 'refTxChannel', 'gsmCarrierConfig_carrierPower'],
        'GCell': ['MOI', 'gcellConfig_gCellEquipmentFuncNo'],
        'NB': ['MOI', 'refECellEquipmentFunctionNB'],
        'NB_eq': ['refECellEquipmentFunctionNB_split', 'refRfDevice', 'cpTransPwr']}
    df_eq1 = pd.DataFrame(columns=sheet_col['eq'])
    df_cell1 = pd.DataFrame(columns=sheet_col['cell'])
    df_RRU1 = pd.DataFrame(columns=sheet_col['RRU'])
    df_Bp1 = pd.DataFrame(columns=sheet_col['Bp'])
    pd.DataFrame(columns=sheet_col['gsm_eq'])
    pd.DataFrame(columns=sheet_col['GCell'])
    df_gsm_eq = pd.DataFrame(columns=sheet_col['gsm_eq'])
    df_GCell = pd.DataFrame(columns=sheet_col['GCell'])
    df_NB = pd.DataFrame(columns=sheet_col['NB'])
    df_NB_eq = pd.DataFrame(columns=sheet_col['NB_eq'])

    # icm_workbooks = glob.glob(os.path.join(input_path, 'SDR_*.xlsx'))
    for i in range(len(icm_workbooks)):
        sheet_names = pd.ExcelFile(icm_workbooks[i]).sheet_names
        mlogger.info(f'{icm_workbooks[i]}, {sheet_names}')
        for j in sheet_names:
            if j in sheet_list:
                df_data = pd.read_excel(icm_workbooks[i], sheet_name=j)
                df_data.drop(labels=[0, 1, 2, 3], inplace=True)
                if 'ECellEquip' in j:
                    if 'NB' in j:
                        df_data.rename(columns={'MOI': 'refECellEquipmentFunctionNB_split'}, inplace=True)
                        df_NB_eq = pd.concat([df_NB_eq, df_data[sheet_col['NB_eq']]], ignore_index=False, join='outer')
                    else:
                        if 'TDD' in j:
                            df_data.rename(columns={'upActAntBitmapSeq': 'antMapDlSeq'}, inplace=True)
                        df_eq1 = pd.concat([df_eq1, df_data[sheet_col['eq']]], ignore_index=False, join="outer")

                elif 'EUtranCell' in j:
                    cell_col = ['SubNetwork', 'MEID', 'ENBFunction', 'userLabel', 'cellLocalId', 'refECellEquip', 'pci',
                                'tac', 'bandInd', 'BandInd', 'earfcn', 'pb', 'bandWidth']
                    # df_cell1 = pd.DataFrame(columns=sheet_col['cell'])
                    for x in cell_col:
                        for y in df_data.columns.tolist():
                            if x in y:
                                if "Ul" in y or "List" in y:
                                    continue
                                else:
                                    if x == 'bandInd':
                                        x = 'BandInd'
                                    df_data.rename(columns={y: x}, inplace=True)
                                    # print(x, y)
                            else:
                                continue
                    df_cell1 = pd.concat([df_cell1, df_data[sheet_col['cell']]], ignore_index=False, join='outer')
                elif j == 'RfDevice':
                    # df_RRU1 = pd.DataFrame(columns=sheet_col['RRU'])
                    df_data.rename(columns={"MOI": "refRfDevice_split", 'description': 'RRU_type'}, inplace=True)
                    df_data['RRU_type'] = df_data['RRU_type'].apply(lambda z: str_replace(z, ')('))
                    df_data['RRU_type'] = df_data['RRU_type'].apply(lambda z: str(z).split(',')[0])
                    df_RRU1 = pd.concat([df_RRU1, df_data[sheet_col['RRU']]], ignore_index=False, join='outer')
                elif j == 'BpDevice':
                    # df_Bp1 = pd.DataFrame(columns=sheet_col['Bp'])
                    df_data.rename(columns={"MOI": "refBpDevice", 'description': 'Bp_type'}, inplace=True)
                    df_Bp1 = pd.concat([df_Bp1, df_data[sheet_col['Bp']]], ignore_index=False, join='outer')
                elif j == 'GCellEquipmentFunction':
                    df_gsm_eq = pd.concat([df_gsm_eq, df_data[sheet_col['gsm_eq']]], ignore_index=False, join='outer')
                elif j == 'GCell':
                    df_GCell = pd.concat([df_GCell, df_data[sheet_col['GCell']]], ignore_index=False, join='outer')
                elif j == 'ECellEquipmentFunctionNB':
                    df_data.rename(columns={'MOI': 'refECellEquipmentFunctionNB_split'}, inplce=True)
                    print(df_data.head(4))
                    df_NB_eq = pd.concat([df_NB_eq, df_data[sheet_col['NB_eq']]], ignore_index=False, join='outer')
                elif j == 'CarrierNB':
                    df_NB = pd.concat([df_NB, df_data[sheet_col['NB']]], ignore_index=False, join='outer')
                    # df_NB.to_excel('nb2.xlsx')
            else:
                continue

    try:
        # GSM 使用通道
        df_GCell = data_split(df_GCell, col='gcellConfig_gCellEquipmentFuncNo', symbol=';')
        df_gsm_eq['MOI'] = df_gsm_eq['MOI'].apply(lambda xx: xx.split(',GCell')[0]) + df_gsm_eq[
            'gCellEquipmentFuncNo'].apply(
            lambda yy: ',No=' + str(yy))
        df_GCell['MOI'] = df_GCell['MOI'].apply(lambda yy: yy.split(',GCell')[0]) + df_GCell[
            'gcellConfig_gCellEquipmentFuncNo_split'].apply(lambda yy: ',No=' + str(yy))
        df_GCell = df_GCell.merge(df_gsm_eq, on='MOI', how='left')
        df_GCell['2G功率W'] = df_GCell['gsmCarrierConfig_carrierPower'].apply(
            lambda yy: sum([float(yy) for yy in yy.split(';')]))
        df_GCell['refRfDevice_split'] = df_GCell['refTxChannel'].apply(lambda xx: xx.split(',TxChannel=')[0])
        df_gsm = df_GCell[['refRfDevice_split', '2G功率W']]

        # NB使用功率
        df_NB = data_split(df_NB, col='refECellEquipmentFunctionNB', symbol=';')
        df_NB = df_NB.merge(df_NB_eq, on='refECellEquipmentFunctionNB_split', how='left')
        df_NB['W'] = df_NB['cpTransPwr'].apply(lambda xx: 10 ** (float(xx) / 10) / 1000)
        df_NB = data_split(df_NB, col='refRfDevice', symbol=';')
        # df_NB.to_excel('nb2.xlsx')
        df_NB['refRfDevice_split1'] = df_NB['refRfDevice_split'].apply(lambda xx: xx.split('=')[-1])
        df_NB['备注'] = 'Y'
        df_NB.loc[((df_NB['refRfDevice_split1'] == '2') | (df_NB['refRfDevice_split1'] == '3')), '备注'] = 'N'
        df_NB = df_NB.query('备注=="Y"')
        df_num = df_NB.pivot_table(index=['refECellEquipmentFunctionNB_split'], values=['refRfDevice_split1'],
                                   aggfunc='count').reset_index()
        df_NB = df_NB.merge(df_num, on='refECellEquipmentFunctionNB_split', how='left', suffixes=('', '_通道数'))
        df_NB['NB平均单通道W'] = df_NB['W'] / df_NB['refRfDevice_split1_通道数']

        del df_NB['备注']
        df_NB = df_NB[['refRfDevice_split', 'NB平均单通道W']]
        # df_NB.rename(columns={'refRfDevice':'refRfDevice_split'},inplace=True)
        # GSM & NB 合并
        df_gsm = pd.merge(df_gsm, df_NB, on='refRfDevice_split', how='outer')
        df_GB = df_gsm.pivot_table(index=['refRfDevice_split'], values=['2G功率W', 'NB平均单通道W'], aggfunc='max',
                                   fill_value=0).reset_index()
        # df_GB.to_excel('nb1.xlsx')
        # df_gsm.to_excel('all.xlsx')
    except Exception as e:
        mlogger.error(f'报错：{e}\n{traceback.format_exc()}')

    try:
        # ICM网管数据
        df_ep = data_split(df_eq1, col='refRfDevice', symbol=';')
        df_ep = pd.merge(df_ep, df_RRU1, how='left', on='refRfDevice_split')  # RRU通道、端口、型号
        df_ep['发射端口'] = df_ep['antMapDlSeq'].apply(lambda xx: xx.split(';'))
        df_ep['发射端口'] = df_ep['发射端口'].apply(
            lambda xx: [str(int(ii) + 1) for ii in range(len(xx)) if xx[ii] == '1'])
        df_ep['发射端口'] = df_ep['发射端口'].apply(lambda xx: ';'.join(xx))
        df_ep = data_split(df_ep, col='发射端口', symbol=';')
        df_ep['refRfDevice_ID'] = df_ep['refRfDevice_split'].apply(lambda m: str(m).split('=')[-1])
        df_ep['对比结果'] = df_ep[['refRfDevice_ID', '发射端口_split']].apply(
            lambda xx: xx['refRfDevice_ID'] == xx['发射端口_split'], axis=1)
        df_ep = df_ep[df_ep['对比结果'] == 1]

        # df_ep['Rack']=df_ep['Rack'].astype('str')
        # df_ep['MOI_Rack']=df_ep['MOI'].str.cat(df_ep['Rack'])
        # df_ep=data_combine(df_ep,col_group='MOI_Rack',col_combine='portNo',symbol=';',mode=1)#聚类RRU通道
        df_ep['portNo聚类'] = df_ep['portNo']
        df_ep = data_combine(df_ep, col_group='MOI', col_combine='portNo聚类', symbol=';', mode=0)  # 聚类基带资源通道
        # df_ep=data_combine(df_ep,col_group='MOI',col_combine='Rack',symbol=';',mode=1)#聚类RRU,可以判断是否为并柜
        df_ep = pd.merge(df_ep, df_Bp1, how='left', on='refBpDevice')  # 基带板
        # print("基带资源大小{}".format(df_ep.shape))
        # df_ep.to_excel("引用的设备.xlsx",index=False)

        df_cell = data_split(df_cell1, col='refECellEquip', symbol=';')
        df_cell.rename(columns={'refECellEquip_split': 'MOI'}, inplace=True)
        df_re = pd.merge(df_cell, df_ep, how='left', on='MOI')

        if df_NB.shape[0] > 0:
            df_re['频段'] = 'FA'
            df_re.loc[(df_re['BandInd'] == '3'), '频段'] = 'FD'
            df_re.loc[(df_re['BandInd'] == '8'), '频段'] = 'FG'
            df_re.loc[(df_re['BandInd'] == '40'), '频段'] = 'E'
            df_re.loc[(df_re['BandInd'] == '41'), '频段'] = 'D'
            df_re.loc[(df_re['BandInd'] == '38'), '频段'] = 'D'
            df_re['RRU_频段'] = df_re['RRU_type'].apply(lambda xx: xx.split('(')[0]) + df_re['频段'].apply(
                lambda xx: '_' + str(xx))
            bz = pd.read_excel(os.path.join(os.path.abspath(r'./config/MyRS/额定功率.xlsx')), sheet_name='LTE')
            df_re = df_re.merge(df_GB, on='refRfDevice_split', how='left').fillna(0)
            df_re = df_re.merge(bz[['RRU_type', 'RRU_频段', '设备额定单通道功率W', '设备通道数']], on='RRU_频段',
                                how='left')
            df_td = df_re.pivot_table(index=['MOI'], values=['portNo'], aggfunc='count',
                                      fill_value=0).reset_index()  # 计算发射通道数量
            df_re = df_re.merge(df_td, on='MOI', how='left', suffixes=('', '_通道数'))

            df_re['4G平均单通道使用功率W'] = (
                    df_re['cpTransPwr'].apply(lambda xx: 10 ** (float(xx) / 10) / 1000) / df_re['portNo_通道数'].
                    apply(lambda xx: int(xx)))
            df_re['4G可使用单通道功率W'] = df_re['设备额定单通道功率W'] - df_re['2G功率W'] - df_re['NB平均单通道W']

            df_y1 = df_re.pivot_table(index=['refRfDevice_split'], values=['4G平均单通道使用功率W'], aggfunc='sum',
                                      fill_value=0).reset_index()  # 计算4G每个通道使用功率（用通道求和）
            df_re = df_re.merge(df_y1, on='refRfDevice_split', how='left', suffixes=('', '_sum'))
            df_re.rename(columns={'4G平均单通道使用功率W': '每个基带资源下4G单通道使用功率W',
                                  '4G平均单通道使用功率W_sum': '4G单通道使用功率W'}, inplace=True)
            df_y = df_re.pivot_table(index=['MOI'],
                                     aggfunc={'4G可使用单通道功率W': 'min', '4G单通道使用功率W': 'max'},
                                     fill_value=0).reset_index()
            # 计算4G每个基带资源可以使用功率（通道最小值）和使用功率（最大值）（用基带资源对单通道求min\max）

            df_re = df_re.merge(df_y, on='MOI', how='left', suffixes=('', '_sum'))
            df_re.rename(columns={'4G可使用单通道功率W_sum': '每个基带资源4G可使用功率W',
                                  '4G单通道使用功率W_sum': '每个基带资源4G使用功率W'}, inplace=True)
            df_re['每个基带资源4G可使用功率W'] = df_re['每个基带资源4G可使用功率W'] * df_re['portNo_通道数']
            df_re['每个基带资源4G使用功率W'] = df_re['每个基带资源4G使用功率W'] * df_re['portNo_通道数']
            # var = ["R8881 S1800", "R8852E S1800", "R8862A S1800", "R8881 S9000", "R8852E S9000", "R8862A S9000"]

            df_re['可提升功率余量W'] = df_re['每个基带资源4G可使用功率W'] - df_re['每个基带资源4G使用功率W']
            df_re.drop(columns=['对比结果', '发射端口_split', 'refRfDevice_ID', '频段'], inplace=True)
            fname = '功率_LTEICM_含gsm&NB(小区-通道)' + t + '.xlsx'
            df_re.to_excel(os.path.join(savepath, fname), index=False)

            fname = '功率_LTEICM_含gsm&NB(小区-RRU)' + t + '.xlsx'
            df_re.drop(columns=['refRfDevice_split', 'RRU_type_x', 'portNo', '发射端口'], inplace=True)
            df_re.drop_duplicates(keep='first', inplace=True)
            df_re.to_excel(os.path.join(savepath, fname), index=False)
        else:
            fname = '功率_LTEICM(纯4G)' + t + '.xlsx'
            df_re.to_excel(os.path.join(savepath, fname), index=False)
        mlogger.info(f"suss")
        return 'suss'
    except Exception as e:
        mlogger.error(f'报错：{e}\n{traceback.format_exc()}')
        return f'fail:{e}'
