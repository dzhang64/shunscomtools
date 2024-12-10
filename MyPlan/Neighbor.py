# -*- coding: UTF-8 -*-
from MyPlan.CalRelation import *
from MyPlan.function_define import *
import pandas as pd


"""
遵循频点规则
1、本站内双向邻区必加
2、主覆盖方向加两层
3、非主覆盖方向加一层
4、考虑特殊场景特殊规则
5、涉及跨核心网跨地市，相关数据及反向。
6、注意控制数量（23G31条，4G256条）
7、2G邻区 不能跨pool
"""


# find_P = pd.read_excel(r"5G工具邻区.xlsx",sheet_name='源站点')#全量小区含待规划PCI小区
# data_S = pd.read_excel(r"5G工具邻区.xlsx",sheet_name='核查范围')#全量小区含待规划PCI小区(工参)
# data=pd.concat([find_P,data_S],join='inner',axis=0).reset_index(drop=True)
# Strong_D = 1000
# Abandon_D = 100000
# TA_R = 1.5
# HBWD_R = 1.5
# file1 = r'F:\shunscomtools\code\邻区待规划表.xlsx'
# file2 = r'F:\shunscomtools\code\工参.xlsx'
# output = r'F:\shunscomtools\code\code\邻区规划表.xlsx'
# warnings.filterwarnings('ignore')


def se_angle(angle, HBWD, HBWD_R):
    if float(HBWD) * HBWD_R >= 360:
        s0 = 0
        e0 = 360
    else:
        s0 = azimuth_xy(angle) - float(HBWD) * HBWD_R / 2
        e0 = azimuth_xy(angle) + float(HBWD) * HBWD_R / 2
    return s0, e0


def plan_neighbor(file1, file2, output, Abandon_D, TA_R, HBWD_R):
    find_P = pd.read_excel(file1)  # 全量小区含待规划PCI小区
    data_S = pd.read_excel(file2)  # 全量小区含待规划PCI小区(工参)
    data = pd.concat([find_P, data_S], join='inner', axis=0).reset_index(drop=True)

    res = pd.DataFrame(
        columns=["ENBID", "CI_1", "CellName_1", "LON_1", "LAT_1", "azimuth_1", "HBWD_1", "type_1", "TA_1", "CI_2",
                 "CellName_2", "LON_2", "LAT_2", "azimuth_2", "HBWD_2", "type_2", "TA_2", "距离", "重叠比例_源正邻正",
                 "重叠比例_源背邻正", "重叠比例_源正邻背", "重叠比例_源背邻背", '重叠比例_权重'])
    for i, row in find_P.iterrows():
        find = pd.DataFrame(row).T
        distance, points = knn_distance(data, find)
        tmp = data.iloc[points[0]]  # 按距离排序
        tmp.insert(1, '距离', list(distance[0]))
        Overlap_data = tmp[tmp['距离'] < Abandon_D]
        re = find.join(Overlap_data, how='outer', lsuffix='_1', rsuffix='_2').ffill(axis=0).bfill(axis=0)
        xy_1 = [(wgs842utm(i[0], i[1])[0], wgs842utm(i[0], i[1])[1]) for i in zip(re['LON_1'], re['LAT_1'])]
        xy_2 = [(wgs842utm(i[0], i[1])[0], wgs842utm(i[0], i[1])[1]) for i in zip(re['LON_2'], re['LAT_2'])]
        # re['x_1'] = [i[0] for i in xy_1]
        # re['y_1'] = [i[1] for i in xy_1]
        # re['x_2'] = [i[0] for i in xy_2]
        # re['y_2'] = [i[1] for i in xy_2]

        Overlap_rate1, Overlap_rate2, Overlap_rate3, Overlap_rate4 = [], [], [], []
        for j in range(re.shape[0]):
            # x0 = re['x_1'].iloc[j]
            # y0 = 0 - re['y_1'].iloc[j]  # 左上角（0，0）x往右越来越大，y往下越来越大，故要使AB两个的相对位置不变，y值取反
            x0 = xy_1[j][0]
            y0 = 0 - xy_1[j][1]  # 左上角（0，0）x往右越来越大，y往下越来越大，故要使AB两个的相对位置不变，y值取反
            start_angle0, end_angle0 = se_angle(angle=re['azimuth_1'].iloc[j], HBWD=re['HBWD_1'].iloc[j], HBWD_R=HBWD_R)
            r0 = re['TA_1'].iloc[j]

            # x1 = re['x_2'].iloc[j]
            # y1 = 0 - re['y_2'].iloc[j]
            x1 = xy_2[j][0]
            y1 = 0 - xy_2[j][1]
            start_angle1, end_angle1 = se_angle(angle=re['azimuth_2'].iloc[j], HBWD=re['HBWD_2'].iloc[j], HBWD_R=HBWD_R)
            r1 = re['TA_2'].iloc[j] * TA_R
            Overlap_rate1.append(
                p_intersection(x0, y0, start_angle0, end_angle0, r0, x1, y1, start_angle1, end_angle1, r1))
            Overlap_rate2.append(
                p_intersection(x0, y0, start_angle0 - 180, end_angle0 - 180, r0 / 10, x1, y1, start_angle1, end_angle1,
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
        re['重叠比例_权重'] = re['重叠比例_源正邻正'] * 0.5 + re['重叠比例_源背邻正'] * 0.2 + re['重叠比例_源正邻背'] * 0.2 + re['重叠比例_源背邻背'] * 0.1
        res = pd.concat([res, re], join='inner', axis=0)
    res['对比结果'] = res[['CI_1', 'CI_2']].apply(lambda x: x['CI_1'] == x['CI_2'], axis=1)
    res1 = res[res['对比结果'] == 0]
    del res1['对比结果']
    res1.sort_values(by=['CI_1', "重叠比例_权重", '距离'], ascending=[True, False, True], inplace=True)
    res1.to_excel(output, index=False)
    return 1, res1
