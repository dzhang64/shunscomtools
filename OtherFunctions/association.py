import pandas as pd
import os
import zipfile
import warnings
import time

from OtherFunctions.logdefine import MyLogging

warnings.filterwarnings('ignore')
t = time.strftime("%Y%m%d")
mlogger = MyLogging(file=f"./log.log")


class north_cm:
    def __init__(self, path: list, save):
        # self.path = path
        self.save = save
        # self.lst = [os.path.join(self.path, i) for i in os.listdir(self.path)]
        self.lst = path

        self.lteHO = pd.DataFrame()
        self.nr_nr_HO = pd.DataFrame()
        self.lteHO_error = pd.DataFrame()
        self.nrRes = pd.DataFrame()
        self.nrRes_error = pd.DataFrame()
        self.lteRes = pd.DataFrame()
        self.lteRes_error = pd.DataFrame()
        if not os.path.exists(os.path.join(self.save, '互操作')):
            os.mkdir(os.path.join(self.save, '互操作'))
        # if not os.path.exists(os.path.join(self.save, 'TOP')):
        #     os.mkdir(os.path.join(self.save, 'TOP'))

    def hand_cell(self):
        mlogger.info('小区信息整理')
        cell = []
        for csv in self.lst:
            DU = pd.read_excel(csv, sheet_name='NRCellDU', skiprows=[1, 2, 3, 4])[
                ['masterOperatorId', 'refNRPhysicalCellDU']]
            CU = pd.read_excel(csv, sheet_name='NRCellCU', skiprows=[1, 2, 3, 4])[
                ["SubNetwork", "ManagedElement", "NE_Name", "ldn", "moId", "userLabel", "masterOperatorId",
                 "cellLocalId", 'duMeMoId', "plmnIdList"]]
            CU = pd.merge(CU, DU, on='masterOperatorId', how='left', suffixes=('', '_DU'))
            CU['on'] = CU['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + CU['refNRPhysicalCellDU']
            SSB = pd.read_excel(csv, sheet_name='CellDefiningSSB', skiprows=[1, 2, 3, 4])
            SSB['on'] = SSB['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + SSB['ldn'].apply(
                lambda x: x.rsplit(',', 1)[0])
            SSB = SSB[['on', 'ldn', 'pci', 'ssbFrequency']]
            CU = pd.merge(CU, SSB, on='on', how='left', suffixes=('', '_SSB'))
            del CU['on']
            cell.append(CU)
        cell_res = pd.concat(cell, join='outer', ignore_index=True)
        cell_res['l'] = cell_res['plmnIdList'].apply(lambda x: '是' if str(x).__contains__("460-00") else '否')
        cell_res = cell_res[cell_res['l'] == '是']
        del cell_res['l']
        cell_res = cell_res.drop_duplicates()
        return cell_res

    @staticmethod
    def read_zip_csv(path, name):
        with zipfile.ZipFile(path, "r") as zFile:
            zFile.extract(name)
            df = pd.read_csv(name, encoding='utf-8', low_memory=False)
        os.remove(name)
        return df

    @staticmethod
    def panduan(A2, A2_Blind, event, B2_1):
        """
        NR-LTE 切换判断是否合理
        :param A2: 数据A2
        :param A2_Blind: 数据盲A2
        :param event: 事件
        :param B2_1: B2_1门限
        :return:
        """
        if event == 'B1':
            if A2 != 'NULL' and A2_Blind != 'NULL':
                if A2 >= -100 or A2_Blind >= -100:
                    res_str = '不合理：B1事件时A2/忙重定向A2>-100'
                else:
                    res_str = '合理'
            else:
                res_str = '不合理:未配置A2'
        else:
            if B2_1 != 'NULL':
                if A2 != 'NULL' and A2_Blind != 'NULL':
                    if (A2 >= -100 and B2_1 >= -100) or A2_Blind >= -100:
                        res_str = '不合理：B2事件时A2/忙重定向A2>-100或B2_1>-100'
                    else:
                        res_str = '合理'
                else:
                    res_str = '不合理:未配置A2'
            else:
                if A2 != 'NULL' and A2_Blind != 'NULL':
                    if A2 >= -100 or A2_Blind >= -100:
                        res_str = '不合理：B2事件时A2/忙重定向A2>-100或B2_1>-100且未配置切换事件'
                    else:
                        res_str = '不合理:未配置切换事件'
                else:
                    res_str = '不合理:未配置A2'
        return res_str

    def associate(self, path, name):
        remove_ref = ['refQuantityConfigNR']
        mlogger.info(f'{path}-{name}')
        names = pd.ExcelFile(path).sheet_names
        if name in names:
            df = pd.read_excel(path, sheet_name=name, skiprows=[1, 2, 3, 4])
            # df['ldn']= df['ManagedElement'].apply(lambda x:"Ne="+str(x)+",")+df['ldn']
            col_ref = [col[3:] for col in df.columns if col.startswith('ref') and col not in remove_ref]
            if col_ref:
                for col in col_ref:
                    if col in names:
                        try:
                            df['on'] = df['ManagedElement'].apply(lambda x: str(x)) + df['ref' + col]
                        except:
                            df['on'] = df['MEID'].apply(lambda x: str(x)) + df['ref' + col]
                        # df_ref = pd.read_excel(path, sheet_name=col, skiprows=[1, 2, 3, 4])
                        df_ref = self.associate(path, col)
                        try:
                            df_ref['on'] = df_ref['ManagedElement'].apply(lambda x: str(x)) + df_ref['ldn']
                        except:
                            df_ref['on'] = df_ref['MEID'].apply(lambda x: str(x)) + df_ref['MOI']
                        df = df.merge(df_ref, on='on', how='left', suffixes=('', '_' + col))
                        del df['on']
            else:
                return df
            return df
        else:
            mlogger.info(f'{name}没有导出')
            # print(f'{name}没有导出')

    def hand_nr_lte_ho(self, key1=None, key2=None):
        """
        梳理5-4切换（数据）
        :param key1: key1为区分是语音还是数据的对象标识
        :param key2: key2为区分是语音还是数据的A1A2对象标识
        :return:
        """
        res_lst = []
        for csv in self.lst:
            print(csv)
            mlogger.info(f'NR-LTE切换：{csv}')
            res = self.associate(csv, 'CoverMobilityLTEFreqMeasCfg')
            res['CoverMobilityMeasCfg'] = res['ldn'].apply(lambda x: x.split('CoverMobilityMeasCfg=')[-1].split(',')[0])
            res['on'] = (res['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                         res['ldn'].apply(lambda x: x.split(',CoverMobilityCtrl=')[0]))
            if key1:
                res['CoverMobilityMeasCfg'] = res['CoverMobilityMeasCfg'].apply(lambda x: str(x))
                res = res[res['CoverMobilityMeasCfg'] == key1]

            res = res[["on", "ldn", "moId", "refMeasObjEUTRA", "refLTEFreqCovHo", "lteFreqCovHoPrio",
                       "lteFreqBlindRedPrio", "measBandWidth", "refEutranFreqRelation", "rdFreqPriority",
                       "refEutranFreq", "frequency", "freqBand", "moId_LTEFreqCovHo", "eventId",
                       "rsrpThreshold", "b2Thrd1Rsrp", "CoverMobilityMeasCfg"]]
            NRCellCU = self.hand_cell()
            NRCellCU['on'] = NRCellCU['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + NRCellCU['ldn']
            InterRatHoA1A2 = pd.read_excel(csv, sheet_name='InterRatHoA1A2', skiprows=[1, 2, 3, 4])
            InterRatHoA1A2['on'] = (InterRatHoA1A2['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                                    InterRatHoA1A2['ldn'].apply(lambda x: x.split(',CoverMobilityCtrl=')[0]))
            InterRatHoA1A2 = InterRatHoA1A2[
                ["on", "ldn", "moId", "rsrpThresholdA1", "rsrpThresholdA2", "hysteresisA1", "hysteresisA2"]]

            InterRatHoA1A2['moId'] = InterRatHoA1A2['moId'].apply(lambda x: str(x))
            InterRatHoA1A2 = InterRatHoA1A2[InterRatHoA1A2['moId'] == key2]
            NRBlindRd = pd.read_excel(csv, sheet_name='NRBlindRd', skiprows=[1, 2, 3, 4])
            NRBlindRd['on'] = (NRBlindRd['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                               NRBlindRd['ldn'].apply(lambda x: x.split(',CoverMobilityCtrl=')[0]))
            NRBlindRd = NRBlindRd[["on", "ldn", "moId", "rsrpThreshold", "hysteresis"]]

            if key1:
                NRBlindRd['moId'] = NRBlindRd['moId'].apply(lambda x: str(x))
                NRBlindRd = NRBlindRd[NRBlindRd['moId'] == key1]
            # NRCellCU.to_excel('a.xlsx')
            # InterRatHoA1A2.to_excel('b.xlsx')
            NRCellCU = pd.merge(NRCellCU, InterRatHoA1A2, on='on', how='left', suffixes=('', '_InterRatHoA1A2')).fillna(
                'NULL')
            NRCellCU = pd.merge(NRCellCU, NRBlindRd, on='on', how='left', suffixes=('', '_NRBlindRd')).fillna('NULL')
            NRCellCU = pd.merge(NRCellCU, res, on='on', how='left', suffixes=('', '_lteHO')).fillna('NULL')
            del NRCellCU['on']
            res_lst.append(NRCellCU)
        self.lteHO = pd.concat(res_lst, join='outer', ignore_index=True)
        self.lteHO.to_csv(os.path.join(self.save, '互操作/' + f'互操作_NR-LTE切换-{key1}.csv'), index=False, encoding='gbk')
        mlogger.info(f'NR-LTE切换完成')

    def hand_nr_nr_ho(self, key1=None, key2=None):
        """
        梳理5-5切换（数据）
        :param key1: key1为区分是语音还是数据的对象标识
        :param key2: key2为区分是语音还是数据的A1A2对象标识
        :return:
        """
        res_lst = []
        for csv in self.lst:
            print(csv)
            mlogger.info(f'NR-NR切换：{csv}')
            interFHO = ["ManagedElement", "ldn", "refInterFMeasObject", "refNRInterFCovHo", "interFCovHoPrio",
                        "interFBlindRedPrio", "ssbFrequency", "moId_NRInterFCovHo", "eventId", "rsrpThreshold",
                        "A5Thrd1Rsrp"]

            res = self.associate(csv, 'CoverMobilityInterFMeasCfg')
            res['CoverMobilityMeasCfg'] = res['ldn'].apply(lambda x: x.split('CoverMobilityMeasCfg=')[-1].split(',')[0])
            res['on'] = (res['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                         res['ldn'].apply(lambda x: x.split(',CoverMobilityCtrl=')[0]))

            if key1:
                res['CoverMobilityMeasCfg'] = res['CoverMobilityMeasCfg'].apply(lambda x: str(x))
                res = res[res['CoverMobilityMeasCfg'] == key1]

            res = res[["on", "ldn", "moId", "refInterFMeasObject", "refNRInterFCovHo", "interFCovHoPrio",
                       "interFBlindRedPrio", "refNRFreq", "ssbFrequency", "moId_NRInterFCovHo", "eventId",
                       "rsrpThreshold", "A5Thrd1Rsrp", "CoverMobilityMeasCfg"]]

            NRCellCU = self.hand_cell()
            NRCellCU['on'] = NRCellCU['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + NRCellCU['ldn']
            InterRatHoA1A2 = pd.read_excel(csv, sheet_name='InterFHoA1A2', skiprows=[1, 2, 3, 4])
            InterRatHoA1A2['on'] = (InterRatHoA1A2['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                                    InterRatHoA1A2['ldn'].apply(lambda x: x.split(',CoverMobilityCtrl=')[0]))
            InterRatHoA1A2 = InterRatHoA1A2[
                ["on", "ldn", "moId", "rsrpThresholdA1", "rsrpThresholdA2", "hysteresisA1", "hysteresisA2"]]

            InterRatHoA1A2['moId'] = InterRatHoA1A2['moId'].apply(lambda x: str(x))
            InterRatHoA1A2 = InterRatHoA1A2[InterRatHoA1A2['moId'] == key2]
            NRBlindRd = pd.read_excel(csv, sheet_name='NRBlindRd', skiprows=[1, 2, 3, 4])
            NRBlindRd['on'] = (NRBlindRd['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                               NRBlindRd['ldn'].apply(lambda x: x.split(',CoverMobilityCtrl=')[0]))
            NRBlindRd = NRBlindRd[["on", "ldn", "moId", "rsrpThreshold", "hysteresis"]]

            if key1:
                NRBlindRd['moId'] = NRBlindRd['moId'].apply(lambda x: str(x))
                NRBlindRd = NRBlindRd[NRBlindRd['moId'] == key1]
            # NRCellCU.to_excel('a.xlsx')
            # InterRatHoA1A2.to_excel('b.xlsx')
            NRCellCU = pd.merge(NRCellCU, InterRatHoA1A2, on='on', how='left', suffixes=('', '_InterRatHoA1A2')).fillna(
                'NULL')
            NRCellCU = pd.merge(NRCellCU, NRBlindRd, on='on', how='left', suffixes=('', '_NRBlindRd')).fillna('NULL')
            NRCellCU = pd.merge(NRCellCU, res, on='on', how='left', suffixes=('', '_lteHO')).fillna('NULL')
            del NRCellCU['on']
            res_lst.append(NRCellCU)
        self.nr_nr_HO = pd.concat(res_lst, join='outer', ignore_index=True)
        self.nr_nr_HO.to_csv(os.path.join(self.save, '互操作/' + f'互操作_NR-NR切换-{key1}.csv'), index=False, encoding='gbk')
        mlogger.info(f'NR-NR切换完成')
    """    def nr_lte_ho_analyse(self):
            self.hand_lte_ho()
            self.lteHO['备注'] = self.lteHO.apply(lambda x: self.panduan(x['A2事件判决的RSRP绝对门限'],
                                                                       x['A2事件判决的RSRP绝对门限_NRBlindRd'],
                                                                       x['事件标识'],
                                                                       x['B2事件服务小区判决的RSRP绝对门限']), axis=1)
            # print(self.lteHO['备注'])
            self.lteHO_error = self.lteHO[self.lteHO['备注'] != '合理']
            self.lteHO_error.to_excel(os.path.join(self.save, 'TOP/' + 'NR_LTE切换不合理明细.xlsx'), index=False)"""

    def hand_nr_nr_res(self):
        """
        异频重选
        :return:
        """
        res_lst = []
        for csv in self.lst:
            mlogger.info(f'NR-NR重选{csv}')
            res = self.associate(csv, 'InterFReselection')
            InterFReselection = ["ManagedElement", "ldn", "refNRFreqRelation", "qRxLevMin", "threshXHighP",
                                 "threshXLowP",
                                 "cellReselectionPriority", "cellReselectionSubPriority", "refNRFreq", "ssbFrequency"]
            res = res[InterFReselection]
            res['ldn'] = (res['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                          res['ldn'].apply(lambda x: x.split(',CellResel=')[0]))
            NRCellCU = self.hand_cell()
            NRCellCU['ldn'] = NRCellCU['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + NRCellCU['ldn']
            Resel = pd.read_excel(csv, sheet_name='CellResel', skiprows=[1, 2, 3, 4])
            Resel['ldn'] = Resel['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + Resel['ldn']
            Resel['ldn'] = Resel['ldn'].apply(lambda x: x.split(',CellResel=')[0])
            CellResel = ["ldn", "qHyst", "threshServingLowP", "cellReselectionPriority", "sNonIntraSearchSwitch",
                         "sNonIntraSearchP", "cellReselectionSubPriority"]
            Resel = Resel[CellResel]
            NRCellCU = pd.merge(NRCellCU, Resel, on='ldn', suffixes=('', '_CellResel'))
            NRCellCU = pd.merge(NRCellCU, res, on='ldn', suffixes=('', '_InterFReselection'))
            # del NRCellCU['on']
            res_lst.append(NRCellCU)
        self.nrRes = pd.concat(res_lst, join='outer', ignore_index=True)
        self.nrRes.to_csv(os.path.join(self.save, '互操作/' + '互操作_NR-NR重选.csv'), encoding='gbk', index=False)
        mlogger.info(f'NR-NR重选完成')

    def nr_lte_res_analyse(self):
        self.hand_nr_lte_res()
        self.lteRes['是否合规'] = self.lteRes['EUTRAN小区重选频点优先级'].apply(lambda x: '否' if x > 3 else '是')
        self.lteRes_error = self.lteRes[self.lteRes['是否合规'] == '否']
        self.lteRes_error.to_excel(os.path.join(self.save, 'TOP/' + 'NR_LTE重选优先级不合规.xlsx'), index=False)

    def hand_nr_lte_res(self):
        res_lst = []
        for csv in self.lst:
            mlogger.info(f'NR-LTE重选：{csv}')
            res = self.associate(csv, 'EUTRAReselection')
            EUTRAReselection = ["ManagedElement", "ldn", "moId", "refEutranFreqRelation", "cellReselectionPriority",
                                "qRxLevMin",
                                "threshXHigh", "threshXLow", "allowedMeasBandwidth", "cellReselectionSubPriority",
                                "refEutranFreq",
                                "frequency", "freqBand"]

            res = res[EUTRAReselection]
            res['ldn'] = (res['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") +
                          res['ldn'].apply(lambda x: x.split(',CellResel=')[0]))
            NRCellCU = self.hand_cell()
            NRCellCU['ldn'] = NRCellCU['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + NRCellCU['ldn']
            Resel = pd.read_excel(csv, sheet_name='CellResel', skiprows=[1, 2, 3, 4])
            Resel['ldn'] = Resel['ManagedElement'].apply(lambda x: "Ne=" + str(x) + ",") + Resel['ldn']
            Resel['ldn'] = Resel['ldn'].apply(lambda x: x.split(',CellResel=')[0])
            CellResel = ["ldn", "qHyst", "threshServingLowP", "cellReselectionPriority", "sNonIntraSearchSwitch",
                         "sNonIntraSearchP", "cellReselectionSubPriority"]
            Resel = Resel[CellResel]
            NRCellCU = pd.merge(NRCellCU, Resel, on='ldn', suffixes=('', '_CellResel'))
            NRCellCU = pd.merge(NRCellCU, res, on='ldn', suffixes=('', '_EUTRAReselection'))
            res_lst.append(NRCellCU)

        self.lteRes = pd.concat(res_lst, join='outer', ignore_index=True)
        self.lteRes.to_csv(os.path.join(self.save, '互操作/' + '互操作_NR-LTE重选.csv'), encoding='gbk', index=False)
        mlogger.info(f'NR-LTE重选完成')

    def hand_es(self, file):
        """
        节能参数整理
        :param file:
        :return: pandas
        """
        print(file)
        mlogger.info(f'节能：{file}')
        names = pd.ExcelFile(file).sheet_names
        print(names)
        if 'EUtranCellTDD' in names:
            cell = pd.read_excel(file, sheet_name='EUtranCellTDD', skiprows=[1, 2, 3, 4])[
                ['SubNetwork', 'MEID', 'MOI', 'cellLocalId', 'userLabel']]
            df = self.associate(file, 'SonCellPolicyTDD')
            df['MOI'] = df['MOI'].apply(lambda x: x.rsplit(',', 1)[0])
            cell = pd.merge(cell, df, on='MOI', how='left', suffixes=('', '_SON'))
            # cell =cell.dropna(axis=1,inplace=True)
            cell['ENB'] = cell['MOI'].apply(lambda x: x.rsplit(',', 2)[1].split('=')[-1])

        elif 'EUtranCellFDD' in names:
            cell = pd.read_excel(file, sheet_name='EUtranCellFDD', skiprows=[1, 2, 3, 4])[
                ['SubNetwork', 'MEID', 'MOI', 'cellLocalId', 'userLabel']]
            df = self.associate(file, 'SonCellPolicy')
            df['MOI'] = df['MOI'].apply(lambda x: x.rsplit(',', 1)[0])
            cell = pd.merge(cell, df, on='MOI', how='left', suffixes=('', '_SON'))
            # cell =cell.dropna(axis=1,inplace=True)
            cell['ENB'] = cell['MOI'].apply(lambda x: x.rsplit(',', 2)[1].split('=')[-1])
        elif 'EUtranCellFDDLTE' in names:
            cell = pd.read_excel(file, sheet_name='EUtranCellFDDLTE', skiprows=[1, 2, 3, 4])[
                ['SubNetwork', 'MEID', 'MOI', 'cellLocalId', 'userLabel']]
            df = self.associate(file, 'SonCellPolicyFDDLTE')
            df['MOI'] = df['MOI'].apply(lambda x: x.rsplit(',', 1)[0])
            cell = pd.merge(cell, df, on='MOI', how='left', suffixes=('', '_SON'))
            # cell =cell.dropna(axis=0,inplace=True)
            cell['ENB'] = cell['MOI'].apply(lambda x: x.rsplit(',', 2)[1].split('=')[-1])

        elif 'EUtranCellTDDLTE' in names:
            cell = pd.read_excel(file, sheet_name='EUtranCellTDDLTE', skiprows=[1, 2, 3, 4])[
                ['SubNetwork', 'MEID', 'MOI', 'cellLocalId', 'userLabel']]
            df = self.associate(file, 'SonCellPolicyTDDLTE')
            df['MOI'] = df['MOI'].apply(lambda x: x.rsplit(',', 1)[0])
            cell = pd.merge(cell, df, on='MOI', how='left', suffixes=('', '_SON'))
            # cell =cell.dropna(axis=1,inplace=True)
            cell['ENB'] = cell['MOI'].apply(lambda x: x.rsplit(',', 2)[1].split('=')[-1])
        elif 'CUEUtranCellTDDLTE' in names:
            cell = pd.read_excel(file, sheet_name='CUEUtranCellTDDLTE', skiprows=[1, 2, 3, 4])[
                ['SubNetwork', 'ManagedElement', 'ldn', 'cellLocalId', 'userLabel']]
            df = self.associate(file, 'SonCellPolicyTDDLTE')
            df['ldn'] = df['ldn'].apply(lambda x: x.rsplit(',', 2)[0])
            cell = pd.merge(cell, df, on='ldn', how='left', suffixes=('', '_SON'))
            # cell =cell.dropna(axis=1,inplace=True)
            cell['ENB'] = cell['ldn'].apply(lambda x: x.split(',')[0].split('=')[-1])
        elif 'CUEUtranCellFDDLTE' in names:
            cell = pd.read_excel(file, sheet_name='CUEUtranCellFDDLTE', skiprows=[1, 2, 3, 4])[
                ['SubNetwork', 'ManagedElement', 'ldn', 'cellLocalId', 'userLabel']]
            df = self.associate(file, 'SonCellPolicyFDDLTE')
            df['ldn'] = df['ldn'].apply(lambda x: x.rsplit(',', 2)[0])
            cell = pd.merge(cell, df, on='ldn', how='left', suffixes=('', '_SON'))
            # cell =cell.dropna(axis=1,inplace=True)
            cell['ENB'] = cell['ldn'].apply(lambda x: x.split(',')[0].split('=')[-1])
        else:
            cell = pd.DataFrame()
        return cell


if __name__ == '__main__':
    MyNorth = north_cm([r'./resource/excel'], r'./save')
    lst_TMM = []
    lst_U31 = []
    for i in os.listdir(r'./resource/excel'):
        file_path = os.path.join(r'./resource/excel', i)
        if i.startswith('RANCM-'):
            # lst_TMM.append()
            MyNorth.hand_nr_nr_res()
            MyNorth.hand_nr_lte_res()
            MyNorth.hand_nr_nr_ho('default', '1')
            MyNorth.hand_nr_lte_ho('default', '1')

    # df_res = pd.concat(lst_U31, join='inner', axis=0)
    # df_res.to_excel(os.path.join(MyNorth.save, '节能_U31.xlsx'), index=False)
    # df_res = pd.concat(lst_TMM, join='inner', axis=0)
    # df_res.to_excel(os.path.join(MyNorth.save, '节能_UME.xlsx'), index=False)
