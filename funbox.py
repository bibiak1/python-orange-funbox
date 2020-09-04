# this is my first class
# this class is created to hundle request to orange funbox

#import httplib
#httplib.HTTPConnection.debuglevel = 5

import urllib3, sys, json, re
try:
	import Cookie
except:
	import http.cookies as Cookie
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
        print('Error: get (url: ' + url + ')')
        sys.exit(-1)

    if 'set-cookie' in r.headers:
        cookie.load(r.headers['set-cookie'].replace('/', '...'))

    return r
     
def uapost(url, data):
    global ua, h, timeout

    h['content-type'] = 'application/x-sah-ws-1-call+json'
    h['Cookie'] = '; '.join(cookie.output(attrs=[], header='').replace('...', '/').split())

    try:
        encoded_data = json.dumps(data).encode('utf-8')
        r = ua.request('POST', url, body=encoded_data, headers=h)
    except Exception as e:
        print('Error: post (url: ' + url + ') :: ' + str(e))
        sys.exit(-1)

    return r

class Hosts(object):
    def getDevices(self):
        r = self.uapost(':getDevices')
        return json.loads(r.data.decode('utf-8'))

    def delHost(self, hostmacaddress):
        r = self.uapost(':delHost', { "parameters": { "physAddress": hostmacaddress } })
        return json.loads(r.data.decode('utf-8'))    

    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data={ "parameters": {} }):
        return uapost(self.url + url, data)
       
    def __init__(self, url):
        self.url = url
     
class Devices(object):
    def get(self, data={"parameters":{"expression":{"usbM2M":" usb && wmbus","usb":" printer && physical","usblogical":"volume && logical","wifi":"wifi && edev","eth":"eth && edev","dect":"voice && dect && handset && physical"}}}):
        r = self.uapost(':get', data)
        return json.loads(r.data.decode('utf-8', 'replace'), strict=False)

    def destroyDevice(self, hostmacaddress):
        r = self.uapost(':destroyDevice', { "parameters": { "key": hostmacaddress } })
        return json.loads(r.data.decode('utf-8'))

    def setName(self, physAddress, name):
        physAddress = physAddress.upper()
        r = self.uapost('/Device/' + physAddress + ':setName', { "parameters": { "name": name } })
        for i in ['webui']:
            r = self.uapost('/Device/' + physAddress + ':setName', { "parameters": { "name": name, "source": i } })
        return json.loads(r.data.decode('utf-8'))

    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data={ "parameters": {} }):
        return uapost(self.url + url, data)
       
    def __init__(self, url):
        self.url = url

class interface_object(object):
    def getDSLStats(self):
        r = self.uapost(':getDSLStats')

        return json.loads(r.data.decode('utf-8'))

    def setFirstParameter(self, data):
        r = self.uapost(':setFirstParameter', data)

        return json.loads(r.data.decode('utf-8'))

    def getMIBs(self, name):
        r = self.uapost(':getMIBs', {"parameters": {"mibs": name}})

        return json.loads(r.data.decode('utf-8'))

    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data={ "parameters": {} }):
        return uapost(self.url + url, data)

    def __init__(self, url):
        self.url = url

class Intf(object):
    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data={ "parameters": {} }):
        return uapost(self.url + url, data)

    def __init__(self, url):
        self.url = url
        self.data = interface_object(url + '/data')
        self.dsl0 = interface_object(url + '/dsl0')
        self.lan = interface_object(url + '/lan')
        self.wwan = interface_object(url + '/wwan')
        self.wl0 = interface_object(url + '/wl0')
        self.wl1 = interface_object(url + '/wl1')

class NeMo(object):
    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data={ "parameters": {} }):
        return uapost(self.url + url, data)

    def __init__(self, url):
        self.url = url
        self.Intf = Intf(url + '/Intf')

class Wifi(object):
    def get(self):
        r = self.uapost(':get')
        j = json.loads(r.data.decode('utf-8'))
        self.Status = j['result']['status']['Status']
        self.ConfigurationMode = j['result']['status']['ConfigurationMode']
        self.Enable = j['result']['status']['Enable']

        return j

    def getStats(self):
        r = self.uapost(':getStats')

        return json.loads(r.data.decode('utf-8'))

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
        return json.loads(r.data.decode('utf-8'))

    def checkForUpgrades(self):
        r = self.uapost(':checkForUpgrades')
        return json.loads(r.data.decode('utf-8'))

    def reboot(self):
        self.uapost(':reboot')

        return True

    def setLANIP(self, Address, Netmask, DHCPEnable, DHCPMinAddress, DHCPMaxAddress):
        r = self.uapost(':setLANIP', { "parameters": { "Address": Address, "Netmask": Netmask, "DHCPEnable": DHCPEnable, "DHCPMinAddress": DHCPMinAddress, "DHCPMaxAddress": DHCPMaxAddress } })

        return json.loads(r.data.decode('utf-8'))

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
        try:
            contextID = json.loads(r.data.decode('utf-8'))['data']['contextID'].encode('ascii','ignore')
            h['X-Context'] = contextID
            ident = r.headers['set-cookie'][0:8]
            cookie.load(ident + '...login=admin')
            cookie.load(ident + '...context=' + contextID)
        except:
            contextID = json.loads(r.data.decode('utf-8'))['data']['contextID']
            h['X-Context'] = contextID
            ident = r.headers['set-cookie'][0:8]
            cookie.load(ident + '...login=admin')
            cookie.load(ident + '...context=' + contextID)


    def DeviceInfo(self):
        r = self.uaget('/sysbus/DeviceInfo?_restDepth=-1')
        return json.loads(r.data.decode('utf-8'))

    def disconnect(self):
        r = self.NeMo.Intf.data.setFirstParameter({ "parameters": { "name": "Enable", "value": 0, "flag": "ppp", "traverse": "down"}})
        return r

    def connect(self):
        r = self.NeMo.Intf.data.setFirstParameter({ "parameters": { "name": "Enable", "value": 1, "flag": "ppp", "traverse": "down"}})
        return r

    def reconnect(self):
        self.disconnect()
        sleep(self.timeout)
        return self.connect()

    def restart(self):
        self.NMC.reboot()
        return True

    def uaget(self, url):
        return uaget(self.url + url)

    def uapost(self, url, data = { "parameters": {} }):
        return uapost(self.url + url, data)

    def __init__(self, url, password, ntimeout=10, login='admin'):
        global timeout

        self.url = url
        timeout = ntimeout
        self.timeout = ntimeout

        self.authenticate(login, password)
        self.NMC = NMC(self.url + '/sysbus/NMC')
        self.Hosts = Hosts(self.url + '/sysbus/Hosts')
        self.Devices = Devices(self.url + '/sysbus/Devices')
        self.NeMo = NeMo(self.url + '/sysbus/NeMo')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
