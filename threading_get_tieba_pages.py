#!/usr/bin/python
import requests
# from bs4 import BeautifulSoup
import threading
import re
import urllib
import urllib2
import socket
import sys
import os
import time
import logging
import errno

# socket.setdefaulttimeout(60)

# create logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# create handler, write into log file
fh = logging.FileHandler('threading.log')
fh.setLevel(logging.DEBUG)

# create handler, print to terminal
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)

# define handler output format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
#ch.setFormatter(formatter)

# add logger handler
logger.addHandler(fh)
#logger.addHandler(ch)

# add one log message
logger.info('##############################   START  ################################')

def getimg(aaa):
    reg = re.compile(r'<img .* src="(.*?)"')

    l = re.findall(reg, aaa)    
    for x in l:
        # logger.debug(threading.currentThread().getName() + '-' + x)
        # sys.exit(0)
        url_list.append(x)        

class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
    def run(self):
        apply(self.func, self.args)

# download pics
def running(url):
    # threadLock.acquire()
    try:
        filename = os.path.basename(url)          
        urllib.urlretrieve(url,"pics/" + filename)
    except IOError as e:
        logger.debug(threading.currentThread().getName() + '-' + url)
        logger.debug(threading.currentThread().getName() + '-' + 'IOError:' + "I/O error(%s): {%s}" % (e.errno, e.strerror))        
        if str(e.strerror) == '[Errno 110] Connection timed out':
            logger.debug(threading.currentThread().getName() + '-' + 'reuse')
            logger.debug(threading.currentThread().getName() + '-' + url)
            url_timeout_list.append(url)        
        pass
    except urllib2.URLError, e:
        logger.debug(url)
        logger.debug('URLError:' + e.code)
        pass    

    # threadLock.release()

# visit pages
def readpages(url):
    try:
        s = urllib.urlopen(url)
        s1 = s.read()
        if s.getcode() == 200:            
            getimg(s1)
        else:
            print(s.getcode())
    except:
        pass

if __name__ == '__main__':
    url_list = ['',]
    url_timeout_list = []
    print('hello!')
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    threadLock = threading.Lock()
    baseUrl = 'http://tieba.baidu.com/p/4241334737'
    a = [baseUrl,]
    pagesCount = 0
    while pagesCount < 31:      
        if pagesCount == 0:
            a.append(baseUrl)
        else:
            a.append(baseUrl+'?pn=%d' % pagesCount)

        pagesCount += 1
        
    
    thread_list = [ MyThread(readpages, (url, )) for url in a ]
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for i in thread_list:
        i.join()


    thread_list = [ MyThread(running, (url, )) for url in url_list ]
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for i in thread_list:
        i.join()
        
    url_timeout_list_run = url_timeout_list
    if len(url_timeout_list_run):
        logger.debug('+++++++++++++++++++++++++++++++++ Download Timeout in +++++++++++++++++++++++')
        thread_list = [ MyThread(running, (url, )) for url in url_timeout_list_run ]
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for i in thread_list:
            i.join()

    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "process ended"

