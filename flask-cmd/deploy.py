#! /usr/bin/python
#coding=utf-8
import os
import sys
import time
import shutil
import subprocess
import zipfile

def cmd (script):
    ret = subprocess.call(script, shell=True)
    if ret != 0:
        print "script execution problems encountered!!!"
        sys.exit(1)
    time.sleep(2)

def zip_dir(dir,zipname):
    if not os.path.exists(dir):
        print "%s is not exist" %s
        sys.exit(1)
    zf = zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED)
    for root,dirs,files in os.walk(dir):
        for name in files:
            zf.write(os.path.join(root,name))
    zf.close()

def tail (file):
    f = open(file,'r')
    f.seek(0,2)
    s_time = int(time.time())

    while True:
        e_time = int(time.time())
        cur_pos = f.tell()
        line = f.readline()
        if not line:
            f.seek(cur_pos)
        if e_time - s_time > 120:
            print "Execute timeout!!!"
            sys.exit(2)
        else:
            x = line.decode('utf-8')
            if x.find(u"推送下来") != -1:
                print "部署完成"
                break
            elif x.find(u"成功") != -1:
                print "部署完成"
                break
            else:
                continue
    f.close()

#定义项目对应项目包
host_package = {
    'ReadWapPortal':       'ReadWapPortal.war',
    'culverin-web': 'culverin-web.war',
    'cic-content':       'cic-content.war',
    'operations-client':      'operations-client.war',
    'productClient-1.0.4':       'productClient-1.0.4.war',
    'uic-client':      'uic-client.war',
    'ClientWap': 'ClientWap.war.zip'
    }
#定义项目下载包命令以及URL
get_curl_url = {'cic-content':'curl -u weihu:xxx -s -o /tmp/cic-content.war  http://192.168.10.166/sy/2013/cic/deploy/cic-content.war;curl -u weihu:xxxx -s  -o /ytxt/jboss/server/default/deploy/cic-business.war  http://192.168.10.166/sy/2013/cic/deploy/cic-business.war',
              'ClientWap':'curl -u weihu:xxxx -s  -o /tmp/ClientWap.war.zip http://192.168.10.171/sy/2014/wap/deploy/ClientWap.war.zip',
              'ReadWapPortal':'curl -u weihu:xxxx  -s -o /tmp/ReadWapPortal.war.zip http://192.168.10.166/sy/2013/www/deploy/ReadWapPortal.war.zip',
              'culverin-web':'curl -u weihu:xxxx -s  -o /tmp/culverin-web.war http://192.168.10.166/sy/2013/xf/deploy/culverin-web.war  ',
              'operations-client.war':'curl -u weihu:xxxx -s  -o /ytxt/jboss/server/default/deploy/operations-client.war  http://192.168.10.166/sy/2013/oic/deploy/operations-client.war',
              'productClient-1.0.4':'curl -u weihu:xxxx -s  -o /ytxt/jboss/server/default/deploy/productClient-1.0.4.war  http://192.168.10.166/sy/2013/pic/deploy/productClient-1.0.4.war',
              'uic-client':'curl -u weihu:xxxx -s -o /ytxt/jboss/server/default/deploy/uic-client.war http://192.168.10.166/sy/2013/uic/deploy/uic-client.war'
              }




#接收项目参数
if len(sys.argv) < 2:
        print "Usage:deploy package_name"
        sys.exit()

host_type = sys.argv[1]

if host_type  not in host_package:
        print "Usage: %s not found" % host_type
        sys.exit()


#获取下载包命令，并执行
curl_war=get_curl_url[host_type]
cmd(curl_war)


# 执行备份操作,非ReadWapPortal，获取tmp最新一个文件,src=/tmp/xxx
date = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
datedir = '/ytxt/backup/%s' %(date)
if host_type != 'ReadWapPortal':
    salt_bak = "/tmp/"
    l = os.listdir(salt_bak)
    l.sort(key=lambda fn: os.path.getmtime(salt_bak+fn) if not os.path.isdir(salt_bak+fn) else 0)
    src = os.path.join(salt_bak,l[-1])
#src = '/ytxt/jboss/server/default/deploy/%s' %(host_package[host_type])
dst = datedir + '/' + host_package[host_type]

#备份目录创建
if not os.path.isdir(datedir):
    os.makedirs(datedir)

#执行新包mv至部署目录
if host_type == 'ReadWapPortal':
    zipname = 'ReadWapPortal.war.zip'
    srczip = '/tmp/ReadWapPortal.war.zip'
    mhdir = '/ytxt/jboss/server/default/deploy/ReadWapPortal.war'
    if os.path.isfile(srczip) and os.path.isdir(mhdir):
        if not os.path.isdir(dst):
            shutil.move(mhdir,dst)
            os.chdir(datedir)
            zip_dir(host_package[host_type],zipname)
            os.chdir('/home/weihu')
        f = zipfile.ZipFile(srczip,'r')
        f.extractall('/ytxt/jboss/server/default/deploy')
        f.close()
    else:
        print "Lack the necessary directories and files!"
        sys.exit(2)
else:
    if not os.path.isfile(dst):
        shutil.copy(src,dst)



#根据机器，执行重启验证操作
if host_type == 'ReadWapPortal':
    cmd("/usr/bin/restartjboss")
    time.sleep(5)
    filelog = '/ytxt/log/jboss_log/server.log'
    tail(filelog)
elif host_type == 'culverin-web':
    cmd("/usr/bin/restartculverinjboss")
    time.sleep(5)
    filelog = '/ytxt/logculverin/culverin/core_culverin.log'
    tail(filelog)
elif host_type == 'cic-content':
    cmd("/usr/bin/restartjboss")
    time.sleep(5)
    filelog = '/ytxt/log/jboss_log/server.log'
    tail(filelog)
elif host_type == 'operations-client':
    cmd("/usr/bin/restartjboss")
    time.sleep(5)
    filelog = '/ytxt/log/jboss_log/server.log'
    tail(filelog)
elif host_type == 'productClient-1.0.4':
    cmd("/usr/bin/restartjboss")
    time.sleep(5)
    filelog = '/ytxt/log/clientProduct/clientProduct.log'
    tail(filelog)
elif host_type == 'uic-client':
    cmd("/usr/bin/restartjboss")
    time.sleep(5)
    filelog = '/ytxt/log/jboss_log/server.log'
    tail(filelog)
elif host_type == 'ClientWap':
    cmd("/usr/bin/restartemjboss")
    time.sleep(5)
    filelog = '/ytxt/logembed/jboss_log/server.log'
    tail(filelog)
else:
    print "nnnnnnnnnnn"

print "Everything is ok!!!"
