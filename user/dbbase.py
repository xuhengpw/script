#encoding: utf-8

import logging
import json

from dbutil import execute_sql

logger = logging.getLogger(__name__)

class DBModel(object):
    _table = ''
    _pk = ''
    _columns = []
    _columns_add = []
    _columns_update = []
    _defaults = {}
    _sql_query_all = 'SELECT {columns} FROM {table} WHERE 1=1'
    _sql_query_count = 'SELECT COUNT(*) FROM {table} WHERE 1=1'
    _sql_query_by_pk = 'SELECT {columns} FROM {table} WHERE {pk} = %s'
    _sql_delete_by_pk = 'DELETE FROM {table} WHERE {pk}=%s'
    _sql_insert = 'INSERT INTO {table}({columns}) VALUES({values})'
    _sql_update = 'UPDATE {table} SET {values} WHERE {pk}=%s'


    @classmethod
    def create_by_request(cls, req):
        _kwargs = {}
        for _column in cls._columns:
            _kwargs[_column] = req.form.get(_column, req.args.get(_column, cls._defaults.get(_column, '')))
        return cls.create_object(**_kwargs)


    @classmethod
    def create_object(cls, *args, **kwargs):
        _obj = cls()
        for _key, _value in kwargs.items():
            setattr(_obj, _key, _value)
        return _obj


    @classmethod
    def query_all(cls, orderby='', offset=None, limit=None, query={}):
        _sql = cls._sql_query_all.format(columns=','.join(cls._columns), table=cls._table)
        _sql += ' AND %s' % query.get('sql', '1=1')
        _params = query.get('args', [])
        if orderby != '':
            _sql += ' ORDER BY %s' % orderby
        
        if limit is not None:
            _sql += ' LIMIT %s'
            _params.append(limit)

        if offset is not None:
            _sql += ' OFFSET %s'
            _params.append(offset)

        _cnt, _rs = cls.execute(_sql, _params, True)
        
        logger.info('query all:%s, %s, %s', _sql, _cnt, _rs)

        return _cnt, [cls.create_object(**dict(zip(cls._columns, _r))) for _r in _rs]


    @classmethod
    def query_count(cls, query={}):
        _sql = cls._sql_query_count.format(table=cls._table)
        _sql += ' AND %s' % query.get('sql', '1=1')
        _params = query.get('args', ())
        _cnt, _rs = cls.execute(_sql, _params, True)
        logger.info('query all:%s, %s, %s, %s', _sql, _cnt, _rs)
        return _cnt, _rs

    
    @classmethod
    def query_by_pk(cls, pk):
        _sql = cls._sql_query_by_pk.format(columns=','.join(cls._columns), table=cls._table, pk=cls._pk)
        _cnt, _rs = cls.execute(_sql, (pk, ), True)
        logger.info('query pk:%s, %s, %s, %s, %s', _sql, pk, _cnt, _rs)
        return cls.create_object(**dict(zip(cls._columns, _rs[0]))) if _cnt > 0 else None

    
    @classmethod
    def delete(cls, pk):
        _sql = cls._sql_delete_by_pk.format(columns=','.join(cls._columns), table=cls._table, pk=cls._pk)
        _cnt, _ = cls.execute(_sql, (pk, ))
        logger.info('delete:%s, %s, %s', _sql, _pk, _cnt)
        return _cnt > 0


    def create(self):
        _sql = self._sql_insert.format(table=self._table, columns=','.join(self._columns_add), values=','.join(['%s'] * len(self._columns_add)))
        _params = [getattr(self, _column, '') for _column in self._columns_add]
        print _sql, _params
        _cnt, _ = self.execute(_sql, _params)
        logger.info('create:%s, %s, %s', _sql, _params, _cnt)
        return _cnt > 0


    def update(self):
        _values = ['{column}=%s'.format(column=_column) for _column in self._columns_update if _column != self._pk]
        _params = [getattr(self, _column) for _column in self._columns_update if _column != self._pk]
        _sql = self._sql_update.format(table=cls._table, values=','.join(_values), pk=cls._pk)
        _cnt, _ = self.execute(_sql, _params)
        _params.append(getattr(self, self._pk))
        logger.info('update:%s, %s, %s', _sql, _params, _cnt)
        return _cnt > 0


    @classmethod
    def execute(cls, sql, args=(), is_fetch=False):
        return execute_sql(sql, args, is_fetch)
    

    def __str__(self):
        return json.dumps(self.__dict__)
