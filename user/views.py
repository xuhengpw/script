#encoding: utf-8
import sys
from functools import wraps
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import time


# 引入flask中的必要类和函数
from flask import Flask              #创建Flask APP对象
from flask import request            #用于获取用户提交的数据
from flask import render_template    #加载模板
from flask import redirect           #重定向到其他url
from flask import session

# 导入自定义的模块
import gconf
import models
from pagelist import PageList
from  remotercmd import runcmd

# 创建一个Flask app
# Flask需要根据传递的参数去寻找templates, static等目录的位置
app = Flask(__name__)
app.secret_key = 'fdsfdsafdsfdsafdsafds'


def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper

# homepage
# 定义路由, 如果以GET方式访问url地址为/则由index函数处理
@app.route('/')
def index():
    # 返回templates目录下的login.html模板中的内容
    return render_template('login.html')

# 登陆验证
# 定义路由, 若以GET、POST方式提交请求到url地址/login/则有login函数处理
@app.route('/login/', methods=['GET', 'POST'])
def login():
    user = models.User.create_by_request(request)
    
    # 验证用户名和密码
    if user.login():
        # 成功则显示所有用户的信息列表
        session['user'] = {'username' : user.username}
        return redirect('/users/')
    else:
        # 失败则提示用户失败, 依然返回登陆页面
        return render_template('login.html', error='用户名或密码错误', login_username=user.username)


# 注册
# 定义路由, 若以POST方式提交请求到url地址/register/则有register函数处理
@app.route('/register/', methods=['POST'])
def register():
    # 从request.form中获取username、password、telephone信息
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    telephone = request.form.get('telephone', '')
    age = request.form.get('age', '')

    # 检查用户提交的数据
    ok, result = models.user.validate_user_add(username, password, telephone, age)
    
    # 如果检查通过则添加到文件中
    if ok:
        if models.user.add_user(username, password, telephone, age):
            ok = True
            result = '注册成功'
        else:
            ok = False
            result = '注册失败'

    return render_template('login.html', ok=ok, result=result, register_username=username, password=password, telephone=telephone, age=age)

# 获取用户列表
# 定义路由, 如果以GET方式访问url地址为/users/则由users函数处理
@app.route('/users/', methods=['GET', 'POST'])
@login_required
def users():
    params = request.args if request.method == 'GET' else request.form
    _query = params.get('query', '')
    _total = models.User.fetch_count(_query)
    _page_size = params.get('pageSize', gconf.PAGE_SIZE)
    _page_num = params.get('pageNum', 1)

    _pageList, _offset = PageList.create_pagelist(_page_num, _page_size, _total)
    # 获取所有用户
    _users = models.User.fetch_all(_query, _offset, _pageList.pageSize)
    _pageList.set_contents(_users)
    
    # 返回用户列表页面
    return render_template('users.html', query=_query, pageList=_pageList)

# 添加用户信息(打开页面)
@app.route('/createUser/')
@login_required
def createUser():
    return render_template('create.html')

# 添加用户信息(更新DB)
@app.route('/addUser/', methods=['POST', 'GET'])
@login_required
def addUser():
    user = models.User.create_by_request(request)

    # 检查用户提交的数据
    ok, result = user.validate_add()
    
    # 如果检查通过则添加到文件中
    if ok:
        if user.create():
            ok = True
            result = '注册成功'
        else:
            ok = False
            result = '注册失败'
    if ok:
        #return redirect('/users/')
        return json.dumps({'ok' : True})
    else:
        #return render_template('create.html',  result=result, register_username=username, password=password, telephone=telephone, age=age)
        return json.dumps({'ok' : False, 'result' : result})

# 更新用户信息(更新DB)
@app.route('/updateUser/', methods=['POST'])
@login_required
def updateUser():
    _id = request.form.get('id', '')
    _ouser = models.User.query_by_pk(_id)
    if _ouser is None:
        return render_template('update.html', result='用户信息不存在')
    else:
        _nuser = models.User.create_by_request(request)

        # 检查用户提交的数据
        ok, result = _nuser.validate_modify()
        
        # 如果检查通过则添加到DB
        if ok:
            if _nuser.update():
                ok = True
                result = '更新成功'
            else:
                ok = False
                result = '更新失败'
        if ok:
            #return redirect('/users/')
            return json.dumps({'ok' : True})
        else:
            return json.dumps({'ok' : False, 'result' : result})
            #return render_template('update.html', result=result, id=_user['id'], username=_user['username'], telephone=telephone, age=age)


# 删除用户信息
@app.route('/deleteUser/')
@login_required
def deleteUser():
    _id = request.args.get('id', '')
    models.User.delete(_id)
    #return redirect('/users/')
    return json.dumps({'ok' : True})

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/assets/', methods=['GET', 'POST'])
@login_required
def assets():
    params = request.args if request.method == 'GET' else request.form
    _query = params.get('query', '')

    _total = models.Asset.query_count(_query)
    _machine_rooms = models.MachineRoom.get_machine_rooms()
    
    # 分页信息
    _page_num = params.get('pageNum', 1)
    _page_size = params.get('pageSize', gconf.PAGE_SIZE)

    _pageList, _offset = PageList.create_pagelist(_page_num, _page_size, _total)
    
    _assets = models.Asset.query_all(_query, _offset, _pageList.pageSize)
    _pageList.set_contents(_assets)
    print _pageList
    return render_template('assets.html', machineRooms=_machine_rooms, query=_query, pageList=_pageList) 


@app.route('/machine_rooms/')
def machine_rooms():
    return json.dumps(models.MachineRoom.get_machine_rooms())

@app.route('/addAsset/', methods=['POST'])
def addAsset():
    _asset = models.Asset.create_by_request(request)
    
    # 检查用户提交的数据
    ok, result, errors = _asset.validate_add()

    if ok:
        if _asset.create():
            ok = True
            result = '添加成功'
        else:
            ok = False
            result = '添加失败'

    return json.dumps({'ok' : ok, 'result' : result, 'errors' : errors})


@app.route('/moniters/', methods=['POST'])
def moniter():
    mtime = request.form.get('mtime','')
    cpu = request.form.get('cpu','')
    mem = request.form.get('mem','')
    ip = request.form.get('ip','')
    mtime = time.strftime('%Y-%m-%d %H:%M%S',time.localtime(int(mtime)))
    rt = models.Moniter(ip,mtime,cpu,mem).save()
    return json.dumps({'code':rt})

@app.route('/moniters/<pk>/',methods=['GET'])
def getmoniters(pk=None):
    _data = models.Moniter.getDATA(pk)
    return json.dumps({'code':200,'data':_data})


@app.route('/remotercmd/',methods=['POST'])
def remotercmd():
    params = request.args if request.method == 'GET' else request.form
    ip = params.get('ip','')
    user = params.get('user','')
    passwd = params.get('passwd','')
    cline = params.get('cline','')

    if user == "" and passwd == "" and cline =="":
        return '信息为空'
    else:
        result = runcmd(ip,user,passwd,cline)
        return json.dumps({'result':result})