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

#=============================
# Custom
#=============================

#handler _expr _digit
def cmd_handler_(arg):
    s = ""
    s += "#{} _expr\n".format(arg[0])
    s += "def cmd_handler_(arg):\n"
    s += "s = ''\n"
    s += ("s += ('\\n'.format())\n")*int(arg[1])
    s += "return s  \n"
    s += "\bcmd_handler_list.append( util.cmd_handler( ''.join(['^{}',sp,expr]) , cmd_handler_ ))\n".format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^handler',sp,expr,sp,expr]) , cmd_handler_ ))


#=============================
# Default
#=============================

#help
def cmd_handler_(arg):
    s = ''
    for c in cmd_handler_list:
        s += c.p + ',\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^help$']) , cmd_handler_ ))

# for _expr from _expr to _expr (include left, exclusde right)
def cmd_handler_(arg):
    s = 'for {} in range( {} , {} ):\npass\n'.format(arg[0],arg[1],arg[2])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^for',sp,expr,sp,'from',sp,expr,sp,'to',sp,expr]) , cmd_handler_ ))
# foreach _expr in _expr
def cmd_handler_(arg):
    s = 'for {} in {}:\npass\n'.format(arg[0],arg[1])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^foreach',sp,expr,sp,'in',sp,expr]) , cmd_handler_ ))
# while _expr
def cmd_handler_(arg):
    s = 'while {}:\npass\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^while',sp,expr]) , cmd_handler_ ))
# dowhile _expr
def cmd_handler_(arg):
    s = 'do_once = False\nwhile (do_once == False) or ({}):\ndo_once = True\npass\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^dowhile',sp,expr]) , cmd_handler_ ))
# if _expr _num
def cmd_handler_(arg):
    s = 'if {}:\npass\n'.format(arg[0])
    for i in range(1,int(arg[1])):
        s += 'elif {}:\npass\n'.format(arg[0])
    s += 'else:\npass\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^if',sp,expr,sp,digit]) , cmd_handler_ ))
# switch _expr _num
def cmd_handler_(arg):
    s = 'if {}:\npass\n'.format(arg[0])
    for i in range(1,int(arg[1])):
        s += 'elif {}:\npass\n'.format(arg[0])
    s += 'else:\npass\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^switch',sp,expr,sp,digit]) , cmd_handler_ ))
#try
def cmd_handler_(arg):
    s = 'try:\n'
    s += 'pass\n'
    s += 'except Exception as err:\n'
    s += 'pass\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^try$']) , cmd_handler_ ))
#err
def cmd_handler_(arg):
    s = 'raise Exception()\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^err$']) , cmd_handler_ ))
#errif _expr
def cmd_handler_(arg):
    s = 'if {}:\n'.format(arg[0])
    s += 'raise Exception( "{0!r}" )\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^errif',sp,expr]) , cmd_handler_ ))
#debug
def cmd_handler_(arg):
    s = 'if DEBUG_FLAG == True:\n'
    s += 'pass\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^debug$']) , cmd_handler_ ))
#typeof _expr
def cmd_handler_(arg):
    s = 'type({})'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^typeof',sp,expr]) , cmd_handler_ ))
#function _expr
def cmd_handler_(arg):
    s = 'def {}():\npass\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^function',sp,expr]) , cmd_handler_ ))
#class _expr
def cmd_handler_(arg):
    s = 'class {}:\ndef __init__(self):\npass\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^class',sp,expr]) , cmd_handler_ ))
#// _digit
def cmd_handler_(arg):
    s = '#\n'
    for i in range(1,int(arg[0])):
        s += '#\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^//',sp,expr]) , cmd_handler_ ))
#/// _digit
def cmd_handler_(arg):
    s = "'''\n"
    for i in range(1,int(arg[0])):
        s += '\n'
    s += "'''\n"
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^///',sp,expr]) , cmd_handler_ ))
#const _expr
def cmd_handler_(arg):
    s = '{} = None\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^const',sp,expr]) , cmd_handler_ ))
#init
def cmd_handler_(arg):
    s = '#!/usr/bin/env python\n\n\n\n\n\n'
    s += 'if __name__ == "__main__":\n'
    s += 'pass\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^init$']) , cmd_handler_ ))
#include _expr
def cmd_handler_(arg):
    s = 'import {}\n'.format(arg[0])
    s += '#from {} import _name1, _name2, _name3\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^include',sp,expr]) , cmd_handler_ ))
#print
def cmd_handler_(arg):
    s = 'print( )\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^print$']) , cmd_handler_ ))
#printf
def cmd_handler_(arg):
    s = 'print("".format())\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^printf$']) , cmd_handler_ ))
#input
def cmd_handler_(arg):
    s = '_userinput = input("")\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^input$']) , cmd_handler_ ))

#var _expr
def cmd_handler_(arg):
    s = '{} = None\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^var',sp,expr]) , cmd_handler_ ))

#new _expr
def cmd_handler_(arg):
    s = '_varname = {}()\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^new',sp,expr]) , cmd_handler_ ))

#inline
def cmd_handler_(arg):
    s = 'lambda _arg1, _arg2 : _expression'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^inline$']) , cmd_handler_ ))

#array _expr
def cmd_handler_(arg):
    s = '{0} = [] # or: {0} = [ obj, obj, obj] \n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^array',sp,expr]) , cmd_handler_ ))

#map _expr
def cmd_handler_(arg):
    s = '{0} = {{}} # or: {0} = {{ key:val, key:val}} \n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^map',sp,expr]) , cmd_handler_ ))

#thread
def cmd_handler_(arg):
    s = 'Did not finished'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^thread']) , cmd_handler_ ))

#readfile _expr
def cmd_handler_(arg):
    s = ''
    s += ('_list = []\n'.format())
    s += ('_file = open("{}", "r")\n'.format(arg[0]))
    s += ('for _line in _file:\n'.format())
    s += ('_list.append(_line) \n'.format())
    s += ('\b_file.close()\n'.format())
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^readfile',sp,expr]) , cmd_handler_ ))

#writefile _expr
def cmd_handler_(arg):
    s = ''
    s += ('_list = _list_to_write\n'.format())
    s += ('_file = open("{}", "a")\n'.format(arg[0]))
    s += ('for _line in _list:\n'.format())
    s += ('_file.write(_line + "\\n") \n'.format())
    s += ('\b_file.close()\n'.format())
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^writefile',sp,expr]) , cmd_handler_ ))
