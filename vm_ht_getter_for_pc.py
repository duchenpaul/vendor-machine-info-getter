import vm_ht_getter
import configparser

try:
	config = configparser.ConfigParser()
	config.read('config.ini')
except Exception as e:
	print("Error read config file, check config.ini")
	sys.exit(1)




for profile in config.sections():
	if not profile.startswith('USER_'):
		continue

	print('..........................')
	machineName = config[profile]['username']
	print("Check: " + machineName)
	vm_ht = vm_ht_getter.ht_getter(machineName, config[profile]['password'])
	vm_ht.login()
	# print('last status: ' + read_log_status(machineName))

	# vm_ht.auto_login()
	status = vm_ht.check_status()
	print(status)
	# print(status['machine_status'])

	print(machineName + ": " + str(status))


