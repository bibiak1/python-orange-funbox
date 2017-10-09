# this is my first class
# this class is created to hundle request to orange funbox

#import httplib
#httplib.HTTPConnection.debuglevel = 5

import urllib3, sys, json, Cookie
from time import sleep

cookie = Cookie.SimpleCookie()
ua = urllib3.PoolManager()
h = { 'content-type': 'text/html' }
timeout = 10

def uaget(url):
    global ua, h, timeout

    try:
        r = ua.request('GET', url)
    except:
        print 'Error: get (url: ' + url + ')'
        sys.exit(-1)

    cookie.load(r.headers['set-cookie'].replace('/', '...'))
    return r
     
def uapost(url, data):
    global ua, h, timeout

    h['content-type'] = 'application/x-sah-ws-1-call+json'
    h['Cookie'] = '; '.join(cookie.output(attrs=[], header='').replace('...', '/').split())

    try:
        r = ua.request('POST', url, body=json.dumps(data).encode('utf-8'), headers=h)
    except:
        print 'Error: post (url: ' + url + ')'
        sys.exit(-1)

    return r

class Wifi(object):
    def get(self):
        r = self.uapost(':get')
        j = json.loads(r.data)
        self.Status = j['result']['status']['Status']
        self.ConfigurationMode = j['result']['status']['ConfigurationMode']
        self.Enable = j['result']['status']['Enable']
        return j

    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data={ "parameters": {} }):
        return uapost(self.url + url, data)
       
    def __init__(self, url):
        self.url = url
        self.Status = "Unknown"
        self.ConfigurationMode = "Unknown"
        self.Enable = "Unknown"
    
class NMC(object):
    def getWANStatus(self):
        r = self.uapost(':getWANStatus')
        return json.loads(r.data)

    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data={ "parameters": {} }):
        return uapost(self.url + url, data)
       
    def __init__(self, url):
        self.url = url
        self.Wifi = Wifi(url + '/Wifi')

class FunBox(object):
    def authenticate(self, login, password):
        global cookie, h, ident

        self.uaget("/")
        sleep(1)
        r = self.uapost('/authenticate?username=' + login + '&password=' + password, { 'username': login, 'password': password })
        cookie.load(r.headers['set-cookie'].replace('/', '...'))
        contextID = json.loads(r.data.decode('utf-8'))['data']['contextID'].encode('ascii','ignore')
        h['X-Context'] = contextID
        ident = r.headers['set-cookie'][0:8]
        cookie.load(ident + '...login=admin')
        cookie.load(ident + '...context=' + contextID)

    def DeviceInfo(self):
        r = self.uapost('/sysbus/DeviceInfo')
        return json.loads(r.data)

    def gethosts(self):
        r = self.uapost('/sysbus/Hosts:getDevices')
        return json.loads(r.data)

    def devicesget(self, data={"parameters":{"expression":{"usbM2M":" usb && wmbus and .Active==true","usb":" printer && physical and .Active==true","usblogical":"volume && logical and .Active==true","wifi":"wifi && edev and .Active==true","eth":"eth && edev and .Active==true","dect":"voice && dect && handset && physical"}}}):
        r = self.uapost('/sysbus/Devices:get', data)
        return json.loads(r.data)

    def destroydevice(self, hostmacaddress):
        r = self.uapost('/sysbus/Devices:destroyDevice', { "parameters": { "key": hostmacaddress} })
        return json.loads(r.data)

    def disconnect(self):
        r = self.uapost('/sysbus/NeMo/Intf/data:setFirstParameter', { "parameters": { "name": "Enable", "value": 0, "flag": "ppp", "traverse": "down"}})
        return json.loads(r.data)

    def connect(self):
        r = self.uapost('/sysbus/NeMo/Intf/data:setFirstParameter', { "parameters": { "name": "Enable", "value": 1, "flag": "ppp", "traverse": "down"}})
        return json.loads(r.data)

    def reconnect(self):
        self.disconnect()
        sleep(self.timeout)
        return self.connect()

    def restart(self):
        self.uapost('/sysbus/NMC:reboot')
        return True

    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data):
        return uapost(self.url + url, data={ "parameters": {} })

    def __init__(self, url, password, ntimeout=10, login='admin'):
        global timeout

        self.url = url
        timeout = ntimeout

        self.authenticate(login, password)
        self.NMC = NMC(self.url + '/sysbus/NMC')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
