#!/usr/bin/python

def my_coroutine():
    while True:
        recevied = yield
        print('Received: {}'.format(recevied))

it = my_coroutine()
next(it)
it.send('First')
it.send('Second')

def minimize():
    current = yield
    while True:
        value = yield current
        print('current: {}, new_value: {}'.format(current, value))
        current = min(value, current)

it = minimize()
next(it)
print(it.send(10))
print(it.send(1))
#print(it.send(0))
print(it.send(-10))
