#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
import sys
class zabbixtools:
    def __init__(self):
        self.url = "http://x.x.x.x/zabbix/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.authID = self.user_login()
    def user_login(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": "xddd",
                        "password": "xddh.com"
                        },
                    "id": 0
                    })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, Please Check Your Name And Password:",e.code
        else:
            response = json.loads(result.read())
            result.close()
            authID = response['result']
            return authID

    def get_data(self,data,hostip=""):
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            return response


    def hosts_get_cpuids(self,hostid):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": "itemids",
                        "hostids":hostid,
                        "search":{"key_":"system.cpu.util"}
                        },
                    "auth": self.authID,
                    "id": 1,
                    })
        res = self.get_data(data)
        if 'result' in res.keys():
            res = res['result'][0]['itemid']
	    return res

    def hosts_get_resource(self,hostid):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "history.get",
                    "params": {
                        "output": "extend",
                        "history":"0",
                        "itemids":hostid,
                        "limit":"10"
                        },
                    "auth": self.authID,
                    "id": 1,
                    })
        res = self.get_data(data)#['result']
        if 'result' in res.keys():
            res = res['result'][0]['value']
	    return res

    def get_all_host_and_ip(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                        "output": ['hostid','host'],
                        "selectInterfaces":['interfaceid','ip']
                        },
                    "auth": self.authID,
                    "id": 1,
                    })
        res = self.get_data(data)#['result']
        if 'result' in res.keys():
            res = res['result']
            for host in res:
		 hostid=host['hostid']
		 if hostid != '':
  		 	itemids=self.hosts_get_cpuids(hostid)
	         	hostcpu=self.hosts_get_resource(itemids)	
		 	print host['interfaces'][0]['ip'],hostcpu
		

def main():
    test = zabbixtools()
    test.get_all_host_and_ip()
if __name__ == "__main__":
    main()
