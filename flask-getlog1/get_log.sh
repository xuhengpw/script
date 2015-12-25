#!/bin/bash
#通过ssh获取log行号和内容
set -e
HOST=$1
SERVICENAME=$2
LINENUM=$3
LOGFILE="/service/tomcat-auth-service/logs/catalina.out"
#LOGFILE="/service/$SERVICENAME/logs/catalina.out"
if [ $LINENUM ];then
    ssh -A -T root@$HOST "sed -n ${LINENUM}p $LOGFILE"
else
    ssh -A -T root@$HOST "wc -l $LOGFILE|awk '{print \$1}'"
fi
