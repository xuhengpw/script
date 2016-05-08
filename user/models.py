#encoding: utf-8

from dbbase import DBModel
import dbutil
import time

class User(DBModel):
    _table = 'user'
    _pk = 'id'
    _columns = ['id', 'username', 'password', 'telephone', 'age', 'sex', 'status']
    _defaults = {'status' : 0, 'sex' : 1, 'age' : 0}

    sql_login = 'SELECT * FROM user WHERE username=%s AND password=md5(%s) LIMIT 1;'
    sql_get_by_username = 'SELECT %s FROM user WHERE username=%%s LIMIT 1;'
    sql_insert = 'INSERT INTO user(username, password, telephone, age, sex, status) VALUES(%s, md5(%s), %s, %s, %s, %s);'
    sql_modify = 'UPDATE user SET telephone=%s, age=%s WHERE id=%s;'

    def login(self):
        _cnt, _ = self.execute(self.sql_login, (self.username, self.password), True)
        return _cnt > 0

    @classmethod
    def fetch_count(cls, query=''):
        _query = {}
        if query.strip() != '':
            _query['sql'] = 'username like %s'
            _query['args'] = ['%{username}%'.format(username=query)]
        
        _cnt, _ret = cls.query_count(query=_query)
        return _ret[0][0] if _cnt > 0 else 0 

    @classmethod
    def fetch_all(cls, query='', offset=None, limit=None):
        _query = {}
        if query.strip() != '':
            _query['sql'] = 'username like %s'
            _query['args'] = ['%{username}%'.format(username=query.strip())]
        
        _, _rt = cls.query_all(offset=offset, limit=limit, query=_query)
        return _rt
        
    def validate_add(self):
        if self.username == '' or self.password == '':
            return False, '用户名和密码不能为空'

        _user = self.get_by_username(self.username)
        if _user is not None:
            return False, '用户已注册'

        if not str(self.age).isdigit() or int(self.age) < 0 or int(self.age) > 100:
            return False, '用户年龄不正确'

        return True, ''

    @classmethod
    def get_by_username(cls, username):
        _sql = cls.sql_get_by_username % ','.join(cls.columns)
        _cnt, _users = cls.execute(_sql, (username, ), True)
        return dict(zip(cls.columns, _users[0])) if _cnt > 0 else None

    def create(self):
        _user = self.get_by_username(self.username)
        if _user is None:
            _cnt, _ = self.execute(self.sql_insert, \
                (self.username, self.password, self.telephone, self.age, self.sex, self.status))
            return _cnt > 0
        return False

    def validate_modify(self):
        if not str(self.age).isdigit() or int(self.age) < 0 or int(self.age) > 100:
            return False, '用户年龄不正确'
        return True, ''

    def update(self):
        _cnt, _ = self.execute(self.sql_modify, (self.telephone, self.age, self.id))
        return True 

class MachineRoom(DBModel):
    _table = 'machine_room'
    _pk = 'id'
    _columns = ['id', 'name']

    @classmethod
    def get_machine_rooms(cls):
        _sql = cls._sql_query_all.format(columns=','.join(cls._columns), table=cls._table)
        _, _machine_rooms = cls.execute(_sql, (), True)
        return dict(_machine_rooms)


class Asset(DBModel):
    _table = 'asset'
    _pk = 'id'
    _columns = 'id,sn,vendor,machine_room_id,model,purchase_date,cpu,ram,disk,os,ip,hostname,admin,bussiness,status'.split(',')
    _columns_add = 'sn,vendor,machine_room_id,model,purchase_date,cpu,ram,disk,os,ip,hostname,admin,bussiness'.split(',')
    _defaults = {'status' : 0}

    @classmethod
    def query_count(cls, query=''):
        _query = {}
        if query.strip() != '':
            _query['sql'] = 'hostname like %s'
            _query['args'] = ['%{hostname}%'.format(hostname=query)]
        
        _cnt, _ret = super(Asset, cls).query_count(query=_query)
        return _ret[0][0] if _cnt > 0 else 0 


    @classmethod
    def query_all(cls, query='', offset=None, limit=None):
        _query = {}
        if query.strip() != '':
            _query['sql'] = 'hostname like %s'
            _query['args'] = ['%{hostname}%'.format(hostname=query.strip())]
        
        _, _rt = super(Asset, cls).query_all(offset=offset, limit=limit, query=_query)
        return _rt

    def validate_add(self):
        errors = {}
        result = ''
        for _column in self._columns_add:
            if str(getattr(self, _column, '')).strip() == '':
                result = '验证失败'
                errors[_column] = '不能为空'

        return len(errors) == 0, result, errors

class Moniter(object):
    def __init__(self,ip,mtime,cpu,mem):
        self.ip = ip
        self.mtime = mtime
        self.cpu = cpu
        self.mem = mem

    def save(self):
        _sql = 'insert into moniter(ip,mtime,cpu,mem) values (%s,%s,%s,%s)'
        _cnt, _ = dbutil.execute_sql(_sql,(self.ip,self.mtime,self.cpu,self.mem))

        return _cnt > 0

    @classmethod
    def getDATA(cls,ip):

        _sql = 'select * from moniter where ip = %s and mtime >= %s order by mtime ASC '
        mtime =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - 60 * 60 ))
        _cnt,_res = dbutil.execute_sql(_sql,(ip,mtime),True )
        _times = []
        _cpu_data = []
        _mem_data = []
        for _rs in _res:
            _cpu,_mem,_time = _rs[2],_rs[3],_rs[4]
            _times.append(_time.strftime('%H:%M'))
            _cpu_data.append(_cpu)
            _mem_data.append(_mem)
        print {'categories':_times,'series':[{'name':'cpu','data':_cpu_data},{'name':'mem','data':_mem_data}]}
        return {'categories':_times,'series':[{'name':'cpu','data':_cpu_data},{'name':'mem','data':_mem_data}]}




# 测试的代码
if __name__ == '__main__':
    print get_users()
    print get_user_by_username('woniu')
    print validate_user_add('pc', '123', '', 'abc')
    print validate_user_add('woniu', '123', '', '12.4')
    print validate_user_add('woniu', '123456', '', '45')
    print add_user('test', '123456', '12345687998', 24)
    print add_user('kk', '123456', '12345687998', 13)
