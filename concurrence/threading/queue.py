#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import datetime
import time
from threading import Thread
from Queue import Queue

queue = Queue(2)

def consumer():
    while True: 
        print('Consumer waiting')
        print('get value:{}'.format(queue.get()))
        print('Consumer done')
        time.sleep(5)
        
    
consumer_thread = Thread(target=consumer)
consumer_thread.setDaemon(True)
consumer_thread.start()

idx = 0

def producer():
    global idx
    idx += 1
    print('Producer putting')
    dt_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    queue.put('[%d] %s' % (idx, dt_str))
    print('Producer done')

producer()
producer()
producer()
producer()
producer()

consumer_thread.join()
print('Done.')
