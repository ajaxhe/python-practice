#!/usr/bin/python
#-*- coding: utf-8 -*-

import math
import time

def check_prime(n):
    if n % 2 == 0:
        return False
    from_i = 3
    to_i = int(math.sqrt(n)) + 1
    for i in xrange(from_i, to_i, 2):
        if i % 2 == 0:
            return False
    return True

if __name__ == '__main__':
    primes = []
    number_range = xrange(1,1000000)
    t1 = time.time()
    for possible_prime in number_range:
        if check_prime(possible_prime):
            primes.append(possible_prime)
    t2 = time.time()
    print('Took {}'.format(t2 - t1))
