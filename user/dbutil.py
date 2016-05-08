#encoding: utf-8

import MySQLdb

import gconf

'''
数据库操作步骤
1. 创建数据库连接
2. 获取游标
3. 执行sql语句
4. 提交事物(增删改)或获取查询结果(查)
5. 关闭游标
6. 关闭数据库连接
'''

# @method 执行sql
# @param str sql 需要执行的sql语句
# @param tuple args 预定义的变量，默认为空元组
# @param boolean is_fetch 是否为查询语句，默认为False 
def execute_sql(sql, args=(), is_fetch=False):
    _conn, _cur = None, None
    _rt_cnt, _rt_fetch = 0, ()

    try:
        # 步骤1
        _conn = MySQLdb.connect(host=gconf.DB_HOST, port=gconf.DB_PORT, \
                                user=gconf.DB_USER, passwd=gconf.DB_PASSWD, \
                                db=gconf.DB_NAME, charset=gconf.DB_CHARSET)

        _cur =_conn.cursor()                                # 步骤2
        _rt_cnt = _cur.execute(sql, args)                   # 步骤3
        if is_fetch:                                        # 步骤4  判断是否为查询还是修改动作
            _rt_fetch = _cur.fetchall()                         # 查询操作
        else:
            _conn.commit()
    except BaseException, e:
        print str(e)                                        # 打印异常
    finally:
        if _cur is not None:
            _cur.close()                                    # 步骤5
        if _conn is not None:
            _conn.close()                                   # 步骤6

    return _rt_cnt, _rt_fetch                               # 返回结果

if __name__ == '__main__':
    # 用户添加
    #print execute_sql('INSERT INTO user(username, password) VALUES(%s, md5(%s));', ('kk', '123456'))
    # 验证用户登录
    #print execute_sql('SELECT * FROM user WHERE username=%s AND password=md5(%s);', ('kk', '123456'), True)
    # 更改用户密码
    #print execute_sql('UPDATE user SET password=md5(%s) WHERE username=%s;', ('123456789', 'kk'))
    # 验证用户登录
    #print execute_sql('SELECT * FROM user WHERE username=%s AND password=md5(%s);', ('kk', '123456'), True)
    # 删除用户
    #print execute_sql('DELETE FROM user where username=%s', ('kk',))
    
    # 添加10个用户
    for i in range(100, 200):
        execute_sql('INSERT INTO user(username, password) VALUES(%s, md5(%s));', ('kk_%s' % i, '123456'))
    
    # 查询所有用户
    #_cnt, _rt = execute_sql('SELECT * FROM user', (), True)
    #print _cnt
    # 遍历所有用户
    #for _rs in _rt:
    #    print _rs

    # 删除所有用户
    #print execute_sql('DELETE FROM user')

    # 获取用户数量
    print execute_sql(sql='SELECT count(*) FROM user', is_fetch=True)
