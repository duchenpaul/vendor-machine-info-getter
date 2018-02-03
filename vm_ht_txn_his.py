import vm_ht_getter
import bs4 as bs
# import pandas as pd
import csv, codecs
import configparser
import hashlib, shutil
from pathlib import Path
from send_mail import send_mail


try:
	config = configparser.ConfigParser()
	config.read('config.ini')
except Exception as e:
	print("Error read config file, check config.ini")
	sys.exit(1)

distri_list = config['mail']['distri_list']

def get_tables(his_table_raw, csv_file):
	'''Get the tables from html, and export to csv'''
	soup = bs.BeautifulSoup(his_table_raw, 'lxml')
	# his_table = soup.select('#checkList')
	his_table = soup.table
	# print(his_table)
	his_table_row = his_table.find_all('tr')

	with codecs.open(csv_file, 'w', 'utf_8_sig') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['机器编号','货道','交易号','支付方式','销售金额(元)','成本(元)','利润(元)','商品名称','销售数量','销售时间','传输时间'])

		for tr in his_table_row[2: ]:
			td = tr.find_all('td')
			row = [ i.text for i in td ]
			writer.writerow(row)

# def get_tables_pd(his_table_raw):
# 	dfs = pd.read_html(his_table_raw, header = 0)
# 	for df in dfs:
# 		print(df.values.tolist())

def chk_md5(file1, file2):
	'''Check md5 of 2 files, if it is the same, return True.'''
	if (not Path(file1).is_file()) or (not Path(file2).is_file()):
		return False
	digests = []
	for filename in [file1, file2]:
		hasher = hashlib.md5()
		with open(filename, 'rb') as f:
			buf = f.read()
			hasher.update(buf)
			a = hasher.hexdigest()
			digests.append(a)
			# print(a)
	return(digests[0] == digests[1])

def get_lastest_txn(csv_file):
	txn_list = []
	item_list = []
	with open(csv_file, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			# print(row)
			txn_list.append(row)
	for item in txn_list[1:6]:
		# print(item[7] + ', ' + item[9])
		item_list.append(item[7] + ' sold on ' + item[9])

	return('\n'.join(item_list))

def refresh_last(trx_his_last, trx_his_curr):
	try:
		Path(trx_his_curr).resolve()
		shutil.move(trx_his_curr, trx_his_last)
	except FileNotFoundError:
		return

def check_txn_his():
	for profile in config.sections():
		if not profile.startswith('USER_'):
			continue

		print('..........................')
		machineName = config[profile]['username']
		trx_his_last = 'trx_his_last_{}.csv'.format(machineName)
		trx_his_curr = 'trx_his_{}.csv'.format(machineName)
		refresh_last(trx_his_last, trx_his_curr)
		print("Check: " + machineName)
		vm_ht = vm_ht_getter.ht_getter(machineName, config[profile]['password'])
		# vm_ht.login()
		vm_ht.auto_login()
		his_table_raw = vm_ht.webpage_get('http://ht.jj1001.com/?a=order&m=history').content.decode('utf-8')
		get_tables(his_table_raw, trx_his_curr)
		# print(his_table_raw)

		if not chk_md5(trx_his_curr, trx_his_last):
			print('New Txn Updated')
			send_mail('[Vender Machi] Good Sold', '{} sold a good just now.\n {}) '.format(machineName, get_lastest_txn(trx_his_curr)), trx_his_curr, distri_list)
		else: 
			print('No New Txn Updated')

if __name__ == '__main__':
	check_txn_his()