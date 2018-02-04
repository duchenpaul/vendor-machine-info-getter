#!/usr/bin/env python3
import vm_ht_getter, vm_ht_txn_his
import configparser
from indicator import LED_indicator
from send_mail import send_mail
import logging, time
import os.path, os, ast, sys
from insert_into_DB import db_append_status

alarmTrigger = 1
log_into_DB_Trigger = 1

def create_dir(dir_name):
	path_name = "{}/{}".format(os.path.dirname(os.path.realpath(__file__)), dir_name)
	not os.path.exists(path_name) and os.mkdir(path_name)

# LOG = './batch_getter_{}.log'.format(time.strftime("%Y%m%d_%H%M%S"))
create_dir('log')
LOG = './log/batch_getter_{}.log'.format(time.strftime("%Y%m%d"))

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = LOG,
					level = logging.INFO,
					format = LOG_FORMAT,
					filemode = 'a') 
logger = logging.getLogger()

# redirect print into file. PART A
orig_stdout = sys.stdout
f = open(LOG, 'a')
sys.stdout = f


def print(text, level = 'Info'):
	# print('[ {} ]: {}'.format(level, text))
	if level == 'Info':
		logger.info(text)
	elif level == 'Error':
		logger.error(text)
	else:
		logger.debug(text)



try:
	config = configparser.ConfigParser()
	config.read('config.ini')
except Exception as e:
	print("Error read config file, check config.ini")
	sys.exit(1)

distri_list = config['mail']['distri_list']

status_dict = {}

def alarm(last_status, current_status):
	'''Send notifications when status changes'''
	if (alarmTrigger == 0) or (not os.path.isfile('./log/last_status.log')):
		return
	print("last_status: " + last_status) 
	print("current_status: " + current_status)
	if (last_status == '[在线]') and (current_status == '[离线]'):
		send_mail('[Vender Machi] Offline', '{} is offline on {}. Last seen: {}'.format(machineName,  time.asctime(time.localtime(time.time())), status['last_response_date']), None, distri_list)
	elif (last_status == '[离线]') and (current_status == '[在线]'):
		send_mail('[Vender Machi] Online', '{} is back online on {}. '.format(machineName,  time.asctime( time.localtime(time.time()) )), None, distri_list)
	elif (last_status != 'Cookie_Invalid') and (current_status == 'Cookie_Invalid'):
		send_mail('[Vender Machi] Cookie Expired', 'Failed to log into {}, cookie is expired on {}. '.format(machineName,  time.asctime( time.localtime(time.time()) )), None, distri_list)
	else:
		print("Status not changed")
	vm_ht_txn_his.check_txn_his()


	
def read_log_status(machineName):
	if os.path.isfile('./log/last_status.log'):
		with open('./log/last_status.log', 'r') as f_read:
			lastStatus = f_read.read()
		lastStatusDict = ast.literal_eval(lastStatus)
		try:
			return lastStatusDict[machineName]['machine_status']
		except Exception as e:
			return "Error"
		

def log_status():
	with open('./log/last_status.log', 'w') as f:
		f.write(str(status_dict))

def append_status(machine_name, machine_status, last_response_date):
	db_append_status(machine_name, machine_status, last_response_date)



print(("======================{}====================").format(time.strftime("%Y/%m/%d %H:%M:%S")))


No = 1
LED_VM_Mapping = {
	1 : [0, 2],
	2 : [0, 5]
}


for profile in config.sections():
	if not profile.startswith('USER_'):
		continue

	print('..........................')
	machineName = config[profile]['username']
	print("Check: " + machineName)
	s = LED_indicator(LED_VM_Mapping[No])
	vm_ht = vm_ht_getter.ht_getter(machineName, config[profile]['password'])
	# vm_ht.login()
	# print('last status: ' + read_log_status(machineName))

	try:
		vm_ht.auto_login()
		s.set_logged_in()
		status = vm_ht.check_status()
		# print(status)
		# print(status['machine_status'])
		if status['machine_status'] == '[在线]':
			s.set_online()
		else:
			s.set_offline()
			# send_mail('[Vender Machi]', '{} is offline. '.format(machineName), None, distri_list)

		print(machineName + ": " + str(status))
	except Exception as e:
		'''Cookie invalid'''
		print('Cookie_Invalid')
		s.set_error()
		status = {'machine_status': 'Cookie_Invalid', 'last_response_date': '00-00 00:00:00'}
		# send_mail('[Vender Machi]', 'Failed to log into {}, cookie is expired. '.format(machineName), None, distri_list)
	
	alarm(read_log_status(machineName), status['machine_status'])
	status_dict[machineName] = status
	append_status(machineName, status['machine_status'], status['last_response_date'])
	No += 1


log_status()
print("=======================================================================\n\n")

# redirect print into file. PART B
sys.stdout = orig_stdout
f.close()