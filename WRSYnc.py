#!/usr/local/bin/python
# encoding:gbk
import os
import sys
import urllib2
import time
import ConfigParser

import tools_wb
import tools_rr

cf = ConfigParser.ConfigParser()
cf.read("conf.ini")
try:
	UserName_rr = cf.get("renren","username")
	Password_rr = cf.get("renren","password")
	UserID_rr = cf.get("renren","userid")
	UserName_wb = cf.get("weibo","username")
	Password_wb = cf.get("weibo","password")
	UserID_wb = cf.get("weibo","userid")
except:
	print "init configure file failed"
	exit()

Sess_rr = tools_rr.Login(UserName_rr,Password_rr,UserID_rr)
Sess_wb = tools_wb.Login(UserName_wb,Password_wb,UserID_wb)

def de_en_code(str):
	return str.decode("gbk","ignore").encode("utf8","ignore")

#��¼΢��
if Sess_wb.login():
	print "login weibo success "
else:
	print "login weibo failed "
	exit()

#��¼������
if Sess_rr.login():
	print "login renren success "
else:
	print "login renren failed "
	exit()
	
#��ʼ�������������״̬
last_rr_status = ""
Status_rr = Sess_rr.getStatus()
if len(Status_rr) > 0:
	last_rr_status = Status_rr[0][0]
print "last renren status:",last_rr_status

#��ʱ��ȡ����״̬
while(1):
	Status_rr = Sess_rr.getStatus()
	for item in Status_rr:
		if item[0] == last_rr_status:
			break
		#����״̬����΢����
		if Sess_wb.send(item[0]):
			print "send %s to weibo success"%item[0]
		else:
			print "send %s to weibo failed"%item[0]
	if len(Status_rr) > 0:
		last_rr_status = Status_rr[0][0]
		print "last renren status:",last_rr_status
	#˯��5����
	time.sleep(5)
	





