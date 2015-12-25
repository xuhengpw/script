#coding=utf-8
import MySQLdb as mysql
con = mysql.connect(user='root',\
                    passwd='',\
                    db='log',\
                    host='localhost')
con.autocommit(True)
cur = con.cursor()
f = open('www_access_20140823.log')
res = {}
for l in f:
    arr = l.split(' ')        # 获取ip url 和status
    ip = arr[0]
    url = arr[6]
    status = arr[8]        # ip url 和status当key，每次统计+1
    res[(ip,url,status)] = res.get((ip,url,status),0)+1
    # 生成一个临时的list
    
res_list = [(k[0],k[1],k[2],v) for k,v in res.items()]
  
for s in res_list:
    sql = 'insert log values ("%s","%s",%s,%s)' % s
    try:
        #  入库
        cur.execute(sql)
    except Exception, e:
        pass