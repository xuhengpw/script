#!/usr/bin/env python
# -*- coding: utf-8 -*-

from netmiko import ConnectHandler
import time
from dbutil import execute_sql
import os


def get_FileSize(filePath):
    filePath = filePath.encode("utf-8")
    fsize = os.path.getsize(filePath)
    fsize = fsize
    return round(fsize,2)

def Cisco(ip):
    "思科交换机配置导出函数"
    cisco_881 = {
        'device_type': 'cisco_asa',
        'ip': ip,
        'username': 'ww',
        'password': 'WDco',
        'port': 22,  # optional, defaults to 22
        'secret': 'WDsco',  # optional, defaults to ''
        'verbose': False,  # optional, defaults to False
    }
    net_connect = ConnectHandler(**cisco_881)
    net_connect.enable()
    commands = [
        'show run',
    ]
    timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    timestr2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    filezip='/data/backup/net/%s_%s.zip' %('zhuanxian-ASA',timestr)
    for cmd in commands:
        filename = u'/data/backup/net/%s_%s_%s.txt' % (ip, cmd.replace(' ', '_'), timestr)
        save = open(filename, 'w')
        result = net_connect.send_command(cmd)
        save.write(result)
	time.sleep(1)
	os.system('zip -P wdy017 %s %s'%(filezip,filename))
    net_connect.disconnect() 
    return  filezip
	
	

def check_File(filezip):
    fexists = os.path.exists(filezip)
    fsize = os.path.getsize(filezip)
    if fexists:                  
        if fsize <= 100 :
               return 0
        else:
               return 1
    else:
        return 0				

	
def get_Time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def insert_sql(ipaddr,bk_start_time,bk_path,bk_end_time,bk_size,bk_state,create_time):
    execute_sql("INSERT INTO backup_info (ip_addr,bk_start_time,bk_path,bk_end_time,bk_size,bk_state,create_time) VALUES('%s','%s','%s','%s','%s','%s','%s');"%(ipaddr,bk_start_time,bk_path,bk_end_time,bk_size,bk_state,create_time))
	

if __name__ == '__main__':
    ips = ['19235',]
    for ip in ips:
        ipaddr=ip
        bk_start_time=get_Time()
        bk_path=Cisco(ip)
        bk_end_time=get_Time()
        bk_size=get_FileSize(bk_path)
        bk_state=check_File(bk_path)
        create_time=bk_start_time
        print ipaddr,bk_start_time,bk_path,bk_end_time,bk_size,bk_state,create_time
        insert_sql(ipaddr,bk_start_time,bk_path,bk_end_time,bk_size,bk_state,create_time)
