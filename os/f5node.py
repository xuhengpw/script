#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import paramiko
import socket
import fcntl
import struct
 
def get_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
        ret = socket.inet_ntoa(inet[20:24])
        return ret
 
def ssh(ip,port,username,passwd,cmd):
        try:
                #paramiko.util.log_to_file('paramiko.log')
                s =  paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(ip,port,username,passwd,timeout=5)
                stdin, stdout, stderr = s.exec_command(cmd)
                #print stdout.read()
                s.close()
        except:
                print '%s\tError\n' %(ip)
 
if __name__ == '__main__':
        ip = get_ip('eth0')
        hostname = socket.gethostname().split('-')
        f5server = '192.168.10.251'
        f5port = '22'
        f5user = 'tyyd'
        f5passwd = 'tyyd2014tyyd'
 
        dic = {
                'mh':('SJYD-MH-pool','80'),
                'www':('SJYD-WWW-8000-POOL','8000'),
                'xf':('SJYD-OLDXF-8080-pool','8080'),
                'culverin':('SJYD-XF12-80-pool','80'),
                'jf':('SJYD-JF-80-POOL','80'),
                'html5':('SJYD-HTML5-80-pool','80')
        }
 
        if len(sys.argv) < 2:
                print "Usage:f5node [start|stop]"
                sys.exit()
 
        try:
                pool = dic[hostname[1]][0]
                port = dic[hostname[1]][1]
                if sys.argv[1] == "start":
                        status = 'enable'
                elif sys.argv[1] == "stop":
                        status = 'disable'
                cmd = 'pool %s member %s:%s session %s' %(pool,ip,port,status)
                ssh(f5server,f5port,f5user,f5passwd,cmd)
        except:
                print "Error,please check again!"