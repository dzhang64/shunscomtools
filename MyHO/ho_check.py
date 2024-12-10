import os
import time
import traceback
import warnings

import numpy
import pandas as pd

from OtherFunctions.logdefine import MyLogging

warnings.filterwarnings('ignore')
t = time.strftime("%Y%m%d")
mlogger = MyLogging(file=f"./log.log")


def data_split(df, col, symbol):
    """

    :param df: 数据帧
    :param col: 分裂所在的列名
    :param symbol: 分裂字符“;”,“,”等
    :return:
    """
    split = col + '_split'
    # num = col + '_num'
    df[split] = df[col].apply(lambda x: x.split(symbol))
    # print(df[split])
    # df[num] = df[[split]].apply(lambda z:len(z[split]), axis=1)
    df_split = df.explode(split)
    df_split = df_split.reset_index(drop=True)
    # print(df_split.shape)
    return df_split


def check_ho(icm_workbooks: list, savepath: str):
    # sheet_list = ['EUtranCellMeas', 'UeEUtranMeasurement', 'EUtranCell', 'EUtranReselection', 'CellMeasGroup']
    sheet_col = {'CMG': ["MOI", "closedInterFMeasCfg", "openInterFMeasCfg", "interFHOMeasCfg"],
                 'cell': ['MOI', 'SubNetwork', 'MEID', 'ENBFunction', 'userLabel', 'cellLocalId', 'pci', 'tac',
                          'bandIndicator', 'earfcn', 'bandWidth'],
                 'CM': ["MOI", 'eutranMeasParas_interCarriFreq', "refCellMeasGroup"],
                 'UM': ["MOI", "measCfgIdx", "eventId", "thresholdOfRSRP", "a5Threshold2OfRSRP"],
                 'ReS': ["MOI", "selQrxLevMin", "qrxLevMinOfst", "qhyst", "snonintrasearch", "threshSvrLow",
                         "cellReselectionPriority", "intraQrxLevMin", "eutranRslPara_interReselPrio",
                         "eutranRslPara_interThrdXLow", "eutranRslPara_interThrdXHigh",
                         "eutranRslPara_interQrxLevMin", "eutranRslPara_interCarriFreq",
                         "eutranRslParaExt_interReselPrioExt", "eutranRslParaExt_interThrdXLowExt",
                         "eutranRslParaExt_interThrdXHighExt", "eutranRslParaExt_interQrxLevMinExt",
                         "eutranRslParaExt_interCarriFreqExt"]}

    H = pd.DataFrame()
    R = pd.DataFrame()

    # icm_workbooks = glob.glob(os.path.join(input_path, 'SDR_*.xlsx'))
    # 读取数据
    for i in range(len(icm_workbooks)):
        name = icm_workbooks[i]
        df_CMG1 = pd.DataFrame(columns=sheet_col['CMG'])
        df_cell1 = pd.DataFrame(columns=sheet_col['cell'])
        df_CM1 = pd.DataFrame(columns=sheet_col['CM'])
        df_UM1 = pd.DataFrame(columns=sheet_col['UM'])
        df_ReS1 = pd.DataFrame(columns=sheet_col['ReS'])
        sheet_names = pd.ExcelFile(icm_workbooks[i]).sheet_names
        for j in sheet_names:
            mlogger.info(f'{name}, {j}')
            df_data = pd.read_excel(name, sheet_name=j)
            # print(f'累计耗时{round(float(time.time() - t1), 2)}')
            df_data.drop(labels=[0, 1, 2, 3], inplace=True)
            df_data.fillna('noting', inplace=True)
            if 'EUtranCell' in j and 'EUtranCellMeas' not in j:
                if j.__contains__('FDD'):
                    df_data.rename(
                        columns={'freqBandInd': 'bandIndicator', 'earfcnDl': 'earfcn', 'bandWidthDl': 'bandWidth'},
                        inplace=True)
                if j == 'EUtranCellFDD':
                    df_data.rename(columns={'ENBFunctionFDD': 'ENBFunction'}, inplace=True)
                if j == 'EUtranCellTDD':
                    df_data.rename(columns={'ENBFunctionTDD': 'ENBFunction'}, inplace=True)
                df_cell1 = pd.concat([df_cell1, df_data[sheet_col['cell']]], ignore_index=False, join="outer")
            elif 'CellMeasGroup' in j:
                df_CMG1 = pd.concat([df_CMG1, df_data[sheet_col['CMG']]], ignore_index=False, join="outer")
            elif 'EUtranCellMeas' in j:
                if j.__contains__('LTE'):
                    df_data.rename(columns={'refCellMeasGroupLTE': 'refCellMeasGroup'}, inplace=True)
                if j == 'EUtranCellMeasurementTDD':
                    df_data.rename(columns={'refCellMeasGroupTDD': 'refCellMeasGroup'}, inplace=True)
                df_CM1 = pd.concat([df_CM1, df_data[sheet_col['CM']]], ignore_index=False, join="outer")

            elif 'UeEUtranMeasurement' in j:
                df_UM1 = pd.concat([df_UM1, df_data[sheet_col['UM']]], ignore_index=False, join="outer")

            elif 'EUtranReselection' in j:
                df_ReS1 = pd.concat([df_ReS1, df_data[sheet_col['ReS']]], ignore_index=False, join="outer")

        mlogger.info('读取数据完成')
        try:
            df_UM1['ENB'] = df_UM1['MOI'].apply(lambda x: x.split(',')[2].split('=')[1])
            df_UM1['辅助'] = df_UM1['ENB'] + df_UM1['measCfgIdx']

            df = df_CM1.merge(df_CMG1, left_on='refCellMeasGroup', right_on='MOI', how='left', suffixes=('', '_y'))
            df['num'] = df['eutranMeasParas_interCarriFreq'].apply(lambda x: len(x.split(';')))
            df['interFHOMeasCfg'] = df['interFHOMeasCfg'].apply(
                lambda x: x.split(';') if len(x.split(';')) == 16
                else x.split(';') + [f'NULL{y}' for y in range(16 - len(x.split(';')))])
            df['interFHOMeasCfg'] = [df['interFHOMeasCfg'][x][:df['num'][x]] for x in
                                     range(len(df['eutranMeasParas_interCarriFreq']))]
            df['interFHOMeasCfg'] = df['interFHOMeasCfg'].apply(lambda x: ';'.join(x))

            df_pd = data_split(df, col='eutranMeasParas_interCarriFreq', symbol=';')
            # df_pd.to_excel('df_pd.xlsx')
            df_CMG = data_split(df, col='interFHOMeasCfg', symbol=';')
            # df_CMG.to_excel('df_CMG.xlsx')
            df_pd['measCfgIdx'] = df_CMG['interFHOMeasCfg_split']

            df_pd['ENB'] = df_pd['MOI'].apply(lambda x: x.split(',')[2].split('=')[1])
            df_pd['A1'] = df_pd['closedInterFMeasCfg'].apply(lambda x: x.split(';')[0])
            df_pd['A2'] = df_pd['openInterFMeasCfg'].apply(lambda x: x.split(';')[0])

            df_pd['辅助'] = df_pd['ENB'] + df_pd['A1']
            df_pd = df_pd.merge(df_UM1[['辅助', 'thresholdOfRSRP']], on='辅助', how='left')
            df_pd.rename(columns={'thresholdOfRSRP': 'A1门限'}, inplace=True)
            df_pd['辅助'] = df_pd['ENB'] + df_pd['A2']
            df_pd = df_pd.merge(df_UM1[['辅助', 'thresholdOfRSRP']], on='辅助', how='left')
            df_pd.rename(columns={'thresholdOfRSRP': 'A2门限'}, inplace=True)

            df_pd['辅助'] = df_pd['ENB'] + df_pd['measCfgIdx']
            df_pd = df_pd.merge(df_UM1[['辅助', 'eventId', 'thresholdOfRSRP', 'a5Threshold2OfRSRP']], on='辅助',
                                how='left')
            df_pd.rename(columns={'thresholdOfRSRP': 'A4/A5门限1'}, inplace=True)
            df_pd['eventId'] = df_pd['eventId'].apply(lambda x: x if x is numpy.NaN else 'A' + str(int(x) + 1))
            df_pd['MOI'] = df_pd['MOI'].apply((lambda x: x.rsplit(',EUtranCellMeas')[0]))
            HO = df_cell1.merge(df_pd[['MOI', 'refCellMeasGroup', 'eutranMeasParas_interCarriFreq_split', 'measCfgIdx',
                                       'eventId', 'A4/A5门限1', 'a5Threshold2OfRSRP', 'A1', 'A2', 'A1门限', 'A2门限']],
                                on='MOI', how='left')
            H = pd.concat([H, HO], join='outer', axis=0)
            mlogger.info(f'{name}切换完成')
            # 重选
            df_ReS2 = data_split(df_ReS1, col='eutranRslPara_interCarriFreq', symbol=';')
            df_ReS2['eutranRslPara_interCarriFreq'] = df_ReS2['eutranRslPara_interCarriFreq_split']

            df_ReS = data_split(df_ReS1, col='eutranRslPara_interQrxLevMin', symbol=';')
            df_ReS2['eutranRslPara_interQrxLevMin'] = df_ReS['eutranRslPara_interQrxLevMin_split']
            df_ReS = data_split(df_ReS1, col='eutranRslPara_interReselPrio', symbol=';')
            df_ReS2['eutranRslPara_interReselPrio'] = df_ReS['eutranRslPara_interReselPrio_split']
            df_ReS = data_split(df_ReS1, col='eutranRslPara_interThrdXLow', symbol=';')
            df_ReS2['eutranRslPara_interThrdXLow'] = df_ReS['eutranRslPara_interThrdXLow_split']
            df_ReS = data_split(df_ReS1, col='eutranRslPara_interThrdXHigh', symbol=';')
            df_ReS2['eutranRslPara_interThrdXHigh'] = df_ReS['eutranRslPara_interThrdXHigh_split']
            df_ReS_z = df_ReS2[["MOI", "selQrxLevMin", "qrxLevMinOfst", "qhyst", "snonintrasearch", "threshSvrLow",
                                "cellReselectionPriority", "intraQrxLevMin", "eutranRslPara_interReselPrio",
                                "eutranRslPara_interThrdXLow", "eutranRslPara_interThrdXHigh",
                                "eutranRslPara_interQrxLevMin", "eutranRslPara_interCarriFreq"]]

            df_ReS_ext = df_ReS1[["MOI", "selQrxLevMin", "qrxLevMinOfst", "qhyst", "snonintrasearch", "threshSvrLow",
                                  "cellReselectionPriority", "intraQrxLevMin", "eutranRslParaExt_interReselPrioExt",
                                  "eutranRslParaExt_interThrdXLowExt", "eutranRslParaExt_interThrdXHighExt",
                                  "eutranRslParaExt_interQrxLevMinExt", "eutranRslParaExt_interCarriFreqExt"]]
            df_ReS_ext.dropna(axis=0, subset=['eutranRslParaExt_interCarriFreqExt'], inplace=True)
            for col in df_ReS_ext.columns:
                if col.__contains__('Ext'):
                    a = col.replace('Ext', '')
                    df_ReS_ext.rename(columns={col: a}, inplace=True)

            df_ReS2 = data_split(df_ReS_ext, col='eutranRslPara_interCarriFreq', symbol=';')
            df_ReS2['eutranRslPara_interCarriFreq'] = df_ReS2['eutranRslPara_interCarriFreq_split']

            df_ReS = data_split(df_ReS_ext, col='eutranRslPara_interQrxLevMin', symbol=';')
            df_ReS2['eutranRslPara_interQrxLevMin'] = df_ReS['eutranRslPara_interQrxLevMin_split']
            df_ReS = data_split(df_ReS_ext, col='eutranRslPara_interReselPrio', symbol=';')
            df_ReS2['eutranRslPara_interReselPrio'] = df_ReS['eutranRslPara_interReselPrio_split']
            df_ReS = data_split(df_ReS_ext, col='eutranRslPara_interThrdXLow', symbol=';')
            df_ReS2['eutranRslPara_interThrdXLow'] = df_ReS['eutranRslPara_interThrdXLow_split']
            df_ReS = data_split(df_ReS_ext, col='eutranRslPara_interThrdXHigh', symbol=';')
            df_ReS2['eutranRslPara_interThrdXHigh'] = df_ReS['eutranRslPara_interThrdXHigh_split']
            del df_ReS2['eutranRslPara_interCarriFreq_split']

            df_ReS_z = pd.concat([df_ReS_z, df_ReS2], join='outer', axis=0)
            df_ReS_z['MOI'] = df_ReS_z['MOI'].apply(lambda x: x.rsplit(',EUtranReselection')[0])
            RES = df_cell1.merge(df_ReS_z, on='MOI', how='left')
            R = pd.concat([R, RES], join='outer', axis=0)
            mlogger.info(f'{name}重选完成')
        except Exception as e:
            mlogger.info(f'报错：{e}\n{traceback.format_exc()}')
            return f'fail:{e}'

    H.to_csv(os.path.join(savepath, f'切换_{t}.csv'), index=False, encoding='gbk')
    R1 = R[~(R['eutranRslPara_interCarriFreq'] == 'noting')]
    R1.to_csv(os.path.join(savepath, f'重选_{t}.csv'), index=False, encoding='gbk')
    mlogger.info(f'suss')
    return 'suss'


if __name__ == '__main__':
    check_ho([r'E:\p_py\互操作核查\source\SDR_tdd_radio_20240108165942.xlsx'], r'E:\p_py\互操作核查\source')
