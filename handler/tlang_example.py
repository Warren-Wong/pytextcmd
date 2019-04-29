import re
from handler import util

cmd_handler_list = []

def exec_cmd( cmd):
    resp = None
    for h in cmd_handler_list:
        arg = h.match_cmd( cmd)
        if arg != None:
            resp = h.exec_cmd( arg)
            break
    return resp

var = '([^\d\W][\w]*)'
token = '([^\s]+)'
digit = '([\d]+)'
expr = '([^\s].*)'
sp = '[\s]+'


#help
def cmd_handler_(arg):
    s = ''
    for c in cmd_handler_list:
        s += c.p + ',\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^help$']) , cmd_handler_ ))

# for _expr from _expr to _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^for',sp,expr,sp,'from',sp,expr,sp,'to',sp,expr]) , cmd_handler_ ))

# foreach _expr in _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^foreach',sp,expr,sp,'in',sp,expr]) , cmd_handler_ ))

# while _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^while',sp,expr]) , cmd_handler_ ))

# dowhile _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^dowhile',sp,expr]) , cmd_handler_ ))

# if _expr _num
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^if',sp,expr,sp,digit]) , cmd_handler_ ))

# switch _expr _num
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^switch',sp,expr,sp,digit]) , cmd_handler_ ))

#try
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^try$']) , cmd_handler_ ))

#err
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^err$']) , cmd_handler_ ))

#errif _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^errif',sp,expr]) , cmd_handler_ ))

#debug
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^debug$']) , cmd_handler_ ))

#typeof _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^typeof',sp,expr]) , cmd_handler_ ))

#function _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^function',sp,expr]) , cmd_handler_ ))

#class _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^class',sp,expr]) , cmd_handler_ ))

#// _digit
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^//',sp,expr]) , cmd_handler_ ))

#/// _digit
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^///',sp,expr]) , cmd_handler_ ))

#const _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^const',sp,expr]) , cmd_handler_ ))

#init
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^init$']) , cmd_handler_ ))

#include _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^include',sp,expr]) , cmd_handler_ ))

#print
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^print$']) , cmd_handler_ ))

#printf
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^printf$']) , cmd_handler_ ))

#input
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^input$']) , cmd_handler_ ))

#var _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^var',sp,expr]) , cmd_handler_ ))

#new _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^new',sp,expr]) , cmd_handler_ ))


#=============================

#array _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^array',sp,expr]) , cmd_handler_ ))

#map _expr
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^map',sp,expr]) , cmd_handler_ ))

#inline
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^inline$']) , cmd_handler_ ))

#thread
def cmd_handler_(arg):
    s = ''.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^thread$']) , cmd_handler_ ))
