# -*- coding: UTF-8 -*-
import warnings
from math import *
import random

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter

global selected_number, num


def greater_than_min(v, ls: list):
    for i in sorted(ls):
        if i > v:
            ncs = i
            break
    return ncs


def distancefuc(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(
        radians,
        [float(lon1), float(lat1),
         float(lon2), float(lat2)])  # 经纬度转换成弧度
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance, 0)
    return distance


def pci_group(pci_all, used):
    """
    PCI划分组
    :param pci_all: PCI范围
    :param used: 已使用的PCI
    :return: PCIGroup_normal（正常PCI组）, PCIGroup_abnormal（非正常的PCI组）, list(PCIGroup_mix)
    """
    PCIGroup0 = [i for i in pci_all if i % 3 == 0]
    PCIGroup1 = [i for i in pci_all if i % 3 == 1]
    PCIGroup2 = [i for i in pci_all if i % 3 == 2]
    PCIGroup = [[i[0], i[1], i[2]] for i in zip(PCIGroup0, PCIGroup1, PCIGroup2)]
    for x in PCIGroup:
        for y in used:
            if y in x:
                x.remove(y)
    PCIGroup_normal = []
    PCIGroup_b = []
    for x in PCIGroup:
        if len(x) == 3:
            PCIGroup_normal.append(x)
        else:
            for y in x:
                PCIGroup_b.append(y)
    PCIGroup0 = [i for i in PCIGroup_b if i % 3 == 0]
    PCIGroup1 = [i for i in PCIGroup_b if i % 3 == 1]
    PCIGroup2 = [i for i in PCIGroup_b if i % 3 == 2]
    PCIGroup_abnormal = [[i[0], i[1], i[2]] for i in zip(PCIGroup0, PCIGroup1, PCIGroup2)]
    if PCIGroup_normal:
        pci0, pci1, pci2 = zip(*PCIGroup_normal)
    else:
        pci0, pci1, pci2 = [], [], []
    if PCIGroup_abnormal:
        pci00, pci11, pci22 = zip(*PCIGroup_abnormal)
        PCIGroup_mix = set([i for i in pci_all]) - set(pci0) - set(pci1) - set(pci2) - set(pci00) - set(
            pci11) - set(pci22) - set(used)
    else:
        PCIGroup_mix = set([i for i in pci_all]) - set(pci0) - set(pci1) - set(pci2) - set(used)
    return PCIGroup_normal, PCIGroup_abnormal, list(PCIGroup_mix)


def workable_pci(pci_usable: list, Azimuth: int, m0_azimuth_range: int):
    a2 = m0_azimuth_range
    if len(pci_usable) != 0:
        if int(a2) < int(Azimuth) <= int(a2) + 120:
            pci_usable1 = [i for i in pci_usable if i % 3 == 1]
            if len(pci_usable1) != 0:
                PlannedPCI = pci_usable1[0]
            else:
                PlannedPCI = pci_usable[0]
        elif int(a2) + 120 < int(Azimuth) <= int(a2) + 240:
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
        pci_usable.remove(PlannedPCI)
    else:
        PlannedPCI = '无可用PCI'
    return PlannedPCI, pci_usable


def plan_pci(PCI_range, azimuth0_range, dis, infile):
    warnings.filterwarnings('ignore')
    # 生成全量PCI
    P1, P2 = PCI_range.split(',')
    PCI = [i for i in range(int(P1), int(P2) + 1)]

    data = pd.read_excel(infile)  # 全量小区含待规划PCI小区
    data['CurrentPCI'].astype('int')
    data['LONLAT'] = data['LON'].apply(lambda x: str(x)) + data['LAT'].apply(lambda x: str(x))
    data.sort_values(by=['LONLAT'], ascending=True, inplace=True, na_position='first')
    del data['LONLAT']
    find = data[data['PCINeeded'] == 1].reset_index(drop=True)  # 待规划PCI小区
    # 从数据库中筛选出经纬度特征数据，用于给KNN分类器训练
    data_fit = data.loc[:, ['LON', 'LAT']]
    # y本身用于标注每条数据属于哪个类别，但我并不使用KNN的分类功能，所以统一全部标注为类别1
    y = [1] * len(data_fit)
    # 筛选需要求出最近N个点的的基站的经纬度特征数据
    find_x = find.loc[:, ['LON', 'LAT']]
    # 指定算法为ball_tree
    knn = KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', metric=lambda s1, s2: distancefuc(*s1, *s2))
    # 训练模型
    knn.fit(data_fit, y)
    # 计算它们最近的N个（n_neighbors）点，这里生成全量数据便于后面筛选距离
    distance, points = knn.kneighbors(find_x, n_neighbors=data.shape[0], return_distance=True)
    result = pd.DataFrame()  # 定义空帧，存放结果
    s0 = ''
    num = 0
    for i, row in find.iterrows():
        tmp = data.iloc[points[i]]
        tmp['距离'] = distance[i]
        tmp = tmp[tmp['距离'] < dis]
        tmp1 = tmp[tmp['PCINeeded'] == 0]
        used = list(tmp['CurrentPCI'])
        if result.shape[0] != 0:  # 剔除已规划过的PCI
            for j, row_j in result.iterrows():
                if row_j['CELLNAME'] in list(tmp['CELLNAME']):
                    used.append(result.loc[j]['PlannedPCI'])

        s = pd.DataFrame(row).T

        pci_group0, pci_group1, pci_group2 = pci_group(pci_all=PCI, used=used)
        if pci_group0:
            if s0 != str(row['LON']) + str(row['LAT']) or num == 3:
                num = 1
                sel_number = random.choice(pci_group0)
            else:
                num += 1
        elif pci_group1:
            if s0 != str(row['LON']) + str(row['LAT']) or num == 3:
                num = 1
                sel_number = random.choice(pci_group1)
            else:
                num += 1
        elif pci_group2:
            if s0 != str(row['LON']) + str(row['LAT']) or num == 3:
                num = 1
                sel_number = random.choice(pci_group1)
            else:
                num += 1
        else:
            sel_number = []
        s0 = str(row['LON']) + str(row['LAT'])
        PCI_Planned, sel_number = workable_pci(pci_usable=sel_number, Azimuth=int(s['Azimuth']),
                                               m0_azimuth_range=azimuth0_range)
        TAC = list(tmp1['TAC'])
        s['PlannedPCI'] = PCI_Planned
        if TAC:
            s['TAC_最近'] = TAC[0]
            tac1 = Counter(TAC).most_common(1)
            s['TAC_最多'] = int(tac1[0][0])
        else:
            s['TAC_最近'] = None
            s['TAC_最多'] = None
        result = pd.concat([result, s])
    return 1, result


def plan_pci2(PCI_range, azimuth0_range, dis, data: pd.DataFrame):
    warnings.filterwarnings('ignore')
    # 生成全量PCI
    P1, P2 = PCI_range.split(',')
    PCI = [i for i in range(int(P1), int(P2) + 1)]

    data['CurrentPCI'].astype('int')
    data['LONLAT'] = data['LON'].apply(lambda x: str(x)) + data['LAT'].apply(lambda x: str(x))
    data.sort_values(by=['LONLAT'], ascending=True, inplace=True, na_position='first')
    del data['LONLAT']
    find = data[data['PCINeeded'] == 1].reset_index(drop=True)  # 待规划PCI小区
    if find.shape[0] != 0:
        # 从数据库中筛选出经纬度特征数据，用于给KNN分类器训练
        data_fit = data.loc[:, ['LON', 'LAT']]
        # y本身用于标注每条数据属于哪个类别，但我并不使用KNN的分类功能，所以统一全部标注为类别1
        y = [1] * len(data_fit)
        # 筛选需要求出最近N个点的的基站的经纬度特征数据
        find_x = find.loc[:, ['LON', 'LAT']]
        # 指定算法为ball_tree
        knn = KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', metric=lambda s1, s2: distancefuc(*s1, *s2))
        # 训练模型
        knn.fit(data_fit, y)
        # 计算它们最近的N个（n_neighbors）点，这里生成全量数据便于后面筛选距离
        distance, points = knn.kneighbors(find_x, n_neighbors=data.shape[0], return_distance=True)
        result = pd.DataFrame()  # 定义空帧，存放结果
        s0 = ''
        num = 0
        for i, row in find.iterrows():
            tmp = data.iloc[points[i]]
            tmp['距离'] = distance[i]
            tmp = tmp[tmp['距离'] < dis]
            # tmp1 = tmp[tmp['PCINeeded'] == 0]
            used = list(tmp['CurrentPCI'])
            if result.shape[0] != 0:  # 剔除已规划过的PCI
                for j, row_j in result.iterrows():
                    if row_j['CELLNAME'] in list(tmp['CELLNAME']):
                        used.append(result.loc[j]['PlannedPCI'])

            s = pd.DataFrame(row).T

            pci_group0, pci_group1, pci_group2 = pci_group(pci_all=PCI, used=used)
            if pci_group0:
                if s0 != str(row['LON']) + str(row['LAT']) or num == 3:
                    num = 1
                    sel_number = random.choice(pci_group0)
                else:
                    num += 1
            elif pci_group1:
                if s0 != str(row['LON']) + str(row['LAT']) or num == 3:
                    num = 1
                    sel_number = random.choice(pci_group1)
                else:
                    num += 1
            elif pci_group2:
                if s0 != str(row['LON']) + str(row['LAT']) or num == 3:
                    num = 1
                    sel_number = random.choice(pci_group1)
                else:
                    num += 1
            else:
                sel_number = []
            s0 = str(row['LON']) + str(row['LAT'])
            PCI_Planned, sel_number = workable_pci(pci_usable=sel_number, Azimuth=int(s['Azimuth']),
                                                   m0_azimuth_range=azimuth0_range)
            s['PlannedPCI'] = PCI_Planned
            result = pd.concat([result, s])
        return 1, result

    else:
        return 0, pd.DataFrame()


def plan_tac(dis, data: pd.DataFrame):
    warnings.filterwarnings('ignore')

    data['CurrentPCI'].astype('int')
    data['LONLAT'] = data['LON'].apply(lambda x: str(x)) + data['LAT'].apply(lambda x: str(x))
    data.sort_values(by=['LONLAT'], ascending=True, inplace=True, na_position='first')
    del data['LONLAT']
    find = data[data['PCINeeded'] == 1].reset_index(drop=True)  # 待规划PCI小区
    # 从数据库中筛选出经纬度特征数据，用于给KNN分类器训练
    data_fit = data.loc[:, ['LON', 'LAT']]
    # y本身用于标注每条数据属于哪个类别，但我并不使用KNN的分类功能，所以统一全部标注为类别1
    y = [1] * len(data_fit)
    # 筛选需要求出最近N个点的的基站的经纬度特征数据
    find_x = find.loc[:, ['LON', 'LAT']]
    # 指定算法为ball_tree
    knn = KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', metric=lambda s1, s2: distancefuc(*s1, *s2))
    # 训练模型
    knn.fit(data_fit, y)
    # 计算它们最近的N个（n_neighbors）点，这里生成全量数据便于后面筛选距离
    distance, points = knn.kneighbors(find_x, n_neighbors=data.shape[0], return_distance=True)
    result = pd.DataFrame()  # 定义空帧，存放结果
    for i, row in find.iterrows():
        tmp = data.iloc[points[i]]
        tmp['距离'] = distance[i]
        tmp = tmp[tmp['距离'] < dis]
        tmp1 = tmp[tmp['PCINeeded'] == 0]
        s = pd.DataFrame(row).T

        TAC = list(tmp1['TAC'])
        if TAC:
            s['TAC_最近'] = TAC[0]
            tac1 = Counter(TAC).most_common(1)
            s['TAC_最多'] = int(tac1[0][0])
        else:
            s['TAC_最近'] = None
            s['TAC_最多'] = None
        result = pd.concat([result, s])
    return 1, result
