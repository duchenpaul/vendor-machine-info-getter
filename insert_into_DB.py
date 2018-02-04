#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import datetime, configparser

try:
	configRead = configparser.ConfigParser()
	configRead.read('config.ini')
	config = {
		'host': configRead['datebase']['host'],
		'port': int(configRead['datebase']['port']),
		'user': configRead['datebase']['user'],
		'passwd': configRead['datebase']['passwd'],
		'db': configRead['datebase']['db'],
		'charset': 'utf8'
	}
except Exception as e:
	print("Error read config file, check config.ini")
	sys.exit(1)

def db_append_status(machine_name, machine_status, last_response_date):
	'''insert machine status into the table'''
	machine_name = machine_name
	if machine_status == '[在线]':
		machine_status = 1
	elif machine_status == '[离线]':
		machine_status = 0
	else:
		machine_status = 2
		
	last_response_date = datetime.datetime.now().strftime('%Y') + '-' + last_response_date

	sql = "INSERT INTO tbl_vm_status (machine_name, machine_status, last_response_date, db_insert_date) VALUES ('{}', {},  STR_TO_DATE('{}', '%Y-%m-%d %H:%i:%s'), now());".format(machine_name, machine_status, last_response_date)

	# with open("D:\python_test\MySQL\DELETE.sql") as sql_file:
	#     DELETE_SQL = sql_file.read().format('Chenny')
	#     # print(DELETE_SQL)

	EXEC_SQL = sql

	db = MySQLdb.connect(**config)
	cursor = db.cursor()
	try:
		cursor.execute(EXEC_SQL)
	except Exception as e:
		print("Execute {} fail!".format(EXEC_SQL))
		print(e)
		db.rollback()
	else:
		print("All good!")
		db.commit()
	finally:
		print('Closing DB conn')
		db.close()