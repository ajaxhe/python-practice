#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
example from http://coolshell.cn/articles/11265.html
'''

def hello(fn):
    def wrapper():
        print "hello, %s" % fn.__name__
        fn()
        print "goodby, %s" % fn.__name__
    return wrapper

@hello
def foo():
    print "i am foo"

foo()

# decorator define
def fuck(fn):
    print "fuck %s!" % fn.__name__[::-1].upper()

@fuck
def wfg():
    pass

# 带参数及多个Decrorator
def make_html_tag(tag, *args, **kwargs):
    def real_decorator(fn):
        css_class = ' class="{}"'.format(kwargs['css_class']) if 'css_class' in kwargs else ""
        def wrapped(*args, **kwargs):
            return '<'+tag+css_class+'>' + fn(*args, **kwargs) + '</'+tag+'>'
        return wrapped
        #return "<"+tag+css_class+">" + fn(*args, **kwargs) + "</"+tag+">"
    return real_decorator

@make_html_tag(tag='b', css_class='bold_css')
@make_html_tag(tag='b', css_class='bold_css')
def hello():
    return 'hello world'

print hello()

# class decorator
class MyDecorator(object):
    # 1）如果decorator有参数的话，__init__() 成员就不能传入fn了，而fn是在__call__的时候传入的。
    def __init__(self, fn):
        print 'inside MyDecorator.__init__()'
        self.fn = fn

    def __call__(self):
        self.fn()
        print 'inside MyDecorator.__call__()'


@MyDecorator
def a_func():
    print 'inside a_func()'

print 'Finish decorator c_func()'

a_func()

# 修改传入参数
def decorator_a(func):
    def wrap(*args, **kwargs):
        kwargs['str'] = 'Hello A!'
        return func(*args, **kwargs)
    return wrap

@decorator_a
def print_a(*args, **kwargs):
    print kwargs['str']

print_a()

def decorator_b(func):
    def wrap(*args, **kwargs):
        s = 'Hello B!'
        return func(s, *args, **kwargs)
    return wrap

@decorator_b
def print_b(s, *args, **kwargs):
    print s

print_b()

def decorator_c(func):
    def wrap(*args, **kwargs):
        args = args + ('Hello C!',)
        return func(*args, **kwargs)
    return wrap

@decorator_c
def print_c(s, *args, **kwargs):
    # 没有明白这里s的顺序为何是排第一?作者的用例有bug
    print s

print_c('Test C!')

def decorator_c2(func):
    def wrap(*args, **kwargs):
        args = ('Hello C2!',) + args
        return func(*args, **kwargs)
    return wrap

@decorator_c2
def print_c2(*args, **kwargs):
    print args[0]

print_c2('Test C2')

# wrapper的作用
from functools import wraps
def hello_wrap(fn):
    @wraps(fn)
    def wrapper():
        print 'hello, %s' % fn.__name__
        fn()
        print 'goodbye, %s' % fn.__name__
    return wrapper

@hello_wrap
def foo_wrap():
    '''foo wrap doc'''
    print 'I am foo_wrap'

foo_wrap()
print(foo_wrap)
print foo_wrap.__name__
print foo_wrap.__doc__

# decorator例子

#1) decorator用作缓存 
def memo(fn):
    cache = {}
    miss = object()
    @wraps(fn)
    def wrapper(args):
        result = cache.get(args, miss)
        if result is miss:
            result = fn(args)
            cache[args] = result
        return result
    return wrapper

@memo
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print "fib(6) = %d" % fib(6)

# 2) router类 
class Router(object):
    def __init__(self):
        self.func_map = {}

    def register(self, fn_name):
        def wrapper(fn):
            self.func_map[fn_name] = fn
            return fn
        return wrapper
            
    def call_method(self, fn_name):
        return self.func_map[fn_name]()

router = Router()
@router.register('/')
def main_page_url():
    return 'This is main page.'

@router.register('/next_page')
def next_page_url():
    return 'This is the next page.'

print main_page_url()
print next_page_url()

#3) logger封装函数
import time
def logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print 'function = {0}'.format(fn.__name__)
        print '\targs = {0} {1}'.format(args, kwargs)
        print '\treturn = {0}'.format(result)
        print '\ttime = {0}'.format(t2-t1)
        return result
    return wrapper

@logger
def multipy(x, y):
    return x * y

@logger
def sum(n):
    s = 0
    for i in xrange(n):
        s += i
    return s

print multipy(10,1024)
print sum(1024*1024)

# 4)异步执行的decorator
from threading import Thread

def async(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        thl = Thread(target=fn, args = args, kwargs = kwargs)
        thl.start()
        return thl
    return wrapper


if __name__ == '__main__':
    from time import sleep
    @async
    def print_samedata(idx):
        print 'start print_samedata %d' % idx
        sleep(2)
        print 'sleep 2 seconds %d' % idx
        sleep(2)
        print 'finish print_samedata %d' % idx

    def main():
        print_samedata(1)
        print 'back in main'
        print_samedata(2)
        print 'back in main'

    main()
