#coding=utf-8
#版本号:0.1
#目前代码有点冗余，抽空优化
#实现web前端通过js 不断发送ajax调用获取日志接口输出至页面。

from flask import Flask
from flask import abort
from flask import redirect
from flask import render_template
from flask import Response
import subprocess

def execcommand(list):
        print tuple(list)
        pobj = subprocess.Popen('%s %s %s %s %s' % tuple(list),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        result = pobj.communicate()
        return result

def execcommand1(list):
        print tuple(list)
        pobj = subprocess.Popen('%s %s %s %s' % tuple(list),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        result = pobj.communicate()
        return result

base_path = "/root/demo-log/"
project = "tomcat-auth-service"
scriptname = '%s%s'%(base_path,'get_log.sh')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('log.html')

@app.route('/getlog/<hostname>/<line>')
def ajxGetLogHandle(hostname,line):
    host = hostname
    res = execcommand(['sh',scriptname,host,project,line])
    if not res[1] and res[0].strip():
        return Response(res[0])
    else:
        return Response(500)

@app.route('/getlog/<hostname>')
def ajxGetLog(hostname):
    host = hostname
    res = execcommand(['sh',scriptname,host,project])
    if not res[1]:
        try:
            if int(res[0]) > 20:
                line = int(res[0]) - 200
            if int(res[0]) == 0:
                line = 1
            return render_template('log.html',line=line)
        except Exception,e:
            print e
            return Response(e)
    else:
        return Response(res[1])

if __name__ == '__main__':
    app.run('0.0.0.0',8080,debug=True)
