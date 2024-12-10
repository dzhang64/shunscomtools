import os
import sqlite3
import pandas as pd
# import modin.pandas as pm
import traceback
import gc
# import ray
import warnings
import time
from OtherFunctions.logdefine import MyLogging

warnings.filterwarnings('ignore')
t = time.strftime("%Y%m%d")
mlogger = MyLogging(file=f"./log.log")
# ray.init()

dic = {'nr': ['NRCellRelation', 'ExternalNRCellCU', 'NRFreq', 'NRCellCU', 'EutranCellRelation',
              'ExternalEutranCellTDD', 'ExternalEutranCellFDD'],
       'tmm': ['EUtranRelationTDDLTE', 'EUtranRelationFDDLTE', 'ExternalEUtranCellFDDLTE',
               'ExternalEUtranCellTDDLTE', 'CUEUtranCellFDDLTE', 'CUEUtranCellTDDLTE'],
       'icm': ['EUtranRelationFDDLTE', 'EUtranRelationTDDLTE', 'ExternalEUtranCellFDDLTE',
               'ExternalEUtranCellTDDLTE', 'EUtranCellFDDLTE', 'EUtranCellTDDLTE', 'EUtranRelationTDD',
               'ExternalEUtranTCellFDD', 'ExternalEUtranTCellTDD', 'EUtranCellTDD', 'EUtranRelation',
               'EUtranCellFDD', 'ExternalEUtranCellFDD',
               'ExternalEUtranCellTDD']}


def split_func(s, delimiter=',', num=1):
    return s.rsplit(delimiter, num)[0]


def split_func2(s, delimiter=',', num=2):
    return s.rsplit(delimiter, num)[0]


class my_sqlite:
    def __init__(self, name):
        self.db_name = name

    def clear_database(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        connection = sqlite3.connect(self.db_name)
        connection.close()

    def drop_tab(self, tab):
        # 连接到数据库
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # 删除表
        cursor.execute(f"DROP TABLE IF EXISTS {tab};")
        conn.commit()
        cursor.execute("select name from sqlite_master where type='table'")
        tab_name = cursor.fetchall()
        tab_name = [line[0] for line in tab_name]
        print(tab_name)

        # 关闭连接
        conn.close()

    def delete_col(self, my_table, column_to_delete):
        # 连接到SQLite数据库（如果不存在，则会创建）
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # 假设我们要从名为`my_table`的表中删除名为`column_to_delete`的列
        table_name = f'{my_table}'
        column_to_delete = f'{column_to_delete}'

        # 创建一个新表，包含除了要删除的列以外的所有列
        cursor.execute(f"""
        CREATE TABLE new_table AS
        SELECT {', '.join([c[1] for c in cursor.execute(f"PRAGMA table_info({table_name})") if c[1] != column_to_delete])}
        FROM {table_name};
        """)

        # 删除旧表
        cursor.execute(f"DROP TABLE {table_name};")

        # 将新表重命名为旧表名
        cursor.execute(f"ALTER TABLE new_table RENAME TO {table_name};")

        # 提交事务
        conn.commit()

        # 关闭连接
        conn.close()

    def combined_column(self, my_table, name, column1, column2, sybom):
        # 连接到数据库（如果不存在，则会创建）
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # 假设表名为my_table，需要合并的两列为column1和column2，新列名为combined_column
        cursor.execute(f"ALTER TABLE {my_table} ADD COLUMN {name} TEXT")

        # 使用||运算符更新表，将column1和column2合并到新列中
        # str_h = f'||{sybom}'.join(col_lst)

        cursor.execute(f"UPDATE {my_table} SET {name} = {column1}||'{sybom}'|| {column2}")
        # cursor.execute(f"UPDATE {my_table} SET {name} = {str_h}")
        # 或者使用CONCAT函数
        # cursor.execute("UPDATE my_table SET {name} = CONCAT(column1, column2)")
        # 提交更改
        conn.commit()
        # 关闭连接
        conn.close()

    def lst_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

    def split(self, col, tab):
        self.delete_col(tab, 'dn')
        conn = sqlite3.connect(self.db_name)
        conn.create_function("SPLIT", 1, split_func)
        cur = conn.cursor()

        cur.execute(f"ALTER TABLE {tab} ADD COLUMN dn TEXT")
        cur.execute(f"UPDATE {tab} SET dn = SPLIT({col})")
        # cur.execute(f"SELECT SPLIT({col}) FROM {tab}")
        conn.commit()
        conn.close()

    def split2(self, col, tab):
        conn = sqlite3.connect(self.db_name)
        conn.create_function("SPLIT", 1, split_func2)
        cur = conn.cursor()
        cur.execute(f"ALTER TABLE {tab} ADD COLUMN dn TEXT")
        cur.execute(f"UPDATE {tab} SET dn = SPLIT({col})")
        # cur.execute(f"SELECT SPLIT({col}) FROM {tab}")
        conn.commit()
        conn.close()

    def count(self, col, tab):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {tab} ADD COLUMN PC TEXT")
        cursor.execute('''
        UPDATE {tab}  AS
        SELECT *,
               COUNT(item) AS frequency
        FROM my_table
        GROUP BY item;
        ''')
        cursor.execute(f"UPDATE {tab} SET PC = COUNT(*) FROM {tab} GROUP BY {col}")
        conn.commit()
        conn.close()


def import_neighbor(path, work_name, sheet):
    # my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
    # my_sqlite1.clear_database()
    sheet_names = pd.ExcelFile(path).sheet_names
    db = sqlite3.connect(f'{work_name}_neighbor_work.db')
    for i in sheet_names:
        if i.split('(')[0].split(' (')[0] in sheet:
            mlogger.info(f'导入邻区信息{i},{sheet}')
            df = pd.read_excel(path, sheet_name=i, skiprows=[1, 2, 3, 4], engine='calamine')
            # df = pm.read_excel(path, sheet_name=i, skiprows=[1, 2, 3, 4], engine=None)
            if i.startswith('ExternalEUtranCellTDD') and work_name in ['nr', 'tmm']:
                df['bandWidth'] = df['bandWidth'].apply(lambda x: x.split('[')[-1].replace(']', ''))
                # df['bandWidth'] = df['bandWidth'].apply(lambda x: str(x))
            elif i.startswith('ExternalEUtranCellFDD'):
                if work_name in ['nr']:
                    df['ulBandWidth'] = df['ulBandWidth'].apply(lambda x: x.split('[')[-1].replace(']', ''))
                    # df['ulBandWidth'] = df['ulBandWidth'].apply(lambda x: str(x))
                    df['dlBandWidth'] = df['dlBandWidth'].apply(lambda x: x.split('[')[-1].replace(']', ''))
                elif work_name in ['tmm']:
                    df['bandWidthDl'] = df['bandWidthDl'].apply(lambda x: x.split('[')[-1].replace(']', ''))
                    # df['ulBandWidth'] = df['ulBandWidth'].apply(lambda x: str(x))
                    df['bandWidthUl'] = df['bandWidthUl'].apply(lambda x: x.split('[')[-1].replace(']', ''))

                # df['dlBandWidth'] = df['dlBandWidth'].apply(lambda x: str(x))

            # elif i.startswith('ExternalNRCellCU'):
            #     df.rename(columns={'nRPCI': 'nRPCI'}, inplace=True)
            df.to_sql(i.split('(')[0].replace(' ', ''), db, if_exists='append', index=False)
            gc.collect()
    mlogger.info(f'导入邻区信息结束')
    db.close()


def import_cell(path):
    mlogger.info(f'导入小区信息')
    try:
        conn = sqlite3.connect('cell_work.db')
        sheetnames = pd.ExcelFile(path).sheet_names
        if 'NRCellCU' in sheetnames:
            try:
                NRCellCU = pd.read_excel(path, sheet_name='NRCellCU', skiprows=[1, 2, 3, 4], engine='calamine')[[
                    'SubNetwork', 'ManagedElement', 'ldn', 'userLabel', 'cellLocalId', 'duMeMoId', 'plmnIdList',
                    'ssbFrequency']]
                NRCellCU.rename(columns={'ldn': 'dn', 'duMeMoId': 'gNBId'}, inplace=True)
                NRCellDU = pd.read_excel(path, sheet_name='NRCellDU', skiprows=[1, 2, 3, 4], engine='calamine')[[
                    'ManagedElement', 'cellLocalId', 'tac', 'nRTAC', 'refNRPhysicalCellDU']]
                NRCellCU = NRCellCU.merge(NRCellDU, on=['ManagedElement', 'cellLocalId'], how='left')
                NRPhysicalCellDU = \
                    pd.read_excel(path, sheet_name='NRPhysicalCellDU', skiprows=[1, 2, 3, 4], engine='calamine')[[
                        'ManagedElement', 'ldn', 'refNRCarrier']]
                CellDefiningSSB = \
                    pd.read_excel(path, sheet_name='CellDefiningSSB', skiprows=[1, 2, 3, 4], engine='calamine')[[
                        'ManagedElement', 'ldn', 'pci']]
                CellDefiningSSB['ldn'] = CellDefiningSSB['ldn'].apply(lambda x: x.rsplit(',', 1)[0])
                NRPhysicalCellDU = NRPhysicalCellDU.merge(CellDefiningSSB, on=['ManagedElement', 'ldn'], how='left')
                NRCellCU = NRCellCU.merge(NRPhysicalCellDU, left_on=['ManagedElement', 'refNRPhysicalCellDU'],
                                          right_on=['ManagedElement', 'ldn'], how='left')
                del NRCellCU['ldn']
                CarrierUL = pd.read_excel(path, sheet_name='CarrierUL', skiprows=[1, 2, 3, 4], engine='calamine')[[
                    'ManagedElement', 'ldn', 'frequency', 'pointAfrequencyUL', 'nrbandwidth', 'frequencyBandList']]
                CarrierDL = pd.read_excel(path, sheet_name='CarrierDL', skiprows=[1, 2, 3, 4], engine='calamine')[[
                    'ManagedElement', 'ldn', 'frequency', 'pointAfrequencyDL', 'nrbandwidth', 'frequencyBandList']]
                CarrierUL['ldn'] = CarrierUL['ldn'].apply(lambda x: x.rsplit(',', 1)[0])
                CarrierDL['ldn'] = CarrierDL['ldn'].apply(lambda x: x.rsplit(',', 1)[0])
                NRCellCU = NRCellCU.merge(CarrierUL, left_on=['ManagedElement', 'refNRCarrier'],
                                          right_on=['ManagedElement', 'ldn'], how='left')
                del NRCellCU['ldn']
                NRCellCU = NRCellCU.merge(CarrierDL, left_on=['ManagedElement', 'refNRCarrier'],
                                          right_on=['ManagedElement', 'ldn'], how='left', suffixes=('_UL', '_DL'))
                del NRCellCU['ldn']
                del NRCellCU['refNRPhysicalCellDU']
                del NRCellCU['refNRCarrier']
                NRCellCU.to_sql('NRcell', conn, if_exists='append', index=False)
            except:
                print(traceback.format_exc())

        else:
            if 'EUtranCellTDD' in sheetnames:
                cell = pd.read_excel(path, sheet_name='EUtranCellTDD', skiprows=[1, 2, 3, 4], engine='calamine')[
                    ["SubNetwork", 'MOI', "MEID", "ENBFunctionTDD", "EUtranCellTDD", "userLabel", "cellLocalId",
                     "refPlmn",
                     "pci",
                     "tac", "bandIndicator", "earfcn", "bandWidth"]]
                cell.columns = [i.split('TDD')[0] for i in cell.columns]
                cell.rename(columns={'earfcn': 'earfcnDl', 'bandWidth': 'bandWidthDl', 'bandIndicator': 'freqBandInd'},
                            inplace=True)
                cell['earfcnUl'] = cell['earfcnDl']
                cell['bandWidthUl'] = cell['bandWidthDl']
                cell.to_sql('LTEcell', conn, if_exists='append', index=False)

            if 'EUtranCellFDD' in sheetnames:
                cell = pd.read_excel(path, sheet_name='EUtranCellFDD', skiprows=[1, 2, 3, 4], engine='calamine')[
                    ["SubNetwork", 'MOI', "MEID", "ENBFunctionFDD", "EUtranCellFDD", "userLabel", "cellLocalId",
                     "refPlmn",
                     "pci",
                     "tac", "freqBandInd", "earfcnUl", "earfcnDl", 'bandWidthDl', 'bandWidthUl']]
                cell.columns = [i.split('FDD')[0] for i in cell.columns]
                cell.to_sql('LTEcell', conn, if_exists='append', index=False)

            if 'EUtranCellFDDLTE' in sheetnames:
                cell = pd.read_excel(path, sheet_name='EUtranCellFDDLTE', skiprows=[1, 2, 3, 4], engine='calamine')[
                    ["SubNetwork", 'MOI', "MEID", "ENBFunction", "EUtranCellFDDLTE", "userLabel", "cellLocalId",
                     "refPlmn",
                     "pci",
                     "tac", "freqBandInd", "earfcnUl", "earfcnDl", 'bandWidthDl', 'bandWidthUl']]
                cell.columns = [i.split('FDD')[0] for i in cell.columns]
                cell.to_sql('LTEcell', conn, if_exists='append', index=False)

            if 'EUtranCellTDDLTE' in sheetnames:
                cell = pd.read_excel(path, sheet_name='EUtranCellTDDLTE', skiprows=[1, 2, 3, 4], engine='calamine')[
                    ["SubNetwork", 'MOI', "MEID", "ENBFunction", "EUtranCellTDDLTE", "userLabel", "cellLocalId",
                     "refPlmn",
                     "pci",
                     "tac", "bandIndicator", "earfcn", "bandWidth"]]
                cell.columns = [i.split('TDD')[0] for i in cell.columns]
                cell.rename(columns={'earfcn': 'earfcnDl', 'bandWidth': 'bandWidthDl', 'bandIndicator': 'freqBandInd'},
                            inplace=True)
                cell['earfcnUl'] = cell['earfcnDl']
                cell['bandWidthUl'] = cell['bandWidthDl']
                cell.to_sql('LTEcell', conn, if_exists='append', index=False)

            if 'CUEUtranCellTDDLTE' in sheetnames:
                cell = pd.read_excel(path, sheet_name='CUEUtranCellTDDLTE', skiprows=[1, 2, 3, 4], engine='calamine')[
                    ["SubNetwork", "ManagedElement", "ldn", "moId", "userLabel", "cellLocalId", "refPlmn", "pci",
                     "tac", "bandIndicator", "earfcn", "bandWidth"]]
                cell.rename(columns={'ManagedElement': 'MEID', 'moId': 'EUtranCell', 'ldn': 'MOI'}, inplace=True)
                cell['ENBFunction'] = cell['MOI'].apply(lambda x: x.split(',')[0].split('=')[-1].rsplit('_', 1)[-1])
                cell['ENBFunction'] = cell['ENBFunction'].apply(lambda x: str(x))
                cell['bandWidth'] = cell['bandWidth'].apply(lambda x: x.split('[')[-1].replace(']', ''))
                cell['bandWidth'] = cell['bandWidth'].apply(lambda x: str(x))

                cell.rename(columns={'earfcn': 'earfcnDl', 'bandWidth': 'bandWidthDl', 'bandIndicator': 'freqBandInd'},
                            inplace=True)
                cell['earfcnUl'] = cell['earfcnDl']
                cell['bandWidthUl'] = cell['bandWidthDl']
                cell.to_sql('LTEcell', conn, if_exists='append', index=False)

            if 'CUEUtranCellFDDLTE' in sheetnames:
                cell = pd.read_excel(path, sheet_name='CUEUtranCellFDDLTE', skiprows=[1, 2, 3, 4], engine='calamine')[
                    ["SubNetwork", "ManagedElement", "ldn", "moId", "userLabel", "cellLocalId", "refPlmn", "pci",
                     "tac", "freqBandInd", "earfcnUl", "earfcnDl", 'bandWidthDl', 'bandWidthUl']]
                cell.rename(columns={'ManagedElement': 'MEID', 'moId': 'EUtranCell', 'ldn': 'MOI'}, inplace=True)
                cell['ENBFunction'] = cell['MOI'].apply(lambda x: x.split(',')[0].split('=')[-1].rsplit('_', 1)[-1])
                cell['ENBFunction'] = cell['ENBFunction'].apply(lambda x: str(x))
                cell['bandWidthDl'] = cell['bandWidthDl'].apply(lambda x: x.split('[')[-1].replace(']', ''))
                cell['bandWidthUl'] = cell['bandWidthUl'].apply(lambda x: x.split('[')[-1].replace(']', ''))
                cell['bandWidthUl'] = cell['bandWidthUl'].apply(lambda x: str(x))
                cell['bandWidthDl'] = cell['bandWidthDl'].apply(lambda x: str(x))
                cell.to_sql('LTEcell', conn, if_exists='append', index=False)
        conn.close()
    except:
        mlogger.info(f'{traceback.format_exc()}')


def import_y_cell(path):
    mlogger.info(f'导入异厂家小区信息')
    try:
        conn = sqlite3.connect('cell_work.db')
        sheetnames = pd.ExcelFile(path).sheet_names
        if 'NRcell' in sheetnames:
            NRCellCU = pd.read_excel(path, sheet_name='NRcell', skiprows=[1, 2], engine='calamine')
            NRCellCU.to_sql('NRcell', conn, if_exists='append', index=False)

        if 'LTEcell' in sheetnames:
            cell = pd.read_excel(path, sheet_name='LTEcell', skiprows=[1, 2], engine='calamine')
            cell.to_sql('LTEcell', conn, if_exists='append', index=False)
        conn.close()
    except:
        mlogger.info(f'{traceback.format_exc()}')


class neighbor_check:
    def integration(self, work_name):
        conn1 = sqlite3.connect('cell_work.db')
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn1.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        for i in tab_name:
            df1 = pd.read_sql_query(f"SELECT * from {i}", conn1)
            df1.to_sql(i, conn2, if_exists='replace', index=False)
        conn1.close()
        conn2.close()

    def Consistency(self, work_name, output):
        mlogger.info(f'邻区一致性核查')
        self.integration(work_name)
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        for i in tab_name:
            if str(i).startswith('ExternalEUtran'):
                print(i, i)
                if i.__contains__('FDD') and work_name in ['icm', 'tmm']:
                    t1 = i
                    t2 = 'LTEcell'
                    # cu.execute('SELECT CAST(column_name AS VARCHAR(255)) FROM FDDcell;')
                    str1 = f"""SELECT {t1}.*,{t2}.pci,{t2}.tac,{t2}.freqBandInd,{t2}.earfcnUl,{t2}.earfcnDl,
    {t2}.bandWidthDl,{t2}.bandWidthUl
    FROM {t1} JOIN {t2} ON {t1}.eNBId = {t2}.ENBFunction 
    AND {t1}.cellLocalId = {t2}.cellLocalId
    WHERE {t1}.pci != {t2}.pci or {t1}.tac != {t2}.tac 
    or {t1}.freqBandInd != {t2}.freqBandInd or {t1}.earfcnUl != {t2}.earfcnUl or {t1}.earfcnDl != {t2}.earfcnDl 
    or {t1}.bandWidthDl != {t2}.bandWidthDl or {t1}.bandWidthUl != {t2}.bandWidthUl;"""
                    df1 = pd.read_sql_query(str1, conn2)
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-外部一致性.csv'), encoding='gbk', index=False)

                elif i.__contains__('TDD') and work_name in ['icm', 'tmm']:
                    t1 = i
                    t2 = 'LTEcell'
                    # cu.execute('SELECT CAST(column_name AS VARCHAR(255)) FROM FDDcell;')
                    str1 = f"""SELECT {t1}.*, {t2}.pci,{t2}.tac,{t2}.freqBandInd,{t2}.earfcnDl,{t2}.bandWidthDl
                        FROM {t1} JOIN {t2} ON {t1}.eNBId = {t2}.ENBFunction 
                        AND {t1}.cellLocalId = {t2}.cellLocalId
                        WHERE {t1}.pci != {t2}.pci or {t1}.tac != {t2}.tac 
                        or {t1}.freqBandInd != {t2}.freqBandInd or {t1}.earfcn != {t2}.earfcnDl
                        or {t1}.bandWidth != {t2}.bandWidthDl;"""
                    df1 = pd.read_sql_query(str1, conn2)
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-外部一致性.csv'), encoding='gbk', index=False)

                elif i.__contains__('TDD') and work_name == 'nr':
                    t1 = i
                    t2 = 'LTEcell'
                    # cu.execute('SELECT CAST(column_name AS VARCHAR(255)) FROM FDDcell;')
                    str1 = f"""SELECT {t1}.*, {t2}.pci,{t2}.tac,{t2}.freqBandInd,{t2}.earfcnDl,{t2}.bandWidthDl
                        FROM {t1} JOIN {t2} ON {t1}.eNBId = {t2}.ENBFunction 
                        AND {t1}.cellLocalId = {t2}.cellLocalId
                        WHERE {t1}.pci != {t2}.pci or {t1}.tac != {t2}.tac 
                        or {t1}.bandIndicator != {t2}.freqBandInd or {t1}.frequency != {t2}.earfcnDl
                        or {t1}.bandWidth != {t2}.bandWidthDl;"""
                    df1 = pd.read_sql_query(str1, conn2)
                    print(df1.shape)
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-外部一致性.csv'), encoding='gbk', index=False)

                elif i.__contains__('FDD') and work_name == 'nr':
                    t1 = i
                    t2 = 'LTEcell'
                    # cu.execute('SELECT CAST(column_name AS VARCHAR(255)) FROM FDDcell;')
                    str1 = f"""SELECT {t1}.*,{t2}.pci,{t2}.tac,{t2}.freqBandInd,{t2}.earfcnUl,{t2}.earfcnDl,
                        {t2}.bandWidthDl,{t2}.bandWidthUl
                        FROM {t1} JOIN {t2} ON {t1}.eNBId = {t2}.ENBFunction 
                        AND {t1}.cellLocalId = {t2}.cellLocalId
                        WHERE {t1}.pci != {t2}.pci or {t1}.tac != {t2}.tac 
                        or {t1}.bandIndicator != {t2}.freqBandInd or {t1}.frequencyUL != {t2}.earfcnUl or {t1}.frequencyDL != {t2}.earfcnDl 
                        or {t1}.ulBandWidth != {t2}.bandWidthDl or {t1}.dlBandWidth != {t2}.bandWidthUl;"""

                    df1 = pd.read_sql_query(str1, conn2)
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-外部一致性.csv'), encoding='gbk', index=False)
            elif str(i).startswith('ExternalNRCell'):
                t1 = i
                t2 = 'NRcell'
                str1 = f"""SELECT {t1}.*,{t2}.pci,{t2}.tac,{t2}.nRTAC,{t2}.frequency_UL,{t2}.nrbandwidth_UL,{t2}.frequencyBandList_UL,
                    {t2}.frequency_DL,{t2}.frequencyBandList_DL,{t2}.pointAfrequencyUL,{t2}.pointAfrequencyDL
                    FROM {t1} JOIN {t2} ON {t1}.gNBId = {t2}.gNBId 
                    AND {t1}.cellLocalId = {t2}.cellLocalId
                    WHERE {t1}.nRPCI != {t2}.pci or {t1}.tac != {t2}.tac or {t1}.nRTAC != {t2}.nRTAC
                    or {t1}.frequencyUL != {t2}.frequency_UL or {t1}.bandwidthUL != {t2}.nrbandwidth_UL or {t1}.freqBandListUL != {t2}.frequencyBandList_UL 
                    or {t1}.frequencyDL != {t2}.frequency_DL or {t1}.bandwidthDL != {t2}.nrbandwidth_DL or {t1}.freqBandListDL != {t2}.frequencyBandList_DL
                    or {t1}.pointAFrequencyUL != {t2}.pointAfrequencyUL or {t1}.pointAFrequencyDL != {t2}.pointAfrequencyDL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-外部一致性.csv'), encoding='gbk', index=False)

    def redundancy(self, work_name, output):
        mlogger.info(f'冗余外部核查')

        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        for i in tab_name:
            print(i)
            t1 = i
            if str(i).startswith('ExternalNRCell'):
                t2 = 'NRCellRelation'
                str1 = f"""SELECT {t1}.* FROM {t1} LEFT JOIN {t2} ON {t1}.ManagedElement = {t2}.ManagedElement and {t1}.ldn = {t2}.refExternalNRCellCU 
        WHERE {t2}.ManagedElement IS NULL and {t2}.refExternalNRCellCU IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
            elif str(i).startswith('ExternalEutranCellTDD') and work_name == 'nr':
                t2 = 'EutranCellRelation'
                str1 = f"""SELECT {t1}.* FROM {t1} LEFT JOIN {t2} ON {t1}.ManagedElement = {t2}.ManagedElement and {t1}.ldn = {t2}.refExternalEutranCellTDD
        WHERE {t2}.ManagedElement IS NULL and {t2}.refExternalEutranCellTDD IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
                # df1.to_excel(os.path.join(output, f'{work_name}-{i}-冗余外部.xlsx'), index=False)
            elif str(i).startswith('ExternalEutranCellFDD') and work_name == 'nr':
                t2 = 'EutranCellRelation'
                str1 = f"""SELECT {t1}.* FROM {t1} LEFT JOIN {t2} ON {t1}.ManagedElement = {t2}.ManagedElement and {t1}.ldn = {t2}.refExternalEutranCellFDD 
        WHERE {t2}.ManagedElement IS NULL and {t2}.refExternalEutranCellFDD IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
                # df1.to_excel(os.path.join(output, f'{work_name}-{i}-冗余外部.xlsx'), index=False)
            elif str(i).startswith('ExternalEUtranCellFDDLTE') and work_name == 'tmm':
                t2 = 'EUtranRelationTDDLTE'
                t3 = 'EUtranRelationFDDLTE'
                str1 = f"""SELECT {t1}.* FROM {t1} 
                        LEFT JOIN {t2} ON {t1}.ManagedElement = {t2}.ManagedElement and {t1}.ldn = {t2}.refExternalEUtranCellFDDLTE
                        LEFT JOIN {t3} ON {t1}.ManagedElement = {t3}.ManagedElement and {t1}.ldn = {t3}.refExternalEUtranCellFDDLTE
                        WHERE {t2}.ManagedElement IS NULL and {t2}.refExternalEUtranCellFDDLTE IS NULL and {t3}.ManagedElement IS NULL and {t3}.refExternalEUtranCellFDDLTE IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)

            elif str(i).startswith('ExternalEUtranCellTDDLTE') and work_name == 'tmm':
                t2 = 'EUtranRelationTDDLTE'
                t3 = 'EUtranRelationFDDLTE'
                str1 = f"""SELECT {t1}.* FROM {t1} 
        LEFT JOIN {t2} ON {t1}.ManagedElement = {t2}.ManagedElement and {t1}.ldn = {t2}.refExternalEUtranCellTDDLTE
        LEFT JOIN {t3} ON {t1}.ManagedElement = {t3}.ManagedElement and {t1}.ldn = {t3}.refExternalEUtranCellTDDLTE 
        WHERE {t2}.ManagedElement IS NULL and {t2}.refExternalEUtranCellTDDLTE IS NULL and {t3}.ManagedElement IS NULL and {t3}.refExternalEUtranCellTDDLTE IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)

            elif str(i).startswith('ExternalEUtranCellTDDLTE') and work_name == 'icm':
                t2 = 'EUtranRelationTDDLTE'
                t3 = 'EUtranRelationFDDLTE'
                str1 = f"""SELECT {t1}.* FROM {t1} 
                    LEFT JOIN {t2} ON {t1}.MOI = {t2}.refExternalEUtranCellTDDLTE
                    LEFT JOIN {t3} ON {t1}.MOI = {t3}.refExternalEUtranCellTDDLTE 
                    WHERE {t2}.refExternalEUtranCellTDDLTE IS NULL and {t3}.refExternalEUtranCellTDDLTE IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
            elif str(i).startswith('ExternalEUtranCellFDDLTE') and work_name == 'icm':
                t2 = 'EUtranRelationTDDLTE'
                t3 = 'EUtranRelationFDDLTE'
                str1 = f"""SELECT {t1}.* FROM {t1} 
                        LEFT JOIN {t2} ON {t1}.MOI = {t2}.refExternalEUtranCellFDDLTE
                        LEFT JOIN {t3} ON {t1}.MOI = {t3}.refExternalEUtranCellFDDLTE 
                        WHERE {t2}.refExternalEUtranCellFDDLTE IS NULL and {t3}.refExternalEUtranCellFDDLTE IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
            elif str(i).startswith('ExternalEUtranTCellFDD') and work_name == 'icm':
                t2 = 'EUtranRelationTDD'
                str1 = f"""SELECT {t1}.* FROM {t1} 
                        LEFT JOIN {t2} ON {t1}.MOI = {t2}.refExternalEUtranTCellFDD
                        WHERE {t2}.refExternalEUtranTCellFDD IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
            elif str(i).startswith('ExternalEUtranTCellTDD') and work_name == 'icm':
                t2 = 'EUtranRelationTDD'
                str1 = f"""SELECT {t1}.* FROM {t1} 
                        LEFT JOIN {t2} ON {t1}.MOI = {t2}.refExternalEUtranTCellTDD
                        WHERE {t2}.refExternalEUtranTCellTDD IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
            elif str(i).startswith('ExternalEUtranCellFDD') and work_name == 'icm':
                t2 = 'EUtranRelation'
                str1 = f"""SELECT {t1}.* FROM {t1} 
                        LEFT JOIN {t2} ON {t1}.MOI = {t2}.refExternalEUtranCellFDD
                        WHERE {t2}.refExternalEUtranCellFDD IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)
            elif str(i).startswith('ExternalEUtranCellTDD') and work_name == 'icm':
                t2 = 'EUtranRelation'
                str1 = f"""SELECT {t1}.* FROM {t1} 
                            LEFT JOIN {t2} ON {t1}.MOI = {t2}.refExternalEUtranCellTDD
                            WHERE {t2}.refExternalEUtranCellTDD IS NULL;"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余外部.csv'), encoding='gbk', index=False)

    def nei_num(self, work_name, output, ):
        mlogger.info(f'邻区数量核查')
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        for i in tab_name:
            if work_name == 'nr' and 'NRCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col('NRCellRelation', 'dn')
                my_sqlite1.split('ldn', 'NRCellRelation')
                my_sqlite1.combined_column('NRCellRelation', 'dn_id', 'ManagedElement', 'dn', ',')
                # conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')

                str1 = 'SELECT dn_id, COUNT(*) AS count FROM NRCellRelation GROUP BY dn_id;'
                df1 = pd.read_sql_query(str1, conn2)
                my_sqlite1.delete_col('NRCellRelation', 'dn_id')
                my_sqlite1.delete_col('NRCellRelation', 'dn')
                df1.to_csv(os.path.join(output, f'{work_name}-NRCellRelation-邻区数量.csv'), encoding='gbk', index=False)
            elif work_name == 'nr' and 'EutranCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.split('ldn', 'EutranCellRelation')
                my_sqlite1.combined_column('EutranCellRelation', 'dn_id', 'ManagedElement', 'dn', ',')
                # conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')

                str1 = 'SELECT dn_id, COUNT(*) AS count FROM EutranCellRelation GROUP BY dn_id;'
                df1 = pd.read_sql_query(str1, conn2)
                my_sqlite1.delete_col('EutranCellRelation', 'dn_id')
                my_sqlite1.delete_col('EutranCellRelation', 'dn')
                df1.to_csv(os.path.join(output, f'{work_name}-EutranCellRelation-邻区数量.csv'), encoding='gbk',
                           index=False)

            elif work_name == 'tmm' and ('EUtranRelationTDDLTE' == i or 'EUtranRelationFDDLTE' == i):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.split('ldn', i)
                my_sqlite1.combined_column(i, 'dn_id', 'ManagedElement', 'dn', ',')
                # conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')

                str1 = f'SELECT dn_id, COUNT(*) AS count FROM {i} GROUP BY dn_id;'
                df1 = pd.read_sql_query(str1, conn2)
                my_sqlite1.delete_col(i, 'dn_id')
                my_sqlite1.delete_col(i, 'dn')
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区数量.csv'), encoding='gbk', index=False)
            elif work_name == 'icm' and i.__contains__('EUtranRelation'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.split('MOI', i)
                # my_sqlite1.combined_column(i, 'dn_id', 'ManagedElement', 'dn', ',')
                # conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')

                str1 = f'SELECT dn, COUNT(*) AS count FROM {i} GROUP BY dn;'
                df1 = pd.read_sql_query(str1, conn2)
                my_sqlite1.delete_col(i, 'dn')
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区数量.csv'), encoding='gbk', index=False)

            # conn2.create_function("SPLIT", 1, split_func)
            # cur = conn2.cursor()
            # cur.execute(f"ALTER TABLE {tab} ADD COLUMN dn TEXT")
            # # cur.execute(f"UPDATE {tab} SET dn = CONCAT(ManagedElement)")
            # cur.execute(f"UPDATE {tab} SET dn = ManagedElement||','|| SPLIT(ldn)")
            # # cur.execute(f"SELECT SPLIT({col}) FROM {tab}")
            # conn2.commit()
            # # conn2.close()

    def nei_duo(self, work_name, output, limit):
        mlogger.info(f'邻区超限核查')
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        for i in tab_name:
            if work_name == 'nr' and ('NRCellRelation' == i or 'EutranCellRelation' == i):

                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.split('ldn', i)
                my_sqlite1.combined_column(i, 'dn_id', 'ManagedElement', 'dn', ',')

                cu.execute(f'CREATE TABLE F AS SELECT dn_id,COUNT(*) AS COUNT FROM {i} GROUP BY dn_id;')
                conn2.commit()
                str1 = f"""SELECT {i}.*,F.COUNT FROM {i} LEFT JOIN F ON {i}.dn_id = F.dn_id WHERE F.COUNT > {limit};"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区数量>{limit}.csv'), encoding='gbk',
                           index=False)
                my_sqlite1.drop_tab('F')
                my_sqlite1.delete_col(i, 'dn_id')
                my_sqlite1.delete_col(i, 'dn')

            elif work_name == 'tmm' and ('EUtranRelationTDDLTE' == i or 'EUtranRelationFDDLTE' == i):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.split('ldn', i)
                my_sqlite1.combined_column(i, 'dn_id', 'ManagedElement', 'dn', ',')
                # conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')

                cu.execute(f'CREATE TABLE F AS SELECT dn_id,COUNT(*) AS COUNT FROM {i} GROUP BY dn_id;')
                conn2.commit()
                str1 = f"""SELECT {i}.*,F.COUNT FROM {i} LEFT JOIN F ON {i}.dn_id = F.dn_id WHERE F.COUNT > {limit};"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区数量>{limit}.csv'), encoding='gbk',
                           index=False)
                my_sqlite1.drop_tab('F')
                my_sqlite1.delete_col(i, 'dn_id')
                my_sqlite1.delete_col(i, 'dn')
            elif work_name == 'icm' and i.__contains__('EUtranRelation'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.split('MOI', i)
                # my_sqlite1.combined_column(i, 'dn_id', 'ManagedElement', 'dn', ',')
                # conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')

                cu.execute(f'CREATE TABLE F AS SELECT dn,COUNT(*) AS COUNT FROM {i} GROUP BY dn;')
                conn2.commit()
                str1 = f"""SELECT {i}.*,F.COUNT FROM {i} LEFT JOIN F ON {i}.dn = F.dn WHERE F.COUNT > {limit};"""
                df1 = pd.read_sql_query(str1, conn2)
                df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区数量>{limit}.csv'), encoding='gbk',
                           index=False)
                my_sqlite1.drop_tab('F')
                my_sqlite1.delete_col(i, 'dn')

    def pci_Conflict(self, work_name, output, ):
        mlogger.info(f'PCI冲突核查')
        self.integration(work_name)
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        print(tab_name)
        for i in tab_name:
            if work_name == 'nr' and 'NRCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('ldn', i)
                t2 = 'NRcell'
                t3 = 'ExternalNRCellCU'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,{i}.ldn,{i}.moId,
IFNULL(S.gNBId,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.frequency_DL as S_earfcn,S.pci as S_pci,
IFNULL(NT.gNBId,'')||IFNULL({t3}.gNBId,'')||'-'||IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'') as N_CI,
IFNULL(NT.frequency_DL,'')||IFNULL({t3}.frequencyDL,'') as N_earfcn,
IFNULL(NT.pci,'')||IFNULL({t3}.nRPCI,'') as N_pci FROM {i} 
LEFT JOIN {t2} as S ON {i}.ManagedElement = S.ManagedElement and {i}.dn = S.dn
LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.ManagedElement and {i}.refNRCellCU = NT.dn
LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalNRCellCU = {t3}.ldn
WHERE S_earfcn=N_earfcn and S_pci=N_pci;
"""
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果为0')

            elif work_name == 'tmm' and i.__contains__('EUtranRelation'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split2('ldn', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,{i}.MO_Description,{i}.ldn,{i}.moId,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
IFNULL(NT.pci,'')||IFNULL(NF.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
LEFT JOIN {t2} as S ON {i}.ManagedElement = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.MEID and {i}.refCUEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.ManagedElement = NF.MEID and {i}.refCUEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalEUtranCellTDDLTE = {t3}.ldn
LEFT JOIN {t4} ON {i}.ManagedElement = {t4}.ManagedElement and  {i}.refExternalEUtranCellFDDLTE = {t4}.ldn
WHERE S_earfcn=N_earfcn and S_pci=N_pci;
"""
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果为0')

            elif work_name == 'icm' and i.__contains__('EUtranRelation') and i.endswith('LTE'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunction,{i}.description,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
IFNULL(NT.pci,'')||IFNULL(NF.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.MEID = NF.MEID and {i}.refEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDDLTE = {t3}.MOI
LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDDLTE = {t4}.MOI
WHERE S_earfcn=N_earfcn and S_pci=N_pci;
"""
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelationTDD':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellTDD'
                t3 = 'ExternalEUtranTCellTDD'
                t4 = 'ExternalEUtranTCellFDD'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunctionTDD,{i}.description,
                IFNULL(S.ENBFunctionTDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcn as S_earfcn,S.pci as S_pci,
                IFNULL(NT.ENBFunctionTDD,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI,
                IFNULL(NT.earfcn,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranTCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranTCellFDD = {t4}.MOI
                WHERE S_earfcn=N_earfcn and S_pci=N_pci;
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelation':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellFDD'
                t3 = 'ExternalEUtranCellTDD'
                t4 = 'ExternalEUtranCellFDD'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunctionFDD,{i}.description,
                IFNULL(S.ENBFunctionFDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
                IFNULL(NT.ENBFunctionFDD,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI,
                IFNULL(NT.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellFDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDD = {t4}.MOI
                WHERE S_earfcn=N_earfcn and S_pci=N_pci;
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果为0')

    def pci_Confusion(self, work_name, output, ):
        mlogger.info(f'PCI混淆核查')
        self.integration(work_name)
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        print(tab_name)
        for i in tab_name:
            if work_name == 'nr' and 'NRCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('ldn', i)
                t2 = 'NRcell'
                t3 = 'ExternalNRCellCU'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,{i}.ldn,{i}.moId,
                IFNULL(S.gNBId,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.frequency_DL as S_earfcn,S.pci as S_pci,
                IFNULL(NT.gNBId,'')||IFNULL({t3}.gNBId,'')||'-'||IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'') as N_CI,
                IFNULL(NT.frequency_DL,'')||IFNULL({t3}.frequencyDL,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.nRPCI,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.ManagedElement = S.ManagedElement and {i}.dn = S.dn
                LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.ManagedElement and {i}.refNRCellCU = NT.dn
                LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalNRCellCU = {t3}.ldn;
                """
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates()
                df_counts = df1.pivot_table(index=['S_CI', 'N_earfcn', 'N_pci'], values=['ldn'],
                                            aggfunc='count').reset_index()
                df_counts.columns = ['S_CI', 'N_earfcn', 'N_pci', 'count']
                df1 = df1.merge(df_counts, on=['S_CI', 'N_earfcn', 'N_pci'], how='left')
                df1 = df1[df1['count'] > 1]
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI混淆.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI混淆核查结果为0')

            elif work_name == 'tmm' and i.__contains__('EUtranRelation'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split2('ldn', i)
                my_sqlite1.drop_tab('F')

                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,{i}.MO_Description,{i}.ldn,{i}.moId,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'') ||'-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
IFNULL(NT.pci,'')||IFNULL(NF.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
LEFT JOIN {t2} as S ON {i}.ManagedElement = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.MEID and {i}.refCUEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.ManagedElement = NF.MEID and {i}.refCUEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalEUtranCellTDDLTE = {t3}.ldn
LEFT JOIN {t4} ON {i}.ManagedElement = {t4}.ManagedElement and  {i}.refExternalEUtranCellFDDLTE = {t4}.ldn
;"""

                df1 = pd.read_sql_query(str1, conn2).drop_duplicates()
                df_counts = df1.pivot_table(index=['S_CI', 'N_earfcn', 'N_pci'], values=['ldn'],
                                            aggfunc='count').reset_index()
                df_counts.columns = ['S_CI', 'N_earfcn', 'N_pci', 'count']
                df1 = df1.merge(df_counts, on=['S_CI', 'N_earfcn', 'N_pci'], how='left')
                df1 = df1[df1['count'] > 1]
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI混淆.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI混淆核查结果路径为：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI混淆核查结果为0')

            elif work_name == 'icm' and i.__contains__('EUtranRelation') and i.endswith('LTE'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunction,{i}.description,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
IFNULL(NT.pci,'')||IFNULL(NF.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.MEID = NF.MEID and {i}.refEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDDLTE = {t3}.MOI
LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDDLTE = {t4}.MOI;
"""
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates()
                df_counts = df1.pivot_table(index=['S_CI', 'N_earfcn', 'N_pci'], values=['MOI'],
                                            aggfunc='count').reset_index()
                df_counts.columns = ['S_CI', 'N_earfcn', 'N_pci', 'count']
                df1 = df1.merge(df_counts, on=['S_CI', 'N_earfcn', 'N_pci'], how='left')
                df1 = df1[df1['count'] > 1]
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI混淆.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI混淆核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelationTDD':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellTDD'
                t3 = 'ExternalEUtranTCellTDD'
                t4 = 'ExternalEUtranTCellFDD'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunctionTDD,{i}.description,
                IFNULL(S.ENBFunctionTDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcn as S_earfcn,S.pci as S_pci,
                IFNULL(NT.ENBFunctionTDD,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI,
                IFNULL(NT.earfcn,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranTCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranTCellFDD = {t4}.MOI;
                """
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates()

                df_counts = df1.pivot_table(index=['S_CI', 'N_earfcn', 'N_pci'], values=['MOI'],
                                            aggfunc='count').reset_index()
                df_counts.columns = ['S_CI', 'N_earfcn', 'N_pci', 'count']
                df1 = df1.merge(df_counts, on=['S_CI', 'N_earfcn', 'N_pci'], how='left')
                df1 = df1[df1['count'] > 1]
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI混淆.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI混淆核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelation':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellFDD'
                t3 = 'ExternalEUtranCellTDD'
                t4 = 'ExternalEUtranCellFDD'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunctionFDD,{i}.description,
                IFNULL(S.ENBFunctionFDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
                IFNULL(NT.ENBFunctionFDD,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI,
                IFNULL(NT.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellFDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDD = {t4}.MOI;
                """
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates()

                df_counts = df1.pivot_table(index=['S_CI', 'N_earfcn', 'N_pci'], values=['MOI'],
                                            aggfunc='count').reset_index()
                df_counts.columns = ['S_CI', 'N_earfcn', 'N_pci', 'count']
                df1 = df1.merge(df_counts, on=['S_CI', 'N_earfcn', 'N_pci'], how='left')
                df1 = df1[df1['count'] > 1]
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-PCI混淆.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}PCI冲突核查结果路径为：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}PCI混淆核查结果为0')

    def earfcn(self, work_name, output, ):
        mlogger.info(f'邻区频点核查')
        # self.integration(work_name)
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        print(tab_name)
        for i in tab_name:
            if work_name == 'nr' and 'NRCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('ldn', i)
                t2 = 'NRcell'
                t3 = 'ExternalNRCellCU'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,{i}.ldn,{i}.moId,
                IFNULL(S.gNBId,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.frequency_DL as S_earfcn,S.pci as S_pci,
                IFNULL(NT.gNBId,'')||IFNULL({t3}.gNBId,'')||'-'||IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'') as N_CI,
                IFNULL(NT.frequency_DL,'')||IFNULL({t3}.frequencyDL,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.pci,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.ManagedElement = S.ManagedElement and {i}.dn = S.ldn
                LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.ManagedElement and {i}.refNRCellCU = NT.ldn
                LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalNRCellCU = {t3}.ldn
                WHERE S_earfcn!=N_earfcn;
                """
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates(subset=['S_CI', 'N_earfcn'])
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区频点核查.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}P邻区频点核查：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}邻区频点核查0')

            elif work_name == 'tmm' and i.__contains__('EUtranRelation'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split2('ldn', i)
                my_sqlite1.drop_tab('F')

                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn FROM {i}
LEFT JOIN {t2} as S ON {i}.ManagedElement = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.MEID and {i}.refCUEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.ManagedElement = NF.MEID and {i}.refCUEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalEUtranCellTDDLTE = {t3}.ldn
LEFT JOIN {t4} ON {i}.ManagedElement = {t4}.ManagedElement and  {i}.refExternalEUtranCellFDDLTE = {t4}.ldn
WHERE S_earfcn!=N_earfcn;"""

                df1 = pd.read_sql_query(str1, conn2).drop_duplicates(subset=['S_CI', 'N_earfcn'])

                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区频点核查.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}P邻区频点核查：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}邻区频点核查0')

            elif work_name == 'icm' and i.__contains__('EUtranRelation') and i.endswith('LTE'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.SubNetwork,{i}.MEID,{i}.ENBFunction,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn FROM {i} 
LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.MEID = NF.MEID and {i}.refEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDDLTE = {t3}.MOI
LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDDLTE = {t4}.MOI
WHERE S_earfcn!=N_earfcn;
"""
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates(subset=['S_CI', 'N_earfcn'])
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区频点核查.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}P邻区频点核查：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}邻区频点核查0')
            elif work_name == 'icm' and i == 'EUtranRelationTDD':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellTDD'
                t3 = 'ExternalEUtranTCellTDD'
                t4 = 'ExternalEUtranTCellFDD'
                str1 = f"""SELECT {i}.SubNetwork,{i}.MEID,{i}.ENBFunctionTDD,
                IFNULL(S.ENBFunctionTDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcn as S_earfcn,S.pci as S_pci,
                IFNULL(NT.earfcn,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranTCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranTCellFDD = {t4}.MOI
                WHERE S_earfcn!=N_earfcn;
                """
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates(subset=['S_CI', 'N_earfcn'])
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区频点核查.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}P邻区频点核查：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}邻区频点核查0')
            elif work_name == 'icm' and i == 'EUtranRelation':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellFDD'
                t3 = 'ExternalEUtranCellTDD'
                t4 = 'ExternalEUtranCellFDD'
                str1 = f"""{i}.SubNetwork,{i}.MEID,{i}.ENBFunctionFDD,
                IFNULL(S.ENBFunctionFDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
                IFNULL(NT.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellFDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDD = {t4}.MOI
                WHERE S_earfcn!=N_earfcn;
                """
                df1 = pd.read_sql_query(str1, conn2).drop_duplicates(subset=['S_CI', 'N_earfcn'])
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-邻区频点核查.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}P邻区频点核查：output/{work_name}-{i}-PCI混淆.csv')
                else:
                    mlogger.info(f'{work_name}{i}邻区频点核查0')

    def m3_Conflict(self, work_name, output, ):
        mlogger.info(f'M3冲突核查')
        self.integration(work_name)
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        print(tab_name)
        for i in tab_name:
            if work_name == 'nr' and 'NRCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('ldn', i)
                t2 = 'NRcell'
                t3 = 'ExternalNRCellCU'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,{i}.ldn,{i}.moId,
                IFNULL(S.gNBId,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.frequency_DL as S_earfcn,S.pci as S_pci,
                IFNULL(NT.gNBId,'')||IFNULL({t3}.gNBId,'')||'-'||IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'') as N_CI,
                IFNULL(NT.frequency_DL,'')||IFNULL({t3}.frequencyDL,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.nRPCI,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.ManagedElement = S.ManagedElement and {i}.dn = S.dn
                LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.ManagedElement and {i}.refNRCellCU = NT.dn
                LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalNRCellCU = {t3}.ldn
                WHERE S_earfcn=N_earfcn and S_pci%3=N_pci%3;
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-M3.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}M3冲突核查结果路径为：output/{work_name}-{i}-M3.csv')
                else:
                    mlogger.info(f'{work_name}{i}M3冲突核查结果为0')

            elif work_name == 'tmm' and i.__contains__('EUtranRelation'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split2('ldn', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.SubNetwork,{i}.ManagedElement,{i}.NE_Name,{i}.MO_Description,{i}.ldn,{i}.moId,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
IFNULL(NT.pci,'')||IFNULL(NF.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
LEFT JOIN {t2} as S ON {i}.ManagedElement = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.MEID and {i}.refCUEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.ManagedElement = NF.MEID and {i}.refCUEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalEUtranCellTDDLTE = {t3}.ldn
LEFT JOIN {t4} ON {i}.ManagedElement = {t4}.ManagedElement and  {i}.refExternalEUtranCellFDDLTE = {t4}.ldn
WHERE S_earfcn=N_earfcn and S_pci%3=N_pci%3;
"""
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-M3.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}M3冲突核查结果路径为：output/{work_name}-{i}-M3.csv')
                else:
                    mlogger.info(f'{work_name}{i}M3冲突核查结果为0')

            elif work_name == 'icm' and i.__contains__('EUtranRelation') and i.endswith('LTE'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunction,{i}.description,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI,
IFNULL(NT.earfcnDl,'')||IFNULL(NF.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
IFNULL(NT.pci,'')||IFNULL(NF.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.MEID = NF.MEID and {i}.refEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDDLTE = {t3}.MOI
LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDDLTE = {t4}.MOI
WHERE S_earfcn=N_earfcn and S_pci%3=N_pci%3;
"""
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-M3.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}M3冲突核查结果路径为：output/{work_name}-{i}-M3.csv')
                else:
                    mlogger.info(f'{work_name}{i}M3冲突核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelationTDD':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellTDD'
                t3 = 'ExternalEUtranTCellTDD'
                t4 = 'ExternalEUtranTCellFDD'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunctionTDD,{i}.description,
                IFNULL(S.ENBFunctionTDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcn as S_earfcn,S.pci as S_pci,
                IFNULL(NT.ENBFunctionTDD,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI,
                IFNULL(NT.earfcn,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranTCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranTCellFDD = {t4}.MOI
                WHERE S_earfcn=N_earfcn and S_pci%3=N_pci%3;
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-M3.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}M3冲突核查结果路径为：output/{work_name}-{i}-M3.csv')
                else:
                    mlogger.info(f'{work_name}{i}M3冲突核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelation':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'EUtranCellFDD'
                t3 = 'ExternalEUtranCellTDD'
                t4 = 'ExternalEUtranCellFDD'
                str1 = f"""SELECT {i}.MOI,{i}.SubNetwork,{i}.MEID,{i}.ENBFunctionFDD,{i}.description,
                IFNULL(S.ENBFunctionFDD,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,S.earfcnDl as S_earfcn,S.pci as S_pci,
                IFNULL(NT.ENBFunctionFDD,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI,
                IFNULL(NT.earfcnDl,'')||IFNULL({t3}.earfcn,'')||IFNULL({t4}.earfcnDl,'') as N_earfcn,
                IFNULL(NT.pci,'')||IFNULL({t3}.pci,'')||IFNULL({t4}.pci,'') as N_pci FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellFDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDD = {t4}.MOI
                WHERE S_earfcn=N_earfcn and S_pci%3=N_pci%3;
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-M3.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}M3冲突核查结果路径为：output/{work_name}-{i}-M3.csv')
                else:
                    mlogger.info(f'{work_name}{i}M3冲突核查结果为0')

    def nei_redundance(self, work_name, output):
        mlogger.info(f'冗余邻区')
        self.integration(work_name)
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        print(tab_name)
        for i in tab_name:
            if work_name == 'nr' and 'NRCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('ldn', i)
                t2 = 'NRcell'
                t3 = 'ExternalNRCellCU'
                str1 = f"""SELECT {i}.*,
                IFNULL(S.gNBId,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,
                IFNULL(NT.gNBId,'')||IFNULL({t3}.gNBId,'')||'-'||IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'') 
                as N_CI FROM {i} 
                LEFT JOIN {t2} as S ON {i}.ManagedElement = S.ManagedElement and {i}.dn = S.dn
                LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.ManagedElement and {i}.refNRCellCU = NT.dn
                LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and {i}.refExternalNRCellCU = {t3}.ldn
                WHERE N_CI NOT IN (SELECT IFNULL({t2}.gNBId,'')||'-'||IFNULL({t2}.cellLocalId,'') as CI FROM {t2});
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    del df1['dn']
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-M3.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}冗余邻区：output/{work_name}-{i}-冗余邻区.csv')
                else:
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果为0')

            elif work_name == 'tmm' and i.__contains__('EUtranRelation'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split2('ldn', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.*,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI 
FROM {i} 
LEFT JOIN {t2} as S ON {i}.ManagedElement = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.ManagedElement = NT.MEID and {i}.refCUEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.ManagedElement = NF.MEID and {i}.refCUEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.ManagedElement = {t3}.ManagedElement and  {i}.refExternalEUtranCellTDDLTE = {t3}.ldn
LEFT JOIN {t4} ON {i}.ManagedElement = {t4}.ManagedElement and  {i}.refExternalEUtranCellFDDLTE = {t4}.ldn
WHERE N_CI NOT IN (SELECT IFNULL({t2}.ENBFunction,'')||'-'||IFNULL({t2}.cellLocalId,'') as CI FROM {t2});
"""
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    del df1['dn']
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余邻区.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果路径为：output/{work_name}-{i}-冗余邻区.csv')
                else:
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果为0')

            elif work_name == 'icm' and i.__contains__('EUtranRelation') and i.endswith('LTE'):
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDDLTE'
                t4 = 'ExternalEUtranCellFDDLTE'
                str1 = f"""SELECT {i}.*,
IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,
IFNULL(NT.ENBFunction,'')||IFNULL(NF.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
IFNULL(NT.cellLocalId,'')||IFNULL(NF.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'') as N_CI 
FROM {i} 
LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDDLTE = NT.MOI
LEFT JOIN {t2} as NF ON {i}.MEID = NF.MEID and {i}.refEUtranCellFDDLTE = NF.MOI
LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDDLTE = {t3}.MOI
LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDDLTE = {t4}.MOI
WHERE N_CI NOT IN (SELECT IFNULL({t2}.ENBFunction,'')||'-'||IFNULL({t2}.cellLocalId,'') as CI FROM {t2});
"""
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    del df1['dn']
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余邻区.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}冗余邻区查结果路径为：output/{work_name}-{i}-冗余邻区.csv')
                else:
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelationTDD':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranTCellTDD'
                t4 = 'ExternalEUtranTCellFDD'
                str1 = f"""SELECT {i}.*,
                IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,
                IFNULL(NT.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI
                FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellTDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranTCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranTCellFDD = {t4}.MOI
                WHERE N_CI NOT IN (SELECT IFNULL({t2}.ENBFunction,'')||'-'||IFNULL({t2}.cellLocalId,'') as CI FROM {t2});
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    del df1['dn']
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余邻区.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果路径为：output/{work_name}-{i}-冗余邻区.csv')
                else:
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果为0')
            elif work_name == 'icm' and i == 'EUtranRelation':
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('MOI', i)
                t2 = 'LTEcell'
                t3 = 'ExternalEUtranCellTDD'
                t4 = 'ExternalEUtranCellFDD'
                str1 = f"""SELECT {i}.*,
                IFNULL(S.ENBFunction,'')||'-'||IFNULL(S.cellLocalId,'') as S_CI,
                IFNULL(NT.ENBFunction,'')||IFNULL({t3}.eNBId,'')||IFNULL({t4}.eNBId,'')||'-'||
                IFNULL(NT.cellLocalId,'')||IFNULL({t3}.cellLocalId,'')||IFNULL({t4}.cellLocalId,'')  as N_CI
                FROM {i} 
                LEFT JOIN {t2} as S ON {i}.MEID = S.MEID and {i}.dn = S.MOI
                LEFT JOIN {t2} as NT ON {i}.MEID = NT.MEID and {i}.refEUtranCellFDD = NT.MOI
                LEFT JOIN {t3} ON {i}.MEID = {t3}.MEID and  {i}.refExternalEUtranCellTDD = {t3}.MOI
                LEFT JOIN {t4} ON {i}.MEID = {t4}.MEID and  {i}.refExternalEUtranCellFDD = {t4}.MOI
                WHERE N_CI NOT IN (SELECT IFNULL({t2}.ENBFunction,'')||'-'||IFNULL({t2}.cellLocalId,'') as CI FROM {t2});
                """
                df1 = pd.read_sql_query(str1, conn2)
                if df1.shape[0] > 0:
                    del df1['dn']
                    df1.to_csv(os.path.join(output, f'{work_name}-{i}-冗余邻区.csv'), encoding='gbk',
                               index=False)
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果路径为：output/{work_name}-{i}-冗余邻区.csv')
                else:
                    mlogger.info(f'{work_name}{i}冗余邻区核查结果为0')

    def delete(self, work_name, output):
        mlogger.info(f'退网小区邻区外部删除')
        self.integration(work_name)
        conn2 = sqlite3.connect(f'{work_name}_neighbor_work.db')
        cu = conn2.cursor()
        cu.execute("select name from sqlite_master where type='table'")
        tab_name = cu.fetchall()
        tab_name = [line[0] for line in tab_name]
        print(tab_name)
        for i in tab_name:
            if work_name == 'nr' and 'NRCellRelation' == i:
                my_sqlite1 = my_sqlite(f'{work_name}_neighbor_work.db')
                my_sqlite1.delete_col(i, 'dn')
                my_sqlite1.split('ldn', i)


if __name__ == '__main__':
    # 导入4G小区信息
    # my_sqlite = my_sqlite('tmm_neighbor_work.db')
    # my_sqlite.clear_database()
    # for i in os.listdir(r'E:\Desktop\新建文件夹\nei'):
    #     if i.endswith(".xlsx"):
    #         f = os.path.join(r'E:\Desktop\新建文件夹\nei', i)
    #         # print(f)
    #         # import_cell(f)
    #         if i.startswith('RANCM'):
    #             import_neighbor(f, 'tmm', dic['tmm'])
    # else:
    #     import_neighbor(f, 'icm', dic['icm'])
    import_cell("111.xlsx")
    # 导入4G小区信息
    # conn = sqlite3.connect('cell_work.db')
    # df1 = pd.read_sql_query("SELECT * from LTEcell", conn)
    # print(df1.shape)
    # df1.to_excel('LTE.xlsx')
    #
    # a = neighbor_check()
    # a.pci_Conflict('tmm', '')
    # a.m3_Conflict('tmm', '')
    # a.earfcn('tmm', '')
    # a.earfcn('icm', '')
    # a.Consistency('icm', '')
    # a.Consistency('tmm', '')
    # a.Consistency('nr', '')
    # a.pci_Confusion('icm', '')
    # a.pci_Confusion('tmm', '')
    # a.nei_duo('tmm', '', 180)

    # my_sqlite1 = my_sqlite('tmm_neighbor_work.db')
    # my_sqlite1.clear_database()

    # conn = sqlite3.connect('cell_work.db')
    # df1 = pd.read_sql_query("SELECT * from LTEcell;", conn)
    # print(df1.shape)
    # df1.to_csv('LTEcell.csv',encoding='gbk')
    # print(1)
