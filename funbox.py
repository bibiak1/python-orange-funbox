# this is my first class
# this class is created to hundle request to orange funbox

#import httplib
#httplib.HTTPConnection.debuglevel = 5

import urllib3, sys, json, Cookie
from time import sleep

class FunBox(object):
	def __init__(self, url, password, timeout=10, login='admin'):
		self.timeout = timeout
		self.url = url
		self.cookie = Cookie.SimpleCookie()
		self.ua = urllib3.PoolManager()
		self.h = { 'content-type': 'text/html',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
			'Accept': '*/*', 'DNT': '1' }

		try:
			r = self.ua.request('GET', url)
		except:
			print 'Error: getting page'
			sys.exit(-1)

		self.cookie.load(r.headers['set-cookie'].replace('/', '...'))
		ident = r.headers['set-cookie'][0:8]

		sleep(1)

		newurl = self.url + '/authenticate?username=' + login + '&password=' + password
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { 'username': login, 'password': password }

		try:
			r = self.ua.request('POST', newurl, fields=data, headers=self.h)
		except:
			print 'Error: auth'
			sys.exit(-1)

		self.cookie.load(r.headers['set-cookie'].replace('/', '...'))
		contextID = json.loads(r.data.decode('utf-8'))['data']['contextID'].encode('ascii','ignore')
		self.h['X-Context'] = contextID
		self.cookie.load(ident + '...login=admin')
		self.cookie.load(ident + '...context=' + contextID)

	def deviceinfo(self):
		newurl = self.url + '/sysbus/DeviceInfo'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { "parameters": {} }

		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: deviceinfo'
			return False

		return json.loads(r.data)

	def gethosts(self):
		newurl = self.url + '/sysbus/Hosts:getDevices'
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { "parameters": {} }

		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: deviceinfo'
			return False

		return json.loads(r.data)

	def devicesget(self, data={"parameters":{"expression":{"usbM2M":" usb && wmbus and .Active==true","usb":" printer && physical and .Active==true","usblogical":"volume && logical and .Active==true","wifi":"wifi && edev and .Active==true","eth":"eth && edev and .Active==true","dect":"voice && dect && handset && physical"}}}):
		newurl = self.url + '/sysbus/Devices:get'
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
	
		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: deviceinfo'
			return False

		return json.loads(r.data)

	def destroydevice(self, hostmacaddress):
		newurl = self.url + '/sysbus/Devices:destroyDevice'
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { "parameters": { "key": hostmacaddress} }	
	
		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: deviceinfo'
			return False

		return json.loads(r.data)

	def getwanstatus(self):
		newurl = self.url + '/sysbus/NMC:getWANStatus'
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { "parameters": {} }

		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: deviceinfo'
			return False

		return json.loads(r.data)

	def disconnect(self):
		newurl = self.url + '/sysbus/NeMo/Intf/data:setFirstParameter'
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { "parameters": { "name": "Enable", "value": 0, "flag": "ppp", "traverse": "down"}}

		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: stop'
			return False

		return json.loads(r.data)

	def connect(self):
		newurl = self.url + '/sysbus/NeMo/Intf/data:setFirstParameter'
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { "parameters": { "name": "Enable", "value": 1, "flag": "ppp", "traverse": "down"}}
		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: stop'
			return False

		return json.loads(r.data)

	def reconnect(self):
		self.disconnect()
		sleep(self.timeout)
		return self.connect()

	def restart(self):
		newurl = self.url + '/sysbus/NMC:reboot'
		self.h['content-type'] = 'application/x-sah-ws-1-call+json'
		self.h['Cookie'] = '; '.join(self.cookie.output(attrs=[], header='').replace('...', '/').split())
		data = { "parameters": {} }

		try:
			r = self.ua.request('POST', newurl, body=json.dumps(data).encode('utf-8'), headers=self.h)
		except:
			print 'Error: deviceinfo'
			return False

		return True

#vim: set ts=4
