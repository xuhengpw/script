# coding=utf-8
# 版本号:0.1
# 目前代码有点冗余，抽空优化


import subprocess
import os
import sys

from flask import Flask
from flask import render_template
from flask import Response
from flask import request

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 定义常用环境变量
base_path = "/ytxt/flask-web/shell/"
script_name = '%s%s' % (base_path, 'todo.sh')
# 项目名称对应主机
get_hostip = {'cic-content': '192.168.20.182', 'ReadWapPortal': '192.168.20.127', 'culverin-web': '192.168.20.129',
              'operations-client': '192.168.20.248', 'productClient-1.0.4': '192.168.20.181',
              'uic-client': '192.168.20.130', 'ClientWap': '192.168.20.130'}
# 项目名称对应版本库URL
get_pj_url = {'cic-content': 'http://192.168.10.166/sy/2013/cic/deploy/cic-content.war',
              'ClientWap': 'http://192.168.10.166/sy/2013/www/deploy/ClientWap.war.zip',
              'ReadWapPortal': 'http://192.168.10.166/sy/2013/www/deploy/ReadWapPortal.war.zip',
              'culverin-web': 'http://192.168.10.166/sy/2013/xf/deploy/culverin-web.war',
              'operations-client': 'http://192.168.10.166/sy/2013/oic/deploy/operations-client.war',
              'productClient-1.0.4': 'http://192.168.10.166/sy/2013/pic/deploy/productClient-1.0.4.war',
              'uic-client': 'http://192.168.10.166/sy/2013/uic/deploy/uic-client.war'}
# 项目验证页面
check_url = {'cic-content': 'wu', 'ClientWap': 'http://192.168.20.130/androidFour/jingxuan.action?channelCode=manhua',
             'ReadWapPortal': 'http://192.168.20.127:8080/',
             'culverin-web': 'http://192.168.20.129:9080/admin/adminManagerTools.htm', 'operations-client': '400',
             'productClient-1.0.4': '400', 'uic-client': '192.168.20.130'}


def execcommand(list):
    print "##execmd##"
    print tuple(list)
    new_env = os.environ.copy()
    # new_env['MEGAVARIABLE'] = 'MEGAVALUE'
    pobj = subprocess.Popen('%s %s %s %s' % tuple(list), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                            env=new_env)
    result = pobj.communicate()
    return result


def check_md5(project, md5):
    new_env = os.environ.copy()
    pj_url = get_pj_url[project]
    pobj = subprocess.Popen("/usr/bin/curl   -u weihu:ydfSD89  -s  %s |md5sum|awk '{print $1}' " % pj_url,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=new_env)
    result = pobj.communicate()
    print "##check_md5##"
    print pj_url
    print result[0].strip('\n')
    if md5 == result[0].strip('\n'):
        return 'Yes'
    else:
        return result[0]


app = Flask(__name__)


@app.route('/')
def index():
    pj_list = []
    for i in get_hostip.keys():
        pj_list.append(i)
    return render_template('index.html', pj_list=pj_list)


# 获取机器:项目：日志，验证部署过程
@app.route('/getlog/<project>/<line>')
def ajxGetLog(project, line):
    hostip = get_hostip[project]
    res = execcommand(['sh', script_name, hostip, project, line])
    if not res[1] and res[0].strip():
        return Response(res[0])
    else:
        return Response(500)


# 通过项目+md5验证最新版本，执行部署脚本
@app.route('/deploy', methods=['GET', 'POST'])
def ajxDeploy():
    project = request.args.get('project_name')
    md5 = request.args.get('md5_value')
    pj_md5 = check_md5(project, md5)
    if pj_md5 != 'Yes':
        return Response("请求md5与服务器端md5值" + pj_md5.strip() + "不匹配")
    host_ip = get_hostip[project]
    url = check_url[project]
    res = execcommand(['sh', script_name, host_ip, project])
    print "##ajxDeploy##"
    print project
    print md5
    print url
    print res[0]
    print res[1]
    if not res[1] and res[0].strip():
        return Response(res[0])
    else:
        return Response(500)


if __name__ == '__main__':
    app.run('0.0.0.0', 18081, debug=True)
