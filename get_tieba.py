#!/usr/bin/python
#-*- encoding:utf-8 -*-
#Download tieba pictures
import re
import urllib
import socket
import sys
import os
import time

a = raw_input('input url: ')
print('hello!')
s = urllib.urlopen(a)
s1 = s.read()


def getimg(aaa):
	reg = re.compile(r'src="(.*?)"')
	l = re.findall(reg, aaa)
	for x in l:
		try:
			# socket.setdefaulttimeout(30)
			filename = os.path.basename(x)			
			urllib.urlretrieve(x,"pics/" + filename)
		except:
			pass


if s.getcode() == 200:
	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	getimg(s1)
	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
else:
	print(s.getcode())
