#! /usr/bin/python
import os
import re
import sys
import time
import shutil
import socket
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
 
def tail (file,keyword):
    f = open(file,'r')
    f.seek(0,2)
    s_time = int(time.time())
 
    while True:
        e_time = int(time.time())
        cur_pos = f.tell()
        line = f.readline()
        if not line:
            f.seek(cur_pos)
        if e_time - s_time > 60:
            print "Execute timeout!!!"
            sys.exit(2)
        else:
            m = re.search(keyword, line)
            if m:
                time.sleep(2)
                break
    f.close()
 
 
host_type = socket.gethostname().split('-')[1]
host_package = {
    'mh':       'ReadWapPortal.war',
    'culverin': 'culverin-web.war',
    'ci':       'cic-content.war',
    'oic':      'operations-client.war',
    'pi':       'productClient-1.0.4.war',
    'uic':      'uic-client.war'
    }
 
# backup
date = time.strftime('%Y%m%d',time.localtime(time.time()))
datedir = '/ytxt/backup/%s' %(date)
if host_type != 'mh':
    salt_bak = "/var/cache/salt/minion/file_backup/ytxt/jboss/server/default/deploy/"
    l = os.listdir(salt_bak)
    l.sort(key=lambda fn: os.path.getmtime(salt_bak+fn) if not os.path.isdir(salt_bak+fn) else 0)
    src = os.path.join(salt_bak,l[-1])
#src = '/ytxt/jboss/server/default/deploy/%s' %(host_package[host_type])
dst = datedir + '/' + host_package[host_type]
 
if not os.path.isdir(datedir):
    os.makedirs(datedir)
 
if host_type == 'mh':
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
 
# services offline
#if host_type == 'mh' or host_type == 'culverin':
#    cmd("/usr/bin/f5node stop")
#else:
#    cmd("/usr/bin/scf")
 
# restart jboss
cmd("/usr/bin/restartjboss")
 
if host_type == 'mh':
    filelog = '/ytxt/log/jboss_log/server.log'
    keyword = r'\[STDOUT\] \(timer\)'
    tail(filelog,keyword)
    cmd("/usr/bin/f5node start")
elif host_type == 'culverin':
    filelog = '/ytxt/log/culverin/core_culverin.log'
    keyword = r'Started'
    tail(filelog,keyword)
    cmd("/usr/bin/f5node start")
 
print "Everything is ok!!!"