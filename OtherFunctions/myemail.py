# 引入相应的模块
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class SendMail(object):

    def __init__(self):
        self.fromUser = "18921790946@139.com"
        self.userPasswd = "Ff112004@"  # 此处邮箱授权码， 不是登录密码
        self.smtpAddr = "smtp.139.com"
        self.to_list = []

    # 构造邮件结构
    # toAddrs 收件人可以是多个,["xxx@qq.com","xxx@qq.com"]， subject 邮件的主题， msg 邮件的内容
    def mailStructure_T(self, toAddrs,cc_list,subject, msg):
        # 邮件对象:
        mailMsg = MIMEMultipart()
        mailMsg['Subject'] = (" <%s>" % subject)
        mailMsg['From'] = ("python robot <%s>" % self.fromUser)
        mailMsg['To'] = ','.join(toAddrs)
        mailMsg['Cc'] = ','.join(cc_list)
        self.to_list = [message['to'], message['Cc']]
        # 邮件正文是MIMEText ：
        mailMsg.attach(MIMEText(msg, 'html', 'utf-8'))
        return mailMsg.as_string()

    def mailStructure_A(self, toAddrs,cc_list, subject, msg, file_path: list):
        # 邮件对象:
        mailMsg = MIMEMultipart()
        mailMsg['Subject'] = (" <%s>" % subject)
        mailMsg['From'] = ("Shuns_tool <%s>" % self.fromUser)
        mailMsg['To'] = ','.join(toAddrs)
        mailMsg['Cc'] = ','.join(cc_list)
        self.to_list = [mailMsg['to'], mailMsg['Cc']]
        # 邮件正文是MIMEText ：
        mailMsg.attach(MIMEText(msg, 'html', 'utf-8'))
        # 发送文件附件， 需要用到附件对象MIMEBase对象， 需要引入from email.mime.multipart import MIMEBase
        # 添加附件就是加上一个MIMEBase，从本地读取一个文件:
        for i in file_path:
            xlsx = MIMEApplication(open(i, 'rb').read())  # 打开Excel,读取Excel文件
            xlsx["Content-Type"] = 'application/octet-stream'  # 设置内容类型
            file_name = os.path.basename(i)
            xlsx.add_header('Content-Disposition', 'attachment', filename=file_name)  # 添加到header信息
            mailMsg.attach(xlsx)
        return mailMsg.as_string()

    # 发送邮件
    def send(self, toAddrs,cc_list, subject, msg, file_path):
        mailMsg_as_string = self.mailStructure_A(toAddrs,cc_list, subject, msg, file_path)
        # 连接服务器发送邮件
        try:
            server = smtplib.SMTP_SSL(self.smtpAddr, 465)
            server.connect(self.smtpAddr)  # 连接smtp服务器
            server.login(self.fromUser, self.userPasswd)  # 登录邮箱
            server.sendmail(self.fromUser, self.to_list, mailMsg_as_string)  # 发送邮件
            server.quit()
            info = '成功发送邮件'
            print("成功发送邮件")
        except Exception as e:
            info = f"Error: unable to send email:{e}"
            print("Error: unable to send email:", e)
        return info


if __name__ == '__main__':
    a = SendMail()
    # lst = [os.path.join(r'E:\Desktop\pdf\xml', i) for i in os.listdir(r'E:\Desktop\pdf\xml')]
    # print(lst)
    a.send(["wangxinyue@shunscom.com"], ['13645202570@139.com','wangxinyue@shunscom.com'],"ces1",'',file_path=[])
