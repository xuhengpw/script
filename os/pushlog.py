
#!/usr/bin/python

import sys
import time
import urllib
import urllib2
import socket
import fcntl
import struct

url='http://192.168.11.172:8088/logMonitor/disLog.do'

files='/ytxt/log/clientProduct/clientProduct.log'


def get_file_end():
    f=file(files,'r')
    f.seek(0,2)
    file_size=f.tell()
    f.close()
    return file_size


def get_content(files,file_size,last_file_size):
    f=file(files,'r')
    f.seek(last_file_size,0)
    lines=f.readlines()
    for line in lines:
        values={'logContent' : line,'ip'  : get_ip_address('eth0')}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        #print req
        try:
            urllib2.urlopen(req)
        except Exception,ex:
            print ex
    f.close()

def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', ifname[:15])
            )[20:24])

    except socket.error:
        return '172.0.0.1'

file_size=get_file_end()
last_file_size=file_size
while True:
    file_size=get_file_end()
    currentTime =  time.strftime('%Y-%m-%d %H:%M:%S')
    print str(file_size) + ';' + str(last_file_size) + ';' + currentTime
   # print get_ip_address('eth0')
    if(file_size>last_file_size):
        #文件修改
        get_content(files,file_size,last_file_size)

    last_file_size=file_size
    time.sleep(5)