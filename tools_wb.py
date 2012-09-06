#!/usr/local/bin/python
# encoding:gbk

import os
import sys
import urllib
import urllib2
import cookielib
import re


# �������ӳ�ʱ
Timeout_Login   = 30
Timeout_Request = 30
Request_Retry = 30
Post_Retry = 30

#����ƥ��
p_vk = re.compile(r'<postfield name="vk" value="(.+?)" />', re.S)
p_gsid = re.compile(r'<go href="http://sina.cn\?gsid=(.+?)&amp;.*?" />', re.S)
p_status = re.compile(r'<br />     (.+?)    <br />.*?>ɾ��</a>&nbsp;(.+?)&nbsp;', re.S)

#Head info
Header_UserAgent = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"
Header_Host = "3g.sina.com.cn"

#Page info
LoginPage = "http://3g.sina.com.cn/prog/wapsite/sso/login.php"
ValidPage = "http://weibo.cn/%s/profile?vt=1&gsid=%s"
SendPage = "http://weibo.cn/mblog/sendmblog?st=8ff8&vt=1&gsid=%s"
StatusPage = "http://weibo.cn/%s/profile?vt=1&gsid=%s"

class Login:
	def __init__(self, username, password,userid):
		self.username = username
		self.password = password
		self.userid = userid
		self.status = []
		
		# ����HTTPͷ
		opener_header = urllib2.build_opener()
		opener_header.addheaders = [
			("User-Agent",       Header_UserAgent),
			("Host",             Header_Host),


		]
		urllib2.install_opener(opener_header)
		
		# ����Cookie
		self.cj = cookielib.MozillaCookieJar()
		opener_cookie = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(opener_cookie)

	def login(self):
	
		#�����¼ҳ�棬ץȡpost������vk��Ϣ
		content = Request(LoginPage,"content")
		m = p_vk.search(content)
		if not m:
			print "Can't find vk info"
			return False
		vk = m.group(1)
		password_field = "password_"+vk[0:vk.find("_")]

		post = urllib.urlencode({
			"mobile"  : self.username,
			password_field  : self.password,
			"vk":vk,
			"submit"	: "��¼"
		})
		
		# ��¼����
		url_ret = Post(LoginPage, post)
		if not url_ret:
			return False
		content = Request(url_ret,"content")
		m = p_gsid.search(content)
		if not m:
			print "Can't find gsid info"
			return False
		self.gsid = m.group(1)
		# ��֤����һ���û���Ϣҳ
		req_p = urllib2.Request(ValidPage%(self.userid,self.gsid), headers={'User-Agent' : "Magic Browser"})
		url = Request(req_p,"url")
		#print ru
		if url!=ValidPage%(self.userid,self.gsid):
			return False
		return True
		
	def getStatus(self):
		req_p = urllib2.Request(ValidPage%(self.userid,self.gsid), headers={'User-Agent' : "Magic Browser"})
		content = Request(req_p,"content").decode("utf8","ignore").encode("gbk","ignore")
		all_status = p_status.findall(content)
		self.status = []
		for item in all_status:
			self.status.append((item[0].strip(),item[1].strip()))
		return self.status
		
	def send(self,content):
		post = urllib.urlencode({
			"rl":"1",
			"content":content
		})
		
		# ����΢��
		post_req = urllib2.Request(SendPage%self.gsid, headers={'User-Agent' : "Magic Browser"})
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

