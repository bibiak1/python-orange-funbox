# python-orange-funbox

How to use this package:

1. to initialize:
funbox = funbox.FunBox("http://192.168.1.1", "admin")

2. to reconnect
funbox.reconnect()

3. to restart router
funbox.restart()

4. to get info about connected devices
hosts = funbox.devicesget()

for type in hosts['result']['status']:
	print type + ' :::'
	for host in hosts['result']['status'][type]:
		name = host['Name']
		physAddress = host['PhysAddress']
		ipAddress = host['IPAddress']
		print '\t' + name + ' :: ' + physAddress + ' :: ' + ipAddress

5 to get info about defined hosts
hosts = funbox.gethosts()

for host in hosts['result']['status']:
	hostName = host['hostName']
	physAddress = host['physAddress']
	ipAddress = host['ipAddress']

	print hostName + ' :: ' + physAddress + ' :: ' + ipAddress

That's all for now. More to come
