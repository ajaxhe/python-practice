#!/usr/bin/python
#-*- coding: utf-8 -*-

from collections import Counter
import ctypes
import multiprocessing
import numpy as np
import os
from prettytable import PrettyTable
import sys

'''numpy使用'''
# 1) numpy with multiprocess
def worker_fn(row):
    np_array[row, :] = os.getpid()

magic_num = 7
size_x, size_y = 10000, 100
items_in_array = size_x * size_y
process_num = 4

shared_array_base = multiprocessing.Array(
    ctypes.c_double, items_in_array, lock=False)
np_array = np.frombuffer(shared_array_base, dtype=ctypes.c_double)
np_array = np_array.reshape(size_x, size_y)
np_array.fill(magic_num)

raw_input('Press a key to start workers using multiprocessing...\nps -eF | egrep "numpy|CMD"\npmap -x 26371 | grep s-')
pool = multiprocessing.Pool(processes=process_num)
pool.map(worker_fn, xrange(size_x)) 
print np_array

# print as table style
counter = Counter(np_array.flat)
tbl = PrettyTable(['PID', 'Count'])
for pid, count in counter.items():
    tbl.add_row([pid, count])
print tbl
raw_input('Exit.')
