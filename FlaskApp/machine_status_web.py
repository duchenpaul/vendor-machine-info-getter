#!/usr/bin/env python3
import MySQLdb as mysql
import json, configparser, sys
from flask import Flask,request,render_template
from datetime import datetime
app = Flask(__name__)

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
	

db = mysql.connect(**config)
db.autocommit(True)

cursor = db.cursor()

class ComplexEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			# return obj.strftime('%Y-%m-%d %H:%M:%S')
			return obj.timestamp()
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		else:
			return json.JSONEncoder.default(self, obj)

@app.route('/',methods=['GET','POST'])
def hello():
	sql = ''
	if request.method == 'POST':
		data = request.json
		try:
			sql = "insert into stat(host,mem_free,mem_usage,mem_total,load_avg,time) values ('%s',%d,%d,%d,'%s',%d)" % (data['Host'],data['MemFree'],data['MemUsage'],data['MemTotal'],data['LoadAvg'],int(data['Time']))
			ret = cursor.execute(sql)
		except mysql.IntegrityError:
			pass
		return 'OK'
	else:
		cursor.execute('select unix_timestamp(db_insert_date), machine_status from tbl_vm_status')
		ones = [[i[0]*1000,i[1]] for i in cursor.fetchall()]
		print(json.dumps(ones, cls=ComplexEncoder))
		return render_template('mon.html',data=json.dumps(ones, cls=ComplexEncoder))


@app.route('/new',methods=['GET'])
def getnew():
	cursor.execute('select unix_timestamp(db_insert_date), machine_status from tbl_vm_status  order by db_insert_date desc limit 1')
	v = cursor.fetchone()
	top = [v[0]*1000,v[1]]
	print(top)
	return json.dumps(top, cls=ComplexEncoder)




# app.run(port=5000,debug=True)
app.run(port=5000, host='0.0.0.0', debug=True)
