#!/usr/local/bin/python
# encoding: gbk

import os
import sys
import urllib
import urllib2
import cookielib
import socket
import httplib
import re
import time

# 各种连接超时
Timeout_Login   = 30
Timeout_Request = 30
Timeout_Socket  = 30
Timeout_Curl  = 500
Request_Retry = 30
Post_Retry = 30

#正则匹配
p_status = re.compile(r'<a name=".+?"></a>(.+?)<p class="time">(.+?)&nbsp', re.S)
p_sendURL = re.compile(r'<form action="(http://3g.renren.com/status/wUpdateStatus.do.*?)" method="post"><p><input type="hidden" name="_rtk" value="(.+?)" />',re.S)

#Head info
Header_UserAgent = "Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2"
Header_Host = "3g.renren.com"

#Page info
LoginPage = "http://3g.renren.com/"
ValidPage = "http://3g.renren.com/home.do"
StatusPage = "http://3g.renren.com/status/getdoing.do?t=%s"
HomePage = "http://3g.renren.com/home.do"

socket.setdefaulttimeout(Timeout_Socket)

class Login:
	def __init__(self, username, password,userid):
		self.username = username
		self.password = password
		self.userid = userid
		self.status = []
		
		# 设置HTTP头
		opener_header = urllib2.build_opener()
		opener_header.addheaders = [
			("User-Agent",       Header_UserAgent),
			("Host",             Header_Host),
			('Cache-Control', 'no-cache'),

		]
		urllib2.install_opener(opener_header)
		
		# 设置Cookie
		self.cj = cookielib.MozillaCookieJar()
		opener_cookie = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(opener_cookie)

	def login(self):
	
		post = urllib.urlencode({
			"email"  : self.username,
			"password"  : self.password,
		})

		# 登录请求
		if not Post(LoginPage, post):
			return False
		# 验证访问一个用户信息页
		url_ret = Request(ValidPage, "url")
		if url_ret!=ValidPage:
			return False
		#获取发布状态的验证信息
		content_req = Request(HomePage, "content")
		m = p_sendURL.search(content_req)
		if not m:
			print "Can't find sendURL info"
			return False
		self.sendURL = m.group(1)
		self.rtk = m.group(2)
		print "send URL:",self.sendURL
		print "_rtk:",self.rtk
		return True

	def getStatus(self):
		t = time.strftime("%H%M%S",time.localtime())
		print t
		#content = Request("www.baidu.com","content")
		content = Request(StatusPage%t,"content")
		all_status = p_status.findall(content)
		for item in all_status:
			self.status.append((item[0],item[1]))
		self.cj.clear()
		return self.status
		
	def send(self,content):
		#封装状态信息
		try:send_content = content.decode("gbk","ignore").encode("utf8","ignore") 
		except:send_content = content
		post = urllib.urlencode({
			"_rtk":self.rtk,
			"sour":"home",
			"loginbybm":"",
			"status":send_content,
			"pid":" ",
			"empty":"1",
			"update":"发布"
		})
		#发布状态
		post_req = urllib2.Request(self.sendURL, headers={'User-Agent' : "Magic Browser"})
		if not Post(post_req, post):
			return False
		return True
			
def Request(url,type):
	retry = Request_Retry
	for i in range(0, retry):
		try:
			req = urllib2.urlopen(url, timeout=Timeout_Request)
			if type == "content":
				ret = req.read()
			elif type == "url":
				ret = req.geturl()
			req.close()
			if len(ret)==0:
				continue
			break
		except Exception, e:
			if i==retry-1:
				return None
	return ret

def Post(url,post):
	retry = Post_Retry
	for i in range(0, retry):
		try:
			req = urllib2.urlopen(url, post,timeout=Timeout_Request)
			url_ret = req.geturl()
			req.close()
			break
		except Exception, e:
			if i==retry-1:
				return False
	return url_ret
