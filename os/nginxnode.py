#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import getpass
import sys
import socket
import fcntl
import struct
import paramiko
 
def get_ip(ifname):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret
 
def ssh_key(nginxserver,port,username,pkey_file,cmd):
    try:
        key=paramiko.RSAKey.from_private_key_file(pkey_file)
        s=paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(nginxserver,port,username,pkey=key)
        stdin,stdout,stderr=s.exec_command(cmd)
        s.close()
    except:
        print stderr.read()
 
if __name__ == '__main__':
    nginxserver = ['192.168.11.176','192.168.11.177','192.168.11.158']
    port = '18822'
    username = 'weihu'
    usr_home = os.path.expanduser('~')
    pkey_file = usr_home + '/.ssh/id_rsa'
    ip = get_ip('eth0')
    if sys.argv[1] == 'dcstart':
        cmd = "/bin/sed -i '/%s:8080/s/^.*$/          server %s:8080;/g' /ytxt/nginx/conf/nginx.conf;/ytxt/nginx/sbin/nginx -s reload" % (ip,ip)
    elif sys.argv[1] == "dcstop":
        cmd = "/bin/sed -i '/%s:8080/s/^.*$/          server %s:8080 down;/g' /ytxt/nginx/conf/nginx.conf;/ytxt/nginx/sbin/nginx -s reload" % (ip,ip)
    elif sys.argv[1] == 'ddstart':
        cmd = "/bin/sed -i '/%s:8180/s/^.*$/          server %s:8180;/g' /ytxt/nginx/conf/nginx.conf;/ytxt/nginx/sbin/nginx -s reload" % (ip,ip)
    elif sys.argv[1] == 'ddstop':
        cmd = "/bin/sed -i '/%s:8180/s/^.*$/          server %s:8180 down;/g' /ytxt/nginx/conf/nginx.conf;/ytxt/nginx/sbin/nginx -s reload" % (ip,ip)
    else:
        print "Usage:nginxnode [dcstart|dcstop|ddstart|ddstop]"
        sys.exit()
 
 
    if len(sys.argv) < 2:
        print "Usage:nginxnode [dcstart|dcstop|ddstart|ddstop]"
        sys.exit()
 
    runuser='weihu'
    curuser = getpass.getuser()
    if curuser != runuser:
        print "this script need to be run as weihu."
        sys.exit()
 
    for server in nginxserver:
        ssh_key(server,port,username,pkey_file,cmd)
        print "%s in %s is successful." % (ip,server)
    print "everything is done."