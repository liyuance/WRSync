#!/usr/local/bin/python
# encoding:gbk

import os
import sys
import urllib2
import time

import tools_rr
import tools_wb

#人人账号
UserName_rr = ""
Password_rr = ""
UserID_rr = ""
#微博账号
UserName_wb = ""
Password_wb = ""
UserID_wb = ""

Sess_rr = tools_rr.Login(UserName_rr,Password_rr,UserID_rr)
Sess_wb = tools_wb.Login(UserName_wb,Password_wb,UserID_wb)

def de_en_code(str):
	return str.decode("gbk","ignore").encode("utf8","ignore")

#登录微博
if Sess_wb.login():
	print "login weibo success "
else:
	print "login weibo failed "
	exit()

#登录人人网
if Sess_rr.login():
	print "login renren success "
else:
	print "login renren failed "
	exit()
	
print "OK"

#初始化最近的人人网状态
last_rr_status = ""
Status_rr = Sess_rr.getStatus()
if len(Status_rr) > 0:
	last_rr_status = Status_rr[0][0].strip()
print "last renren status:",last_rr_status
if Sess_wb.send(last_rr_status):
	print "send status to weibo success"
exit()
#定时获取人人状态
while(1):
	Status_rr = Sess_rr.getStatus()
	for item in Status_rr:
		print item[0],"time",item[1]
		if item[0].strip() == last_rr_status:
			break
		#将新状态发到微博上
		if Sess_wb.send(item[0].strip()):
			print "send status to weibo success"
		else:
			print "send status to weibo failed"
	if len(Status_rr) > 0:
		last_rr_status = Status_rr[0][0].strip()
	#睡眠5秒钟
	time.sleep(5)
	





