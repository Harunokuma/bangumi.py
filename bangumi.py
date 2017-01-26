#_*_ coding:utf-8 _*_

import requests
import re
from bs4 import BeautifulSoup
import pymysql
import threading
import os
import json
import logging
import logging.config
from mail import *
# bt站参数
MAIN_URL = 'http://www.kisssub.org/'
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

# 连接数据库的参数
db_host = 'localhost'
db_user = 'root'
db_password = 'password'
db_dbname = 'Anime'
db_charset = 'utf8'
db_bangumiTbl = 'bangumi'
db_userTbl = 'user'
global_conn = None

# 本地文件路径参数
abspath = os.path.dirname(__file__)
torrentDirPath = os.path.join(abspath, "torrent")
magnetDirPath = os.path.join(abspath, "magnet")

# logging参数
logger = logging.getLogger("animeLogger")

# 更新动画所用的线程
class updateThread (threading.Thread):
	def __init__(self, name, num, total_num):
		threading.Thread.__init__(self)
		self.name = name
		self.num = num
		self.total_num = total_num
	def run(self):
		updateEachTorrent(self.name, self.num, self.total_num)
		print("Update", self.name, "over")

# 搜索是否有满足要求的资源页面
def searchUrl(name, num):
	url = MAIN_URL + "search.php?keyword=" + name
	headers = {'User-Agent':User_Agent}
	html = requests.get(url, headers = headers).content
	bsObj = BeautifulSoup(html, "html.parser")

	pattern1 = re.compile(r'((字幕)|(新番)|(Sub)).*%s[^0-9]+'% num)
	pattern2 = re.compile(r'^(?!.*?OVA).*$')
	pattern3 = re.compile(r'((BIG5)|(繁)|(CHT)|(PV)|(预告))')

	for link in bsObj.findAll("a", href=re.compile("show-")):
		text = link.text.replace("\n"," ")
		if pattern1.search(text):
			if pattern2.search(text):
				if not pattern3.search(text):
					text = text.replace(" ","")
					suburl = link.attrs['href']
					logger.info('Find a url [%s], which include [%s]' % (MAIN_URL+suburl, text))
					return suburl

	logger.info("Can't find [%s][%s]'s resourse"%(name,num))
	return None

# 通过下载地址下载种子和磁链
def getTorrent(suburl, name, num):
	url = MAIN_URL + suburl
	headers = {'User-Agent':User_Agent}
	html = requests.get(url, headers = headers).content
	bsObj = BeautifulSoup(html, "html.parser")

	for link in bsObj.findAll("a", {"id":"magnet"}):
		if 'href' in link.attrs:
			magnet = bytes(link.attrs['href'], encoding='utf8')
			filePath = os.path.join(magnetDirPath, "[%s][%s].txt"%(name,num))
			try:
				with open(filePath, "wb") as magnetFile:
					magnetFile.write(magnet)
			except Exception as e:
				logger.error('Failed to create file [%s]' % filePath, exc_info=True)
				return False
			else:
				logger.info('[%s][%s] update success' %(name, num))
				return True

	# for link in bsObj.findAll("a", {"id":"download"}):
	# 	if 'href' in link.attrs:
	# 		download_url = MAIN_URL + link.attrs['href']

	# while True:
	# 	try:
	# 		download_req = requests.get(download_url, headers = headers, allow_redirects = False, timeout = 10)
	# 		break
	# 	except:
	# 		logger.warn('Connect to [%s] timeout, try to redownload' % download_url)
	# 		continue

	# file = download_req.content

	# try:
	# 	filePath = os.path.join(torrentDirPath, "[%s][%s].torrent"%(name,num))
	# 	with open(filePath, "wb") as torrentFile:
	# 		torrentFile.write(file)
	# except Exception as e:
	# 	logger.error('Failed to create file [%s]' % filePath, exc_info=True)
	# 	return False
	# else:
	# 	logger.info('[%s][%s] update success' %(name, num))
	# 	return True

# 更新所有的动画
def updateAllTorrent():
	setupLogging()
	global global_conn
	try:
		global_conn = pymysql.connect(host=db_host,user=db_user,passwd=db_password,db=db_dbname,charset=db_charset)
	except Exception as e:
		logger.error('Failed to connect to database', exc_info=True)

	# 更新动画的线程池
	threads = []

	# 测试是否能连接至主站
	if not testConnect(MAIN_URL):
		print("Can't connect to", MAIN_URL)
		return

	# 获取数据库中的所有动画数据
	cur = global_conn.cursor()
	cur.execute("SELECT * FROM %s WHERE num < total_num" % db_bangumiTbl)
	
	for each in cur.fetchall():
		name = each[0]
		num = each[1]
		total_num = each[2]
		# if(num < total_num):
		thread = updateThread(name, num, total_num)
		threads.append(thread)
		thread.start()
	cur.close()

	# 等待所有更新线程结束之后，退出该函数
	for t in threads:
		t.join()

	pushToUser()

	global_conn.close()
	print("Update Over!")

# 将更新的动画推送给用户
def pushToUser():
	animeDist = {}
	cur = global_conn.cursor()
	cur.execute("SELECT * FROM %s" % db_bangumiTbl)
	for each in cur.fetchall():
		animeDist[each[0]] = each[1]
	cur.close()

	userList = []
	cur = global_conn.cursor()
	cur.execute("SELECT DISTINCT(mail) FROM %s" % db_userTbl)
	for each in cur.fetchall():
		userList.append(each[0])
	cur.close()

	torrents = []
	for mail in userList:
		cur = global_conn.cursor()
		cur.execute("SELECT title, num FROM %s WHERE mail = '%s'" % (db_userTbl, mail))
		for each in cur.fetchall():
			title = each[0]
			num = each[1]
			while animeDist[title] > num:
				num += 1
				str_num = str("%02d"% num)
				torrent = {}
				torrent['title'] = title
				torrent['num'] = str_num
				filePath = os.path.join(magnetDirPath, "[%s][%s].txt"%(title,str_num))
				with open(filePath, "r") as magnetFile:
					torrent['maglink'] = magnetFile.read()
				torrents.append(torrent)
			cur_2 = global_conn.cursor()
			cur_2.execute("UPDATE %s SET num = %d WHERE mail = '%s' AND title = '%s'" %(db_userTbl ,num, mail, title))
			cur_2.close()
			global_conn.commit()
		if len(torrents) > 0:
			sendTorrent(mail, torrents)
		cur.close()

# 对单个动画进行更新
def updateEachTorrent(name, num, total_num):
	try:
		conn = pymysql.connect(host=db_host,user=db_user,passwd=db_password,db=db_dbname,charset=db_charset)
	except Exception as e:
		logger.error('Failed to connect to database', exc_info=True)
		return

	while num < total_num :
		# 将集数的数字转换成字符串
		str_num = str("%02d"%(num + 1))
		# 搜索是否有该集的动画更新
		suburl = searchUrl(name, str_num)
		
		if suburl is not None:
			if not getTorrent(suburl, name, str_num):
				break

			# 将数据库中的数据更新
			cur = conn.cursor()
			cur.execute('UPDATE %s SET num = num + 1 WHERE title = "%s"' % (db_bangumiTbl ,name))
			num = num + 1
			print("Update %s %s" %(name, str_num))
			conn.commit()
			cur.close()
		else:
			break
	logger.info('%s update over, the leatest is %d' % (name, num))

# 重置所有未完结动画下载的记录（调试用）
def resetDownload():
	cur = global_conn.cursor()
	cur.execute("UPDATE %s SET num = 0 WHERE num < total_num" % db_bangumiTbl)
	global_conn.commit()
	cur.close()
	print("Reset Over!")

# 向数据库中添加一个动画
def addAnime(name):
	cur = global_conn.cursor()
	cur.execute('INSERT INTO %s (title) VALUES ("%s")' % (db_bangumiTbl ,name))
	global_conn.commit()
	cur.close()
	print("Add anime Over!")

# 测试是否能连接至主站
def testConnect(url):
	try:
		headers = {'User-Agent':User_Agent}
		html = requests.get(MAIN_URL, headers = headers).content
	except Exception as e:
		logger.error('Failed to global_connect to [%s]' % MAIN_URL, exc_info=True)
		return False
	else:
		return True

# 设置日志格式
def setupLogging():
	logger = logging.getLogger("animeLogger")
	handler = logging.handlers.RotatingFileHandler(os.path.join(abspath,'anime.log'), maxBytes=1024*1024, backupCount = 5)
	formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s")
	handler.setFormatter(formatter)
	logger.setLevel(logging.INFO)
	logger.addHandler(handler)

if __name__ == '__main__':
	updateAllTorrent()
# 	setupLogging()

# 	while(1):
# 		try:
# 			global_conn = pymysql.connect(host=db_host,user=db_user,passwd=db_password,db=db_dbname,charset=db_charset)
# 		except Exception as e:
# 			logger.error('Failed to connect to database', exc_info=True)
# 		else:
# 			print(
# """
# ----------------------------------------------------------------------------------------------------------
# Select Operation:
# 1.update torrent
# 2.add anime
# 3.reset download
# 4.exit

# Your choice:
# """)
# 			op = input()
# 			while not op:
# 				op = input()
# 			print(
# """
# ----------------------------------------------------------------------------------------------------------
# """)
# 			if(op == '1'):
# 				print("Updating......")
# 				updateAllTorrent()
# 			elif(op == '2'):
# 				print("Anime name:")
# 				name = input()
# 				addAnime(name)
# 			elif(op == '3'):
# 				resetDownload()
# 			elif(op == '4'):
# 				break
# 		global_conn.close()