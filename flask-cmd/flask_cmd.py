#coding=utf-8
#版本号:0.1
#目前代码有点冗余，抽空优化
#实现web前端通过js 不断发送ajax调用获取日志接口输出至页面。

from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import subprocess
import os
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#定义常用环境变量
base_path = "/root/shell/"
script_name = '%s%s'%(base_path,'todo.sh')
#项目名称对应主机
get_hostip = {'ReadWapPortal':'192.168.10.189'}
#项目名称对应版本库URL
get_pj_url = {'ReadWapPortal':'http://192.168.10.189:8081/hello.war'}
#项目验证页面
check_url = {'ReadWapPortal':'http://192.168.10.189:8080/hello'}

def execcommand(list):
        print tuple(list)
        new_env = os.environ.copy()
        #new_env['MEGAVARIABLE'] = 'MEGAVALUE'
        pobj = subprocess.Popen('%s %s %s' % tuple(list),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,env=new_env)
        result = pobj.communicate()
        return result

def check_md5(project,md5):
        new_env = os.environ.copy()
        pj_url=get_pj_url[project]
        pobj = subprocess.Popen("/usr/bin/curl   -s  %s |md5sum|awk '{print $1}' " % pj_url,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,env=new_env)
        result = pobj.communicate()
        if md5 == result[0].strip('\n'):
            return 'Yes'
        else:
            return  result[0]


app = Flask(__name__)


@app.route('/')
def index():
    pj_list=[]
    for i in get_hostip.keys():
        pj_list.append(i)
    return render_template('index.html',pj_list=pj_list)

#获取机器:项目：日志，验证部署过程
@app.route('/getlog/<project>/<line>')
def ajxGetLog(project,line):
    hostip = get_hostip[project]
    res = execcommand(['sh',script_name,hostip,project,line])
    if not res[1] and res[0].strip():
        return Response(res[0])
    else:
        return Response(500)

#通过项目+md5验证最新版本，执行部署脚本
@app.route('/deploy', methods = ['GET', 'POST'])
def ajxDeploy():
    project=request.args.get('project_name')
    md5=request.args.get('md5_value')
    pj_md5 = check_md5(project,md5)
    if pj_md5 != 'Yes':
        return Response("请求md5与服务器端md5值"+pj_md5.strip()+"不匹配"+"<a href='http://192.168.10.187:8080/deploy?project_name="+project+"&md5_value="+pj_md5.strip()+"'>提交服务端md5部署</a>")
    host_ip = get_hostip[project]
    url = check_url[project]
    print url
    res = execcommand(['sh',script_name,host_ip])
    if not res[1] and res[0].strip():
        return Response(res[0]+'<a href="%s">验证页面</a>'% url )
    else:
        return Response(500)

if __name__ == '__main__':
    app.run('0.0.0.0',8080,debug=True)