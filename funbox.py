# this is my first class
# this class is created to hundle request to orange funbox

#import httplib
#httplib.HTTPConnection.debuglevel = 5

import urllib3, sys, json, Cookie
from time import sleep

class FunBox(object):
    def get(self, url):
        try:
            r = self.ua.request('GET', self.url + url)
        except:
            print 'Error: get (url: ' + url + ')'
            sys.exit(-1)

        self.cookie.load(r.headers['set-cookie'].replace('/', '...'))
        self.ident = r.headers['set-cookie'][0:8]
        return r
 
    def post(self, url, data={}):
        newurl = self.url + url
        self.h['content-type'] = 'application/x-sah-ws-1-call+json'
        self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())

        try:
            r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
        except:
            print 'Error: post (url: ' + url + ')'
            sys.exit(-1)

        return r

    def authenticate(self, login, password):
        self.get("/")
        sleep(1)
        r = self.post('/authenticate?username=' + login + '&password=' + password, { 'username': login, 'password': password })
        self.cookie.load(r.headers['set-cookie'].replace('/', '...'))
        contextID = json.loads(r.data.decode('utf-8'))['data']['contextID'].encode('ascii','ignore')
        self.h['X-Context'] = contextID
        self.cookie.load(self.ident + '...login=admin')
        self.cookie.load(self.ident + '...context=' + contextID)

    def __init__(self, url, password, timeout=10, login='admin'):
        self.timeout = timeout
        self.url = url
        self.cookie = Cookie.SimpleCookie()
        self.ua = urllib3.PoolManager()
        self.h = { 'content-type': 'text/html' }

        self.authenticate(login, password)

    def deviceinfo(self):
        r = self.post('/sysbus/DeviceInfo', { "parameters": {} })
        return json.loads(r.data)

    def gethosts(self):
        r = self.post('/sysbus/Hosts:getDevices', { "parameters": {} })
        return json.loads(r.data)

    def devicesget(self, data={"parameters":{"expression":{"usbM2M":" usb && wmbus and .Active==true","usb":" printer && physical and .Active==true","usblogical":"volume && logical and .Active==true","wifi":"wifi && edev and .Active==true","eth":"eth && edev and .Active==true","dect":"voice && dect && handset && physical"}}}):
        r = self.post('/sysbus/Devices:get', data)
        return json.loads(r.data)

    def destroydevice(self, hostmacaddress):
        r = self.post('/sysbus/Devices:destroyDevice', { "parameters": { "key": hostmacaddress} })
        return json.loads(r.data)

    def getwanstatus(self):
        r = self.post('/sysbus/NMC:getWANStatus', { "parameters": {} })
        return json.loads(r.data)

    def disconnect(self):
        r = self.post('/sysbus/NeMo/Intf/data:setFirstParameter', { "parameters": { "name": "Enable", "value": 0, "flag": "ppp", "traverse": "down"}})
        return json.loads(r.data)

    def connect(self):
        r = self.post('/sysbus/NeMo/Intf/data:setFirstParameter', { "parameters": { "name": "Enable", "value": 1, "flag": "ppp", "traverse": "down"}})
        return json.loads(r.data)

    def reconnect(self):
        self.disconnect()
        sleep(self.timeout)
        return self.connect()

    def restart(self):
        r = self.post('/sysbus/NMC:reboot', { "parameters": {} })
        return True

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
