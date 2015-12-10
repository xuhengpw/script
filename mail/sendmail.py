# -*- coding:utf-8 -*-
'''
sendmail模块根据文件次数发送告警
check_key模块记录文件次数至字典，返回查询文件对应的次数
read_file模块读取文件至字典
write_file模块将最新记录更新至文件

'''
 
import smtplib
from email.mime.text import MIMEText
import sys


class MailModel:
 
    def __init__(self):
        self.mail_host = "smtp.126.com"
        self.mail_user = "lanfeng007"
        self.mail_pass = "xuheng.qq.com"
        self.postfix = "126.com"

    def write_file(self,what):
        with open("user.txt", "w") as f:
            for key,value in what.items():
                f.writelines(str(key)+','+str(value)+'\n')
                f.flush()

    def read_file(self):
        with open("user.txt", "r") as f:
            listStu = {}
            for k,v in (l.split(',') for l in f) :
                listStu[k.strip()]=int(v.strip())
            return listStu

    def check_key(self,content):
            listStu=self.read_file()
            if content in listStu:
                listStu[content] = int(listStu[content]) + 1
                self.write_file(listStu)
                return listStu[content]
            else:
                listStu.update({content:1})
                self.write_file(listStu)
                return listStu[content]

    def send_mail(self, user_list, sub, content):
        '''
        根据check_key判断文件名记录次数
        大于3次则直接pass
        '''
        if self.check_key(content) > 2:
            print  '发送次数超过3次'
        else:
            me = "hello"+"<"+self.mail_user+"@"+self.postfix+">"
            msg = MIMEText(content, _subtype = 'html', _charset = 'utf-8')
            msg['Subject'] = sub
            msg['From'] = me
            msg['To'] = ';'.join(user_list)
            try:
                server = smtplib.SMTP()
                server.connect(self.mail_host)
                server.login(self.mail_user, self.mail_pass)
                server.sendmail(me, user_list, msg.as_string())
                server.close()
                print  '发送成功'
            except Exception, e:
                print str(e)
                print '发送失败，请检查'





if __name__=='__main__':
    mailuser_list=["369134@qq.com", "xuheng@tyread.com"]
    #title = sys.argv[1]
    #content = sys.argv[2]
    mail = MailModel()
    #mail.send_mail(mailuser_list,title, content)
    mail.send_mail(mailuser_list,'告警文件','/fiodata/DataFiles/outside/NGLogHour/2015-12-09//nginxxf/2015-12-09_192.168.10.194_14.log.zip')