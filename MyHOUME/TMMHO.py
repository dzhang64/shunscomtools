import glob
import os
import traceback
import pandas as pd
import time
import warnings
import numpy
from OtherFunctions.logdefine import MyLogging

input_path = r".\source"
warnings.filterwarnings('ignore')
t = time.strftime("%Y%m%d")
# icm_workbooks = glob.glob(os.path.join(input_path, 'RANCM*.xlsx'))
mlogger = MyLogging(file=f"./log.log")


def ho_tmm(icm_workbooks, savepath):
    try:
        if icm_workbooks:
            sheet_list = ['EUtranCellMeas', 'UeEUtranMeasurement', 'EUtranCell', 'EUtranReselection', 'CellMeasGroup']
            sheet_col = {'CMG': ["ldn", "closedInterFMeasCfg", "openInterFMeasCfg", "interFHOMeasCfg"],
                         'cell': ['ldn', 'SubNetwork', 'ManagedElement', 'ENBFunction', 'userLabel', 'cellLocalId',
                                  'pci', 'tac',
                                  'bandIndicator', 'earfcn', 'bandWidth'],
                         'pd': ['ldn', 'eutranFreqMeaCfgIndex', 'interCarriFreq'],
                         'CM': ['ldn', "refCellMeasGroup"],
                         'UM': ["ldn", "measCfgIdx", "eventId", "thresholdOfRSRP", "a5Threshold2OfRSRP"],
                         'ReS': ["ldn", "selQrxLevMin", "qrxLevMinOfst", "qhyst", "snonintrasearch", "threshSvrLow",
                                 "cellReselectionPriority", "intraQrxLevMin", ],
                         'ReSpd': ['ldn', "interReselPrio", "interThrdXLow", "interThrdXHigh", "interQrxLevMin",
                                   "interCarriFreq"]}

            H = pd.DataFrame()
            R = pd.DataFrame()

            def data_split(df, col, symbol):
                """
                :param df: 数据帧
                :param col: 分裂所在的列名
                :param symbol: 分裂字符“;”,“,”等
                :return:
                """
                split = col + '_split'
                num = col + '_num'
                df[split] = df[col].apply(lambda x: x.split(symbol))
                # print(df[split])
                # df[num] = df[[split]].apply(lambda z:len(z[split]), axis=1)
                df_split = df.explode(split)
                df_split = df_split.reset_index(drop=True)
                # print(df_split.shape)
                return df_split

            # icm_workbooks = glob.glob(os.path.join(input_path, 'RANCM*.xlsx'))
            # 读取数据
            t1 = time.time()
            for i in range(len(icm_workbooks)):
                name = icm_workbooks[i]
                df_CMG1 = pd.DataFrame(columns=sheet_col['CMG'])
                df_cell1 = pd.DataFrame(columns=sheet_col['cell'])
                df_CM1 = pd.DataFrame(columns=sheet_col['CM'])
                df_pd1 = pd.DataFrame(columns=sheet_col['pd'])
                df_UM1 = pd.DataFrame(columns=sheet_col['UM'])
                df_ReS1 = pd.DataFrame(columns=sheet_col['ReS'])
                df_ReS_pd1 = pd.DataFrame(columns=sheet_col['ReSpd'])
                sheet_names = pd.ExcelFile(icm_workbooks[i]).sheet_names
                for j in sheet_names:
                    mlogger.info(f'{name}, {j}')
                    mlogger.info(f'累计耗时{round(float(time.time() - t1), 2)}')
                    if 'EUtranCell' in j and 'EUtranCellMeas' not in j:
                        df_data = pd.read_excel(name, sheet_name=j, skiprows=[1, 2, 3, 4]).fillna('noting')
                        if j.__contains__('FDD'):
                            df_data.rename(
                                columns={'freqBandInd': 'bandIndicator', 'earfcnDl': 'earfcn',
                                         'magicRadioMaxBandWidth': 'bandWidth'},
                                inplace=True)
                        df_data['ENBFunction'] = df_data['ldn'].apply(
                            lambda x: x.split(',')[0].replace('ENBCUCPFunction=', ''))
                        df_cell1 = pd.concat([df_cell1, df_data[sheet_col['cell']]], ignore_index=False, join="outer")
                    elif 'CellMeasGroup' in j:
                        df_data = pd.read_excel(name, sheet_name=j, skiprows=[1, 2, 3, 4]).fillna('noting')
                        df_CMG1 = pd.concat([df_CMG1, df_data[sheet_col['CMG']]], ignore_index=False, join="outer")
                    elif 'EUtranCellMeas' in j:
                        df_data = pd.read_excel(name, sheet_name=j, skiprows=[1, 2, 3, 4]).fillna('noting')
                        if j.__contains__('LTE'):
                            df_data.rename(columns={'refCellMeasGroupLTE': 'refCellMeasGroup'}, inplace=True)
                        if j == 'EUtranCellMeasurementTDD':
                            df_data.rename(columns={'refCellMeasGroupTDD': 'refCellMeasGroup'}, inplace=True)
                        df_CM1 = pd.concat([df_CM1, df_data[sheet_col['CM']]], ignore_index=False, join="outer")
                    elif j.startswith('EUtranMeas'):
                        df_data = pd.read_excel(name, sheet_name=j, skiprows=[1, 2, 3, 4]).fillna('noting')
                        df_data['ldn'] = df_data['ldn'].apply(lambda x: x.rsplit(',', 1)[0])
                        df_pd1 = pd.concat([df_pd1, df_data[sheet_col['pd']]], ignore_index=False, join="outer")
                    elif 'UeEUtranMeasurement' in j:
                        df_data = pd.read_excel(name, sheet_name=j, skiprows=[1, 2, 3, 4]).fillna('noting')
                        df_UM1 = pd.concat([df_UM1, df_data[sheet_col['UM']]], ignore_index=False, join="outer")
                    elif 'EUtranReselection' in j:
                        df_data = pd.read_excel(name, sheet_name=j, skiprows=[1, 2, 3, 4]).fillna('noting')
                        df_ReS1 = pd.concat([df_ReS1, df_data[sheet_col['ReS']]], ignore_index=False, join="outer")
                    elif 'EUtranRslExt' in j or 'EUtranRslPara' in j:
                        df_data = pd.read_excel(name, sheet_name=j, skiprows=[1, 2, 3, 4]).fillna('noting')
                        if 'EUtranRslExt' in j:
                            for ii in df_data.columns:
                                df_data.rename(columns={ii: ii.replace('Ext', '')}, inplace=True)
                        df_ReS_pd1 = pd.concat([df_ReS_pd1, df_data[sheet_col['ReSpd']]], ignore_index=False,
                                               join="outer")

                mlogger.info('读取数据完成')
                df_UM1['辅助'] = df_UM1['ldn'].apply(lambda x: str(x.split(',')[0].split('=')[1])) + df_UM1[
                    'measCfgIdx'].apply(lambda x: str(x))

                df = df_CM1.merge(df_CMG1, left_on='refCellMeasGroup', right_on='ldn', how='left', suffixes=('', '_y'))
                df = df_pd1.merge(df, on='ldn', how='left')
                # df_num = df['ldn'].value_counts().reset_index()
                # df_num.rename(columns={'index':'ldn','ldn':'num'},inplace=True)
                # df = df.merge(df_num, on='ldn', how='left')
                df['eutranFreqMeaCfgIndex'] = df['eutranFreqMeaCfgIndex'].apply(lambda x: int(x))
                df.sort_values(by=['ldn', 'eutranFreqMeaCfgIndex'], ascending=[True, True], inplace=True)
                num_lst = [0]
                num_inx = 0
                for inx in range(1, len(list(df['ldn']))):
                    if list(df['ldn'])[inx] == list(df['ldn'])[inx - 1]:
                        num_inx += 1
                        num_lst.append(num_inx)
                    else:
                        num_inx = 0
                        num_lst.append(num_inx)
                df['eutranFreqMeaCfgIndex'] = num_lst
                df['interFHOMeasCfg'] = df['interFHOMeasCfg'].apply(
                    lambda x: x.split(';') if len(x.split(';')) == 16
                    else x.split(';') + [f'NULL{y}' for y in range(16 - len(x.split(';')))])

                df['interFHOMeasCfg'] = df.apply(lambda x: x.interFHOMeasCfg[x.eutranFreqMeaCfgIndex], axis=1)
                df['measCfgIdx'] = df['interFHOMeasCfg']
                df['ENB'] = df['ldn'].apply(lambda x: x.split(',')[0].split('=')[1])
                df['A1'] = df['closedInterFMeasCfg'].apply(lambda x: x.split(';')[0])
                df['A2'] = df['openInterFMeasCfg'].apply(lambda x: x.split(';')[0])

                df['辅助'] = df['ENB'] + df['A1']
                df = df.merge(df_UM1[['辅助', 'thresholdOfRSRP']], on='辅助', how='left')
                df.rename(columns={'thresholdOfRSRP': 'A1门限'}, inplace=True)
                df['辅助'] = df['ENB'] + df['A2']
                df = df.merge(df_UM1[['辅助', 'thresholdOfRSRP']], on='辅助', how='left')
                df.rename(columns={'thresholdOfRSRP': 'A2门限'}, inplace=True)

                df['辅助'] = df['ENB'] + df['measCfgIdx']
                df = df.merge(df_UM1[['辅助', 'eventId', 'thresholdOfRSRP', 'a5Threshold2OfRSRP']], on='辅助',
                              how='left')
                df.rename(columns={'thresholdOfRSRP': 'A4/A5门限1'}, inplace=True)
                df['eventId'] = df['eventId'].apply(lambda x: x if x is numpy.NaN else x.split('[')[0])
                df['ldn'] = df['ldn'].apply((lambda x: x.rsplit(',', 1)[0]))
                HO = df_cell1.merge(df[['ldn', 'interCarriFreq', 'refCellMeasGroup', 'A1', 'A2', 'A1门限', 'A2门限',
                                        'measCfgIdx', 'eventId', 'A4/A5门限1', 'a5Threshold2OfRSRP']], on='ldn',
                                    how='left')
                H = pd.concat([H, HO], join='outer', axis=0)
                mlogger.info(f'{name}切换完成')
                # 重选
                df_ReS_pd1['ldn'] = df_ReS_pd1['ldn'].apply(lambda x: x.rsplit(',', 1)[0])
                df_ReS1 = pd.merge(df_ReS1, df_ReS_pd1, on='ldn', how='left')
                df_ReS1['ldn'] = df_ReS1['ldn'].apply(lambda x: x.rsplit(',', 2)[0])
                RES = df_cell1.merge(df_ReS1, on='ldn', how='left')
                R = pd.concat([R, RES], join='outer', axis=0)

                mlogger.info(f'{name}重选完成')
            H.rename(columns={'ldn': 'MOI', 'ManagedElement': 'MEID',
                              'interCarriFreq': 'eutranMeasParas_interCarriFreq_split'}, inplace=True)
            R.rename(columns={'ldn': 'MOI', 'ManagedElement': 'MEID', "interReselPrio": 'eutranRslPara_interReselPrio',
                              "interThrdXLow": 'eutranRslPara_interThrdXLow',
                              "interThrdXHigh": 'eutranRslPara_interThrdXHigh',
                              "interQrxLevMin": 'eutranRslPara_interQrxLevMin',
                              "interCarriFreq": 'eutranRslPara_interCarriFreq'})

            H.to_csv(os.path.join(savepath, f'切换TMM_{t}.csv'), index=False, encoding='gbk')
            R.to_csv(os.path.join(savepath, f'重选TMM_{t}.csv'), index=False, encoding='gbk')
            mlogger.info(f'suss')
            return 'suss'
    except Exception as e:
        print(e, traceback.format_exc())
        mlogger.info(f'{traceback.format_exc()}')
        return 'fail'
