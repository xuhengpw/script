#! /usr/bin/python
# _*_ coding:utf-8 _*_
import socket
import fileinput
 
 
file = "/ytxt/jboss/server/default/conf/scfconfig.properties"
com_log = "/ytxt/log/jboss_log/server.log"
pic_log = "/ytxt/log/clientProduct/clientProduct.log"
hostname = socket.gethostname().split('-')
 
 
try:
    if hostname[1] == "pi":
        f = open(pic_log,'r')
    else:
        f = open(com_log,'r')
except IOError,e:
    print e
 
f.seek(0,2)
 
for line in fileinput.input(file,inplace=1):
    k,v = line.strip().split("=",1)
    if k == "scf.service.online":
        if v == "true":
            line = line.replace("true","false")
        else:
            line = line.replace("false","true")
    print line,
 
fileinput.close()
 
while True:
    cur_pos = f.tell()
    line = f.readline()
    if not line:
        f.seek(cur_pos)
    else:
        x = line.decode('utf-8')
        if x.find(u"已注册") != -1:
            print "scf services online"
            break
        elif x.find(u"服务注销成功") != -1:
            print "scf services offline"
            break
        else:
            continue