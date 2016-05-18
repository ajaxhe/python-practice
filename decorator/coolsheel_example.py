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
