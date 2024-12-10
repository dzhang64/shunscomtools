# -*- coding: UTF-8 -*-
import warnings
from collections import Counter

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

from CalRelation import p_intersection
from function_define import distancefuc, se_angle, knn_distance, wgs842utm
from OtherFunctions.myemail import SendMail


def greater_than_min(v: int, ls: list):
    for i in sorted(ls):
        if i > v:
            ncs = i
            break
    return ncs


class pci:
    def __init__(self, pci0, pci1, M0, M1, M2, file):
        self.PCI = [i for i in range(int(pci0), int(pci1) + 1)]
        self.M0 = M0  # 方位角1
        self.M1 = M1  # 方位角2
        self.M2 = M2  # 方位角3
        self.ncs = ''
        self.resource = pd.read_excel(file)  # 带规划表
        self.result = pd.DataFrame()
        self.state = 0
        self.info = ''
        self.saveRoute = ''

    def check_azimuth(self):
        # 方位角，根据方位角1,以120度进行更新
        if self.M0 + 120 >= 360:
            self.M1 = self.M0 + 120 - 360
        else:
            self.M1 = self.M0 + 120
        if self.M0 + 240 > 360:
            self.M2 = self.M0 + 240 - 360
        else:
            self.M2 = self.M0 + 240

    def workable_pci(self, pci_used: list, Azimuth: int):
        pci_usable = [i for i in self.PCI if i not in pci_used]  # 可用PCI
        if len(pci_usable) != 0:
            if int(self.M1) < int(Azimuth) <= int(self.M1) + 120:
                pci_usable1 = [i for i in pci_usable if i % 3 == 1]
                if len(pci_usable1) != 0:
                    PlannedPCI = pci_usable1[0]
                else:
                    PlannedPCI = pci_usable[0]
            elif int(self.M1) + 120 < int(Azimuth) <= int(self.M1) + 240:
                pci_usable1 = [i for i in pci_usable if i % 3 == 2]
                if len(pci_usable1) != 0:
                    PlannedPCI = pci_usable1[0]
                else:
                    PlannedPCI = pci_usable[0]
            else:
                pci_usable1 = [i for i in pci_usable if i % 3 == 0]
                if len(pci_usable1) != 0:
                    PlannedPCI = pci_usable1[0]
                else:
                    PlannedPCI = pci_usable[0]
        else:
            PlannedPCI = '无可用PCI'
        return PlannedPCI

    def used_pci(self, dis):
        """

        @param dis: 复用距离米
        @return: 生产规划PCI
        """

        warnings.filterwarnings('ignore')
        # 生成全量PCI

        self.resource['CurrentPCI'].astype('int')
        find = self.resource[self.resource['PCINeeded'] == 1].reset_index(drop=True)  # 待规划PCI小区
        # 从数据库中筛选出经纬度特征数据，用于给KNN分类器训练
        data_fit = self.resource.loc[:, ['LON', 'LAT']]
        # y本身用于标注每条数据属于哪个类别，但我并不使用KNN的分类功能，所以统一全部标注为类别1
        y = [1] * len(data_fit)
        # 筛选需要求出最近N个点的的基站的经纬度特征数据
        find_x = find.loc[:, ['LON', 'LAT']]
        # 指定算法为ball_tree
        knn = KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', metric=lambda s1, s2: distancefuc(*s1, *s2))
        # 训练模型
        knn.fit(data_fit, y)
        # 计算它们最近的N个（n_neighbors）点，这里生成全量数据便于后面筛选距离
        distance, points = knn.kneighbors(find_x, n_neighbors=self.resource.shape[0], return_distance=True)

        for i, row in find.iterrows():
            tmp = self.resource.iloc[points[i]]
            tmp['距离'] = distance[i]
            tmp = tmp[tmp['距离'] < dis]
            tmp1 = tmp[tmp['PCINeeded'] == 0]
            used = list(tmp['CurrentPCI'])
            if self.result.shape[0] != 0:  # 剔除已规划过的PCI
                for j, row_j in self.result.iterrows():
                    if row_j['CELLNAME'] in list(tmp['CELLNAME']):
                        used.append(self.result.loc[j]['PlannedPCI'])

            s = pd.DataFrame(row).T
            PCI_Planned = self.workable_pci(pci_used=used, Azimuth=int(s['Azimuth']), )
            TAC = list(tmp1['TAC'])

            s['PlannedPCI'] = PCI_Planned
            s['TAC_最近'] = TAC[0]
            tac1 = Counter(TAC).most_common(1)
            s['TAC_最多'] = int(tac1[0][0])
            self.result = pd.concat([self.result, s])
            self.state = 1

    def prach(self, f_prach, d_prach, out_file, email_str):
        if self.state == 1:
            self.saveRoute = out_file
            if f_prach == '839':
                ncs = 1.04875 * (6.67 * (d_prach / 1000) + 5 + 2)
                ncs = greater_than_min(ncs, [0, 13, 15, 18, 22, 26, 32, 38, 46, 59, 76, 93, 119, 167, 279, 419])
                self.ncs = (str(ncs))
                ncs = int(838 / ncs)
                ncs1 = int(64 / ncs) + 1
                ncs2 = int(838 / ncs1)
                self.result['rootsequencelndex'] = self.result['PlannedPCI'].apply(
                    lambda x: ncs1 * (x - int(x / ncs2) * ncs2))
            elif f_prach == '139':
                ncs = 1.045 * (6.67 * (d_prach / 1000) + 5 + 2)
                ncs = greater_than_min(ncs, [2, 4, 6, 8, 10, 12, 15])
                self.ncs = (str(ncs))
                ncs = int(138 / ncs)
                ncs1 = int(64 / ncs) + 1
                ncs2 = int(138 / ncs1)
                self.result['rootsequencelndex'] = self.result['PlannedPCI'].apply(
                    lambda x: ncs1 * (x - int(x / ncs2) * ncs2))

            self.result.to_excel(out_file, index=False)
            if ',' in email_str:
                em_lt = list(email_str.split(','))
                em_lt1 = [i for i in em_lt if '@' in i]
                em = SendMail()
                bd = f"""<b><body>你好！</b><br>
                        <b><body>你正在使用顺盛网优工具。PCI规划详细结果请查看附件。</b><br>
                        <b><body>\n</b><br>
                        <b><body>\n</b><br>
                        <b><body>如有问题或新增功能，请联系邮箱wangxinyue@shunscom.com或电话18921790946(微信同号)</b><br>
                    """
                info = em.send(toAddrs=em_lt1, subject="网优工具-PCI规划", msg=bd, file_path=[out_file])
                self.info = f"{info}"
            else:
                self.info = f"""每个邮箱后加',' """


class neighbor:
    def __init__(self, planRoute, GCRoute):
        self.planRoute = planRoute  # 待规划路径
        self.GCRoute = GCRoute  # 工参路径
        self.state = 0
        self.info = ''
        self.saveRoute = ''

        self.result = pd.DataFrame(
            columns=["ENBID", "CI_1", "CellName_1", "LON_1", "LAT_1", "azimuth_1", "HBWD_1", "type_1", "TA_1", "CI_2",
                     "CellName_2", "LON_2", "LAT_2", "azimuth_2", "HBWD_2", "type_2", "TA_2", "距离",
                     "重叠比例_源正邻正",
                     "重叠比例_源背邻正", "重叠比例_源正邻背", "重叠比例_源背邻背", '重叠比例_权重'])

    def plan_neighbor(self, output, Abandon_D, TA_R, HBWD_R):
        find_P = pd.read_excel(self.planRoute)  # 待规划小区
        data_S = pd.read_excel(self.GCRoute)  # 全量小区(工参)
        data = pd.concat([find_P, data_S], join='inner', axis=0).reset_index(drop=True)

        for i, row in find_P.iterrows():
            find = pd.DataFrame(row).T
            distance, points = knn_distance(data, find)
            tmp = data.iloc[points[0]]  # 按距离排序
            tmp.insert(1, '距离', list(distance[0]))
            Overlap_data = tmp[tmp['距离'] < Abandon_D]
            re = find.join(Overlap_data, how='outer', lsuffix='_1', rsuffix='_2').ffill(axis=0).bfill(axis=0)
            xy_1 = [(wgs842utm(i[0], i[1])[0], wgs842utm(i[0], i[1])[1]) for i in zip(re['LON_1'], re['LAT_1'])]
            xy_2 = [(wgs842utm(i[0], i[1])[0], wgs842utm(i[0], i[1])[1]) for i in zip(re['LON_2'], re['LAT_2'])]

            Overlap_rate1, Overlap_rate2, Overlap_rate3, Overlap_rate4 = [], [], [], []
            for j in range(re.shape[0]):
                # x0 = re['x_1'].iloc[j]
                # y0 = 0 - re['y_1'].iloc[j]  # 左上角（0，0）x往右越来越大，y往下越来越大，故要使AB两个的相对位置不变，y值取反
                x0 = xy_1[j][0]
                y0 = 0 - xy_1[j][1]  # 左上角（0，0）x往右越来越大，y往下越来越大，故要使AB两个的相对位置不变，y值取反
                start_angle0, end_angle0 = se_angle(angle=re['azimuth_1'].iloc[j], HBWD=re['HBWD_1'].iloc[j],
                                                    HBWD_R=HBWD_R)
                r0 = re['TA_1'].iloc[j]

                # x1 = re['x_2'].iloc[j]
                # y1 = 0 - re['y_2'].iloc[j]
                x1 = xy_2[j][0]
                y1 = 0 - xy_2[j][1]
                start_angle1, end_angle1 = se_angle(angle=re['azimuth_2'].iloc[j], HBWD=re['HBWD_2'].iloc[j],
                                                    HBWD_R=HBWD_R)
                r1 = re['TA_2'].iloc[j] * TA_R
                Overlap_rate1.append(
                    p_intersection(x0, y0, start_angle0, end_angle0, r0, x1, y1, start_angle1, end_angle1, r1))
                Overlap_rate2.append(
                    p_intersection(x0, y0, start_angle0 - 180, end_angle0 - 180, r0 / 10, x1, y1, start_angle1,
                                   end_angle1,
                                   r1))
                Overlap_rate3.append(
                    p_intersection(x0, y0, start_angle0, end_angle0, r0, x1, y1, start_angle1 - 180, end_angle1 - 180,
                                   r1 / 10))
                Overlap_rate4.append(
                    p_intersection(x0, y0, start_angle0 - 180, end_angle0 - 180, r0 / 10, x1, y1, start_angle1 - 180,
                                   end_angle1 - 180, r1 / 10))

            re['重叠比例_源正邻正'] = Overlap_rate1
            re['重叠比例_源背邻正'] = Overlap_rate2
            re['重叠比例_源正邻背'] = Overlap_rate3
            re['重叠比例_源背邻背'] = Overlap_rate4
            re['重叠比例_权重'] = re['重叠比例_源正邻正'] * 0.5 + re['重叠比例_源背邻正'] * 0.2 + re[
                '重叠比例_源正邻背'] * 0.2 + re['重叠比例_源背邻背'] * 0.1
            res = pd.concat([res, re], join='inner', axis=0)
        res['对比结果'] = res[['CI_1', 'CI_2']].apply(lambda x: x['CI_1'] == x['CI_2'], axis=1)
        res1 = res[res['对比结果'] == 0]
        del res1['对比结果']
        res1.sort_values(by=['CI_1', "重叠比例_权重", '距离'], ascending=[True, False, True], inplace=True)
        res1.to_excel(output, index=False)
        return 1, res1
