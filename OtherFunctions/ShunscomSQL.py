import pandas as pd
import pymysql


class ShunscomToolSql:
    def __init__(self):
        self.sql = pymysql.connect(
            host='114.67.174.212',
            user='shunscomtool',
            password='Wangxinyue1994@Zdy',
            port=3306,
            db='shunscomtool',
            charset='utf8'
        )

    def query_sql(self, sql):
        cursor = self.sql.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()

    def write_sql(self, sql):
        cursor = self.sql.cursor()
        cursor.execute(sql)
        self.sql.commit()


if __name__ == '__main__':
    p = r'E:\Desktop\人员.xlsx'
    df = pd.read_excel(p)

    conn = ShunscomToolSql()

    for idx, row in df.iterrows():
        username, name, region = (
            row["公司邮箱"],
            row["OA姓名"],
            row["区域"],
        )
        print(username, name, region)
        sqlInsert = f"""
                            insert into emailusers
                           (username,name,region)
                           values
                           ('{username}','{name}','{region}')
                           """
        print(conn.write_sql(sqlInsert))
