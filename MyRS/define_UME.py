# -*- coding: utf-8 -*-
import math
import os
import time
import traceback

from MyRS.define_func import *
from OtherFunctions.logdefine import MyLogging

t = time.strftime("%Y%m%d")
mlogger = MyLogging(file=f"./log.log")


def rs_ume(ume_workbooks, savepath):
    sheet_list = ['DUEUtranCellTDDLTE', 'DUEUtranCellFDDLTE', 'CUEUtranCellFDDLTE', 'CUEUtranCellTDDLTE',
                  'ECellEquipFuncFDDLTE', 'ECellEquipFuncTDDLTE', 'SectorFunction', 'AauTxRxGroup', 'PrruTxRxGroup',
                  'IrRruTxRxGroup', 'NRSectorCarrier', 'PowerControlDL', 'CPList', 'NRCarrier', 'BpPoolFunction',
                  'ReplaceableUnit', 'RfLink', 'NRCellDU', 'CarrierDL']
    sheet_col = {
        'eq': ['ManagedElement', 'ldn', 'refBpPoolFunction', 'refSectorFunction', 'maxCPTransPwr', 'cpTransPwr',
               'cpSpeRefSigPwr'],
        'cell': ['SubNetwork', 'ManagedElement', 'ldn', 'userLabel', 'cellLocalId', 'pci', 'tac', 'BandInd',
                 'earfcn', 'pb', 'bandWidth'],
        'group': ["ManagedElement", "ldn", "refReplaceableUnit", "usedRxChannel"],
        'Bp': ['ManagedElement', 'ldn', 'refReplaceableUnit'],
        'CULTE': [''], 'sector': ["ManagedElement", "ldn", 'TxRxGroup'],
        'DULTE': ["ManagedElement", "ldn", 'refECellEquip', 'cellLocalId']}
    ducon = ['ManagedElement', 'cellLocalId', 'refNRPhysicalCellDU', 'userLabel']
    ccon = ['ManagedElement', 'ldn', 'nrbandwidth']
    eq_ume = pd.DataFrame(columns=sheet_col['eq'])
    cell_ume = pd.DataFrame(columns=sheet_col['cell'])
    # RRU_ume = pd.DataFrame(columns=sheet_col['RRU'])
    pd.DataFrame(columns=sheet_col['Bp'])
    group_ume = pd.DataFrame(columns=sheet_col['group'])
    sector_ume = pd.DataFrame(columns=sheet_col['sector'])
    DULTE_uem = pd.DataFrame(columns=sheet_col['DULTE'])
    NRSectorCarrier = pd.DataFrame()
    NRCarrier = pd.DataFrame()
    CPList = pd.DataFrame()
    BpPoolFunction = pd.DataFrame()
    ReplaceableUnit = pd.DataFrame()
    PowerControlDL = pd.DataFrame()
    DU = pd.DataFrame(columns=ducon)
    CarrierDL = pd.DataFrame(columns=ccon)

    # input_path = input('输入路径：')
    # input_path = path
    # ume_workbooks = glob.glob(os.path.join(input_path, 'RANCM*.xlsx'))
    for i in range(len(ume_workbooks)):
        try:
            sheet_names = pd.ExcelFile(ume_workbooks[i]).sheet_names

            for j in sheet_names:
                mlogger.info(f"{ume_workbooks[i]}, {j}")
                if j in sheet_list:
                    df_data = pd.read_excel(ume_workbooks[i], sheet_name=j)
                    df_data.drop(labels=[0, 1, 2, 3], inplace=True)
                    if 'TxRxGroup' in j or 'RfLink' in j:
                        if j == 'IrRruTxRxGroup':
                            df_data.rename(columns={'refRxRfLink': 'usedRxChannel'}, inplace=True)
                        elif j == 'RfLink':
                            df_data['refReplaceableUnit'] = df_data['refRfPort'].apply(lambda z: z.split(',RfPort=')[0])
                            df_data['usedRxChannel'] = df_data['ldn']

                        group_ume = pd.concat([group_ume, df_data[sheet_col['group']]],
                                              ignore_index=False, join="outer")

                    elif j == 'SectorFunction':
                        if 'refRxRfLink' in df_data.columns.tolist():
                            df_data1 = df_data[
                                ['ManagedElement', 'ldn', 'refAauTxRxGroup', 'refIrRruTxRxGroup', 'refPrruTxRxGroup',
                                 'refRxRfLink']].fillna(method='bfill', axis=1)
                            df_data1['TxRxGroup'] = df_data1['refAauTxRxGroup']
                            # df_data1.to_excel("refRxRfLink.xlsx")
                        else:
                            df_data1 = df_data[
                                ['ManagedElement', 'ldn', 'refAauTxRxGroup', 'refIrRruTxRxGroup',
                                 'refPrruTxRxGroup']].fillna(
                                method='bfill', axis=1)
                            df_data1['TxRxGroup'] = df_data1['refAauTxRxGroup']
                        sector_ume = pd.concat([sector_ume, df_data1[sheet_col['sector']]], ignore_index=False,
                                               join="outer")
                        # sector_ume.to_excel("sector_ume.xlsx")
                    elif 'ECellEquip' in j:
                        if j == 'ECellEquipFuncTDDLTE':
                            df_data['maxCPTransPwr'] = 'null'
                        eq_ume = pd.concat([eq_ume, df_data[sheet_col['eq']]], ignore_index=False, join='outer')
                    elif 'DUEUtranCell' in j:
                        if j == 'DUEUtranCellTDDLTE':
                            df_data.rename(columns={'refECellEquipFuncTDDLTE': 'refECellEquip'}, inplace=True)
                        elif j == 'DUEUtranCellFDDLTE':
                            df_data.rename(columns={'refECellEquipFuncFDDLTE': 'refECellEquip'}, inplace=True)
                        DULTE_uem = pd.concat([DULTE_uem, df_data[sheet_col['DULTE']]],
                                              ignore_index=False, join='outer')
                    elif 'CUEUtranCell' in j:
                        cucell_col = ['SubNetwork', 'ManagedElement', 'ldn', 'userLabel', 'cellLocalId', 'pci', 'tac',
                                      'bandInd', 'BandInd', 'earfcn', 'pb', 'bandWidth']
                        for x in cucell_col:
                            for y in df_data.columns.tolist():
                                if x in y:
                                    if "Ul" in y or "List" in y or 'Type' in y:
                                        continue
                                    else:
                                        if x == 'bandInd':
                                            x = 'BandInd'
                                        df_data.rename(columns={y: x}, inplace=True)
                                        # print(x, y)
                                else:
                                    continue
                        cell_ume = pd.concat([cell_ume, df_data[sheet_col['cell']]], ignore_index=False, join='outer')

                    elif j == 'NRSectorCarrier':
                        NRSectorCarrier = pd.concat([NRSectorCarrier, df_data], ignore_index=False, join="outer")
                    elif j == 'NRCarrier':
                        NRCarrier = pd.concat([NRCarrier, df_data], ignore_index=False, join="outer")
                    elif j == 'CPList':
                        CPList = pd.concat([CPList, df_data], ignore_index=False, join="outer")
                    elif j == 'BpPoolFunction':
                        BpPoolFunction = pd.concat([BpPoolFunction, df_data], ignore_index=False, join="outer")
                    elif j == 'ReplaceableUnit':
                        ReplaceableUnit = pd.concat([ReplaceableUnit, df_data], ignore_index=False, join="outer")
                    elif j == 'PowerControlDL':
                        PowerControlDL = pd.concat([PowerControlDL, df_data], ignore_index=False, join="outer")
                    elif j == 'NRCellDU':
                        DU = pd.concat([DU, df_data[ducon]], ignore_index=False, join="outer")
                    elif j == 'CarrierDL':
                        CarrierDL = pd.concat([CarrierDL, df_data[ccon]], ignore_index=False, join="outer")
        except Exception as e:
            mlogger.error(f'报错：{e}\n{traceback.format_exc()}')
    try:
        DU['dn'] = DU['ManagedElement'] + DU['refNRPhysicalCellDU']
        DU['CI'] = DU['ManagedElement'] + '-' + DU['cellLocalId']
        CarrierDL['CarrierID'] = CarrierDL['ManagedElement'] + CarrierDL['ldn'].apply(
            lambda z: str(z).split(',CarrierDL')[0])

        # group_ume.to_excel('group_ume.xlsx')
        # sector_ume.to_excel('sector_ume.xlsx')

        eq_ume = pd.merge(eq_ume, sector_ume, how='left', left_on=['ManagedElement', 'refSectorFunction'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        del eq_ume['ldn_y']

        eq_ume = data_split(eq_ume, col='TxRxGroup', symbol=';')
        eq_ume = pd.merge(eq_ume, group_ume, how='left', left_on=['ManagedElement', 'TxRxGroup_split'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        del eq_ume['ldn_y']

        eq_ume = pd.merge(eq_ume, ReplaceableUnit.loc[:, ['ManagedElement', 'ldn', 'moId', 'name']], how='left',
                          left_on=['ManagedElement', 'refReplaceableUnit'], right_on=['ManagedElement', 'ldn'],
                          suffixes=('', '_y'))
        eq_ume.rename(columns={'moId': 'Rack', 'name': 'RRU_type', 'usedRxChannel': 'portNo'}, inplace=True)
        # eq_ume.to_excel('eq_ume.xlsx')
        del eq_ume['ldn_y']

        eq_ume = pd.merge(eq_ume, BpPoolFunction.loc[:, ['ManagedElement', 'ldn', 'refReplaceableUnit']],
                          how='left', left_on=['ManagedElement', 'refBpPoolFunction'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        del eq_ume['ldn_y']

        eq_ume = pd.merge(eq_ume, ReplaceableUnit.loc[:, ['ManagedElement', 'ldn', 'slotNo', 'name']], how='left',
                          left_on=['ManagedElement', 'refReplaceableUnit_y'], right_on=['ManagedElement', 'ldn'],
                          suffixes=('', '_y'))
        eq_ume.rename(columns={'refReplaceableUnit_y': 'refReplaceableUnit_Bp', 'name': 'Bp_type'}, inplace=True)
        eq_ume['slotNo'] = eq_ume['slotNo'].astype('str')
        eq_ume['Bp_type'] = eq_ume['Bp_type'].str.cat(eq_ume['slotNo'], sep='-')
        del eq_ume['ldn_y']
        # eq_ume.to_excel('eq_ume.xlsx',index=False)

        cell_ume['ENBFunction'] = cell_ume['ldn'].apply(
            lambda z: str(z.split(',')[0].split('=')[1]).replace('460-00_', ''))
        DULTE_uem = data_split(DULTE_uem, 'refECellEquip', ';')
        DULTE_uem['ENBFunction'] = DULTE_uem['ldn'].apply(
            lambda z: str(z.split(',')[0].split('=')[1]).replace('460-00_', ''))
        DULTE_uem = pd.merge(DULTE_uem, cell_ume, how='left', on=['ManagedElement', 'ENBFunction', 'cellLocalId'],
                             suffixes=('', '_y'))
        # print(DULTE_uem.columns)
        # del DULTE_uem['ManagedElement_y','ldn_y']
        DULTE_uem = pd.merge(DULTE_uem, eq_ume, how='left', left_on=['ManagedElement', 'refECellEquip_split'],
                             right_on=['ManagedElement', 'ldn'],
                             suffixes=('', '_y'))

        lte = DULTE_uem.rename(
            columns={'ManagedElement': 'MEID', 'refECellEquip_split': 'MOI', 'TxRxGroup': 'refRfDevice',
                     'refBpPoolFunction': 'refBpDevice',
                     'TxRxGroup_split': 'refRfDevice_split'})
        lte = lte[['SubNetwork', 'MEID', 'ENBFunction', 'userLabel', 'cellLocalId', 'refECellEquip', 'pci', 'tac',
                   'BandInd', 'earfcn', 'pb', 'bandWidth', 'MOI', 'refRfDevice', 'refBpDevice', 'maxCPTransPwr',
                   'cpTransPwr', 'cpSpeRefSigPwr', 'refRfDevice_split', 'RRU_type', 'portNo', 'Rack', 'Bp_type']]
        del lte['refRfDevice_split']
        del lte['portNo']
        lte = lte.drop_duplicates()
        lte['RRU'] = lte['MEID'] + lte['Rack']
        lte['4G功率W'] = lte['cpTransPwr'].apply(lambda z: math.pow(10, float(z) / 10) / 1000)
        lte.to_excel(os.path.join(savepath, '功率_MIMO.xlsx'), index=False)
        lte_tj = lte.groupby('RRU', as_index=False)['4G功率W'].agg(['count', 'sum'])

        CPList = pd.merge(CPList, NRCarrier.loc[:, ['ManagedElement', 'ldn', 'refNRSectorCarrier']], how='left',
                          left_on=['ManagedElement', 'refNRCarrier'], right_on=['ManagedElement', 'ldn'],
                          suffixes=('', '_y'))
        del CPList['ldn_y']

        CPList = pd.merge(CPList, NRSectorCarrier.loc[:, ['ManagedElement', 'ldn', 'configuredMaxTxPower',
                                                          'maximumTransmissionPower', 'refSectorFunction',
                                                          'refBpPoolFunction']],
                          how='left', left_on=['ManagedElement', 'refNRSectorCarrier'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_NRSectorCarrier'))

        CPList = pd.merge(CPList, sector_ume, how='left', left_on=['ManagedElement', 'refSectorFunction'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        del CPList['ldn_y']

        CPList = data_split(CPList, col='TxRxGroup', symbol=';')
        CPList = pd.merge(CPList, group_ume, how='left', left_on=['ManagedElement', 'TxRxGroup_split'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        del CPList['ldn_y']

        CPList = pd.merge(CPList, ReplaceableUnit.loc[:, ['ManagedElement', 'ldn', 'moId', 'name']],
                          how='left', left_on=['ManagedElement', 'refReplaceableUnit'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        CPList.rename(columns={'moId_y': 'Rack', 'name': 'RRU_type', 'usedRxChannel': 'portNo'}, inplace=True)
        del CPList['ldn_y']

        CPList = pd.merge(CPList, BpPoolFunction.loc[:, ['ManagedElement', 'ldn', 'refReplaceableUnit']],
                          how='left', left_on=['ManagedElement', 'refBpPoolFunction'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        del CPList['ldn_y']

        CPList = pd.merge(CPList, ReplaceableUnit.loc[:, ['ManagedElement', 'ldn', 'slotNo', 'name']],
                          how='left', left_on=['ManagedElement', 'refReplaceableUnit_y'],
                          right_on=['ManagedElement', 'ldn'], suffixes=('', '_y'))
        CPList.rename(columns={'refReplaceableUnit_y': 'refReplaceableUnit_Bp', 'name': 'Bp_type'}, inplace=True)
        CPList['slotNo'] = CPList['slotNo'].astype('str')
        CPList['Bp_type'] = CPList['Bp_type'].str.cat(CPList['slotNo'], sep='-')
        del CPList['ldn_y']
        PowerControlDL['ManagedElement'] = PowerControlDL['ManagedElement'].astype('str')
        PowerControlDL['dn'] = PowerControlDL['ldn'].apply(lambda z: z.split(',PowerControlDL')[0])
        PowerControlDL['dn'] = PowerControlDL['ManagedElement'].str.cat(PowerControlDL['dn'])

        CPList['ManagedElement'] = CPList['ManagedElement'].astype('str')
        CPList['dn'] = CPList['ldn'].apply(lambda z: z.split(',CPList')[0])
        CPList['dn'] = CPList['ManagedElement'].str.cat(CPList['dn'])
        CPList = pd.merge(CPList, PowerControlDL.loc[:, ['dn', 'sssOffsetRE']], how='left', on='dn')
        CPList.to_excel(os.path.join(savepath, '功率_NR.xlsx'), index=False)

        CPList['RRU'] = CPList['ManagedElement'] + CPList['Rack']
        CPList = pd.merge(CPList, lte_tj, on='RRU', how='left').fillna(0)
        ed = pd.read_excel(os.path.join(os.path.abspath(r'./config/MyRS/额定功率.xlsx')))
        CPList = pd.merge(CPList, ed.loc[:, ['RRU_type', '额定功率', '类型']], on='RRU_type', how='left').fillna(
            'null')
        CPList['分类'] = CPList['类型'] + CPList['额定功率'].apply(lambda z: str(z).split('.')[0]) + '-' + CPList[
            'count'].apply(lambda z: str(z).split('.')[0])
        bz = pd.read_excel(os.path.join(os.path.abspath(r'./config/MyRS/标准.xlsx')))
        CPList = pd.merge(CPList, bz.loc[:, ['分类', '5G功率合规最低值']], on='分类', how='left').fillna(0)
        CPList['5G功率W'] = CPList['maximumTransmissionPower'].apply(lambda z: math.pow(10, float(z) / 100) / 1000)
        CPList['差值5-标准'] = CPList['5G功率W'] - CPList['5G功率合规最低值']
        CPList['备注'] = CPList['差值5-标准'].apply(lambda z: '合规' if z >= 0 else '不合规')
        CPList['CarrierID'] = CPList['ManagedElement'] + CPList['refNRCarrier']
        CPList = pd.merge(CPList, DU.loc[:, ['dn', 'CI', 'userLabel']], on='dn', how='left')
        CPList = pd.merge(CPList, CarrierDL.loc[:, ['CarrierID', 'nrbandwidth']], on='CarrierID', how='left')
        CPList.to_excel(os.path.join(savepath, '功率_NR_统计.xlsx'), index=False)
        mlogger.info(f"suss")
        return 'suss'
    except Exception as e:
        mlogger.error(f'报错：{e}\n{traceback.format_exc()}')
        return f'fail:{e}'