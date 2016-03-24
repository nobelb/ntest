#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
使用多线程抓取某论坛帖子的url和标题
'''

import requests
from bs4 import BeautifulSoup
import threading
import time

url_list = []
for x in range(1, 50):
    raw_url = 'http://bbs.a9vg.com/forum-261-%d.html' % x    
    url_list.append(raw_url)

class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
    def run(self):
        apply(self.func, self.args)

def running(url):
    # lock.acquire()
    html = requests.get(url)
    if html.status_code == 200:
        html_text = html.text

    soup = BeautifulSoup(html_text, 'html.parser')
    with open('cao.txt', 'a+') as f:
        for link in soup.find_all('a', 'xst'):
            s = 'http://bbs.a9vg.com/' + str(link.get('href')) + ' ' + str(link.get_text().encode('utf-8'))
            f.writelines(s)
            f.writelines('\n')
    # lock.release()

if __name__ == '__main__':
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    threadLock = threading.Lock()
    thread_list = [ MyThread(running, (url, )) for url in url_list ]
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for i in thread_list:
        i.join()
    print "process ended"

    # inspect repetition data
    with open('cao.txt', 'r') as f:
        f_list = f.readlines()
        set_list = set(f_list)
    for x in set_list:
        if f_list.count(x) > 1:
            print "the <%s> has found <%d>" % (x, f_list.count(x))
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))