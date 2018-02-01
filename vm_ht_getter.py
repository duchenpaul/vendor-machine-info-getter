import requests
from requests import Request, Session
import requests.utils, pickle
# import cv2, os.path 
import os.path 
from os.path import dirname, abspath
import bs4 as bs
import re, time

url = 'http://ht.jj1001.com'
# SCRIPT_PATH = 'D:\\python_test\\vm_ht_getter\\'
SCRIPT_PATH = dirname(abspath(__file__)) + '/'


headers = {
'Host': 'ht.jj1001.com',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
'Referer': 'http://ht.jj1001.com/?a=index&m=login',
'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}

mobile_headers = {
	'Host': 'ht.jj1001.com',
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Referer': 'http://ht.jj1001.com/?a=index&m=left',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}


class ht_getter:
	headers_default = {
		'Host': 'ht.jj1001.com',
		'Connection': 'keep-alive',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
		'Referer': 'http://ht.jj1001.com/?a=index&m=login',
		'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
		}

	cookies_dict = {}

	def __init__(self, username, password):
		self.Sess = requests.session()
		self.username = username
		self.password = password
		self.cookie_file = SCRIPT_PATH + 'cookies_{}.txt'.format(self.username)
		# print(self.cookie_file)


	def webpage_get(self, url, headers=headers_default):
		# print("Get: " + url)
		self.resp = self.Sess.get(url, headers=headers)		
		return self.resp

	def webpage_post(self, url, data, headers=headers_default):
		self.req = Request('POST', url, data=data, headers=headers)
		self.prepped = self.Sess.prepare_request(self.req)
		self.resp = self.Sess.send(self.prepped)
		return self.resp


	def input_captcha(self, response):
		captcha_img = SCRIPT_PATH + 'Captcha_new.png'
		with open(captcha_img, 'wb') as f:
			f.write(response)
		time.sleep(.01)

		try:
			import cv2
			img = cv2.imread(captcha_img, 0)
			cv2.imshow("Captcha", img)

			cv2.waitKey(25)
			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				
			captcha = input('Input the captcha: ')
			cv2.destroyAllWindows()
		except Exception as e:
			captcha = input('Input the captcha: ')
		return captcha

	def login_w_pass(self):
		self.url = 'http://ht.jj1001.com/'
		self.resp = self.webpage_get(self.url)
		self.cookies_dict.update(self.resp.cookies)
		print(str(self.cookies_dict))

		print('Fetching captcha...')
		self.url = 'http://ht.jj1001.com/?a=index&m=randcode'
		self.resp = self.webpage_get(self.url)
		self.cookies_dict.update(self.resp.cookies)
		print(str(self.cookies_dict))
		self.captcha = self.input_captcha(self.resp.content)
		self.url = 'http://ht.jj1001.com/?a=index&m=login'
		self.data = 'username={}&password={}&verify={}&a=index&m=login'.format(self.username, self.password, self.captcha)
		self.headers = {
		'Host': 'ht.jj1001.com',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Origin': 'http://ht.jj1001.com',
		'Upgrade-Insecure-Requests': '1',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Referer': 'http://ht.jj1001.com/?a=index&m=login',
		'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',

		}

		self.resp = self.webpage_post(self.url, self.data, self.headers)
		self.login_rtn_page = self.resp.content.decode('utf-8')

		if '登录成功' in self.login_rtn_page:
			print('Authentication succeed!')
			self.cookies_dict.update(self.resp.cookies)
			# print(self.cookies_dict)

			# with open(self.cookie_file, 'wb') as f:
			# 	pickle.dump(self.cookies_dict, f)
			with open(self.cookie_file, 'w') as f:
				f.write(str(self.cookies_dict))

	def login_w_cookies(self):
		self.url  = 'http://ht.jj1001.com/'
		# with open(self.cookie_file, 'rb') as f:
		# 	print("Reading cookie...")
		# 	cookies_bin = pickle.load(f)
		with open(self.cookie_file, 'r') as f:
			# print("Reading cookie {}...".format(self.cookie_file))
			cookies_bin = f.read()
			self.Sess.cookies.update(eval(cookies_bin))
			# print(cookies_bin)
		self.resp = self.Sess.get(self.url)
		# print(self.resp.content.decode('utf-8'))

	def login(self):
		'''
		Auto login with cookies, if cookie is invalid, use password and captcha to login.
		'''
		try:
			self.login_w_cookies()
			# print(self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'))
			if self.username.upper() not in self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'):
				raise cookie_expired
		except Exception as e:
			self.Sess = requests.session()
			self.login_w_pass()

		# print(self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'))

		if self.username.upper() in self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'):
			print("Login Success!")

	def auto_login(self):
		'''
		Auto login with cookies, if cookie is invalid, quit the process.
		'''
		try:
			self.login_w_cookies()
			# print(self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'))
			if self.username.upper() not in self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'):
				raise cookie_expired
		except Exception as e:
			# print(e)
			pass

		# print(self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'))

		if self.username.upper() in self.webpage_get('http://ht.jj1001.com/?a=index&m=top').content.decode('utf-8'):
			print("Login Success!")

	def check_status(self):
		machine_status_page = self.webpage_get('http://ht.jj1001.com/?a=machine&m=status', mobile_headers).content.decode('utf-8')
		soup = bs.BeautifulSoup(machine_status_page, 'lxml')
		# tgt = soup.body.find('div', attrs={'class':'ui-block-c center'}).
		machine_status = soup.select('#list_view > li > h2 > div > div.ui-block-c.center > span')[0].get_text()
		# last_response_list = soup.select('#list_view > li > h2 > div > div.ui-grid-a')[0]
		last_response_date = soup.select('#list_view > li > h2 > div > div > div ')[-2].get_text()
		return {"machine_status": machine_status, "last_response_date": last_response_date}


class cookie_expired(Exception):
	def __init__(self):
		Exception.__init__(self)
		print('Cookie is invalid.')


