#!/bin/bash

function base() {
  echo "####环境部署开始####"
  num=`rpm -qa |grep wget|wc -l`
  if [ $num -eq 0 ]
  then
  yum install wget -y;
  fi

  jdkPath="/usr/local/java/"
  appPath="/service/"
  tomcatPath="/service/apache-tomcat-7.0.59"
  if [ ! -d "$jdkPath" ]; then
     mkdir "$jdkPath"
     cd /usr/local/java
     echo "远程下载jdk包较慢，等待.."
     wget http://122.229.31.21:10008/soft/jdk-7u45-linux-x64.tar.gz -q
     tar -zxf jdk-7u45-linux-x64.tar.gz
     rm jdk-7u45-linux-x64.tar.gz
     echo "export JAVA_HOME=/usr/local/java/jdk1.7.0_45">>/etc/profile
     echo "export JRE_HOME=/usr/local/java/jdk1.7.0_45/jre">>/etc/profile
     echo "export CLASSPATH=.:\$JAVA_HOME/lib/dt.jar:\$JAVA_HOME/lib/tools.jar:\$JRE_HOME/lib:\$CLASSPATH">>/etc/profile
     echo "export PATH=\$JAVA_HOME/bin:\$PATH">>/etc/profile
     source /etc/profile
  fi


  if [ ! -d "$tomcatPath" ]; then
       mkdir "$appPath"
       cd $appPath
     echo "远程下载tomcat包较慢，等待.."
     wget http://122.229.31.21:10008/soft/apache-tomcat-7.0.59.tar.gz -q
     tar -zxf apache-tomcat-7.0.59.tar.gz
  fi
echo "1# JDK基础环境完成"
}

function app() {
  nn=`echo "$1"|cut -c 1-5`
  na="tomca"
  nb="awifi"
  if [ $nn = $na ]; then
    if [ ! -d "/service/$1" ]; then
       base
       cd /service/
       \cp -r apache-tomcat-7.0.59  $1
       cd $1/conf
       wget -O  server.xml http://122.229.31.21:10008/soft/tomcat/$1-service.xml -q
       rm -rf /service/$1/webapps/{docs,examples,host-manager,manager}
       echo "2# $1项目环境部署"
       info
    else
       echo "$1 该项目已存在 路径为"
       ls -l /service/$1
    fi
  elif [ $nn = $nb ]; then
    if [ ! -d "/service/zzz/$1" ]; then
       pybase
       mkdir -p /service/zzz/$1
       echo "$1项目环境部署完成，请上传相应代码包"
    else
       echo "$1 该项目已存在 路径为/server/zzz/"
       ls -l /service/zzz/$1
    fi
  else
    echo "有bug,怎么会到这里来，奇怪啊！"
  fi
}

function info() {
  echo "3# jdk路径为${JAVA_HOME}"
  echo "4# tomcat路径为:/service/"
  rm -rf /service/apache-tomcat-7.0.59.tar.gz
  ls -l /service/
}

function pybase() {
  pyPath="/usr/local/python2.7"
  if [ ! -d "$pyPath" ]; then
    yum install -y gcc gcc-c++ mysql-devel zlib-devel bzip2-devel openssl-devel xz-libs wget
    cd /usr/local/src/
    echo "远程下载Python包较慢，等待.."
    wget  http://122.229.31.21:10008/soft/Python-2.7.9.tar.gz -q
    wget  http://122.229.31.21:10008/soft/setuptools-1.4.2.tar.gz -q
    wget http://122.229.31.21:10008/soft/pip-1.5.6.tar.gz -q
    echo "开始Python环境安装"
    tar -zxf Python-2.7.9.tar.gz
    cd Python-2.7.9
    ./configure --prefix=/usr/local/python2.7
    make
    make altinstall
    mv /usr/bin/python /usr/bin/python.bak
    ln -s /usr/local/python2.7/bin/python2.7 /usr/bin/python
    cd /usr/local/src/
    tar -zxf setuptools-1.4.2.tar.gz
    cd setuptools-1.4.2
    python setup.py install
    cd /usr/local/src/
    tar -zxf pip-1.5.6.tar.gz
    cd pip-1.5.6
    python setup.py install
    echo "export PATH=\$PATH:/usr/local/python2.7/bin/">>/etc/profile
    source /etc/profile
    echo "完成Python基础环境"
    upip
  fi
}

function upip() {
echo "开始pip模块安装"
/usr/local/python2.7/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  uWSGI==2.0.10 Pillow==2.8.1  psutil==2.2.1 pika simplejson==3.6.5
echo "等待.."
/usr/local/python2.7/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple backports.ssl-match-hostname==3.4.0.2  BeautifulSoup==3.2.1  beautifulsoup4==4.3.2 certifi==14.05.14  Django==1.7.5 django-redis-cache==0.13.0 ez-setup
echo "等待....."
/usr/local/python2.7/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flup==1.0.2 image==1.3.9  Jinja2==2.7.3  MarkupSafe  meld3==1.0.0 MySQL-python==1.2.3 pika Pillow==2.8.1
echo "模块安装完成"
/usr/local/python2.7/bin/pip list
}



read -p "输入需要部署TOMCAT产品项(auth/portal/access/wg/4a-app/4a-cas/oms/2b-pub/2b-admin/2b-api) :" KEY
case $KEY in
auth)
  app  tomcat-auth6001
;;
portal)
  app  tomcat-portal6000
;;
access)
  app  tomcat-access6002
;;
wg)
  app  tomcat-wg5000
;;
oms)
  app  tomcat-oms5003
;;
4a-app)
  app  tomcat-app5002
;;
4a-cas)
  app  tomcat-cas5001
;;
2b-pub)
  app  awifimerchant
;;
2b-admin)
  app  awifiadmin
;;
2b-api)
  app  awifiapi
;;
test)
  upip
;;
*)
echo "非法参数"
esac