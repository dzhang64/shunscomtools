import time

from OtherFunctions.ShunscomSQL import ShunscomToolSql
import traceback

from OtherFunctions.logdefine import MyLogging

mlogger = MyLogging(file=f"./log.log")


class ShunscomToolLogin:
    def __init__(self, userName='', passWord='', ):
        self.userName = userName  # 工具的用户名
        self.passWord = passWord  # 工具的密码
        self.sql = ShunscomToolSql()  # 连接数据库
        self.date = time.strftime('%Y-%m-%d')  # 工具登录时间
        self.state = 0  # 用于判断是否登录成功
        self.info = ''  # 返回信息

    def login(self):
        if not self.userName:
            self.info = '请输入用户名'
            return
        if not self.passWord:
            self.info = '请输入密码'
            return

        sql = f"""
                    select * from toolusers where username='{self.userName}' and password='{self.passWord}'
                    """
        try:
            rows = self.sql.query_sql(sql)
            print(rows)
            if len(rows) == 1:
                self.state = 1
                sql_update = f"""update toolusers set lastdate='{self.date}' 
                where username='{self.userName}'
                            """
                self.sql.write_sql(sql_update)
                self.info = '登录成功'
            else:
                self.info = '用户或密码错误'
            mlogger.info(f'{self.userName}{self.info}')
        except Exception as e:
            self.info = (e, traceback.format_exc())
            mlogger.info(f'{self.info}')


class ShunscomToolRegister:
    def __init__(self, userName='', passWord='', passWordConfirm=''):
        self.userName = userName  # 工具的用户名
        self.passWord = passWord  # 工具的密码
        self.passWordConfirm = passWordConfirm  # 工具的密码
        self.sql = ShunscomToolSql()  # 连接数据库
        self.info = ''
        self.state = 0  # 用于判断是否登录成功

    def register(self, operate):
        if not self.userName:
            self.info = '请输入账号'
            return
        if not self.userName.endswith('@shunscom.com'):
            self.info = '请输入注册的账号必须为公司邮箱'
            return
        if not self.passWord:
            self.info = '请输入密码'
            return
        if not self.passWordConfirm:
            self.info = '请确认密码'
            return
        if self.passWord != self.passWordConfirm:
            self.info = '密码不一致'
            return

        if operate == 'register':
            sqlEmail = f"""
                    select * from emailusers
                    where username='{self.userName}'
                """

            sqlTool = f"""
                    select * from toolusers
                    where username='{self.userName}'
                """
            try:
                rows = self.sql.query_sql(sqlEmail)
                rows1 = self.sql.query_sql(sqlTool)
                if len(rows) != 1:
                    self.info = '请确认邮箱是否正确，如正确请联系联系作者'
                    return
                if len(rows1) >= 1:
                    self.info = '该账号已被注册'
                    return
                sqlInsert = f"""
                                    insert into toolusers
                                   (username,password,lastdate)
                                   values
                                   ('{self.userName}','{self.passWord}','{time.strftime('%Y-%m-%d', time.localtime())}')
                                   """
                self.sql.write_sql(sqlInsert)
                self.info = '注册成功'
                self.state = 1
            except Exception as e:
                self.info = (e, traceback.format_exc())

        elif operate == 'update':
            sql = f"""select * from toolusers
                    where username='{self.userName}'
                    """
            try:
                rows = self.sql.query_sql(sql)
                if len(rows) == 1:
                    sql = f"""
                                    update toolusers set
                                    password='{self.passWord}'
                                    where username='{rows[0]['username']}'
                                """
                    self.sql.write_sql(sql)
                    self.info = '密码修改成功'
                    self.state = 1
                else:
                    self.info = '账号不正确，请重新输入'
            except Exception as e:
                self.info = (e, traceback.format_exc())
        mlogger.info(f'{self.info}')


if __name__ == '__main__':
    q = ShunscomToolLogin(userName='wangxinyue@shunscom.com', passWord='1')
    q.login()
    print(q.info)
