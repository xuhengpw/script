#!/bin/bash
#通过ssh获取log行号和内容
set -e
HOST=$1
SERVICENAME=$2
LINENUM=$3
#LOGFILE="/service/tomcat-auth-service/logs/catalina.out"
#LOGFILE="/service/$SERVICENAME/logs/catalina.out"
if [ $LINENUM ];then
    #ssh -A -T weihu@$HOST "sed -n ${LINENUM}p $LOGFILE"
    echo "todo fail"
else
    #ssh -A -T weihu@$HOST "wc -l $LOGFILE|awk '{print \$1}'"
    ssh -A -T weihu@$HOST "source /etc/profile;source ~/.bash_profile;python /ytxt/shell/deploy.sh $SERVICENAME"
fi

