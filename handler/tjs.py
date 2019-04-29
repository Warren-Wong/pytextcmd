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
    s = 'for ( {0} = {1}; {0} < {2} ; {0} = {0} + 1) {{\n//\n}}\n'.format(arg[0],arg[1],arg[2])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^for',sp,expr,sp,'from',sp,expr,sp,'to',sp,expr]) , cmd_handler_ ))

# foreach _expr in _expr
def cmd_handler_(arg):
    s = 'for ( {0} in {1} ) {{\n//\n}}\n'.format(arg[0], arg[1])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^foreach',sp,expr,sp,'in',sp,expr]) , cmd_handler_ ))

# while _expr
def cmd_handler_(arg):
    s = 'while ( {} ) {{\n//\n}}\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^while',sp,expr]) , cmd_handler_ ))

# dowhile _expr
def cmd_handler_(arg):
    s = 'do {{\n//\n}} while ( {} );\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^dowhile',sp,expr]) , cmd_handler_ ))

# if _expr _num
def cmd_handler_(arg):
    s = 'if ( {} ) {{\n//\n}}\n'.format(arg[0])
    for i in range(1,int(arg[1])):
        s += 'else if ( {} ) {{\n//\n}}\n'.format(arg[0])
    s += 'else {{\n//\n}}\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^if',sp,expr,sp,digit]) , cmd_handler_ ))

# switch _expr _num
def cmd_handler_(arg):
    s = 'switch ( {} ) {{\n'.format(arg[0])
    s += 'case _label:\n//\nbreak;\n'.format()
    for i in range(1,int(arg[1])):
        s += 'case _label:\n//\nbreak;\n'.format()
    s += 'default:\n//\n}}\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^switch',sp,expr,sp,digit]) , cmd_handler_ ))

#try
def cmd_handler_(arg):
    s = 'try {{\n//\n}}\n'.format()
    s += 'catch(Exception e) {{\n//console.log(e);\n}}\n'.format()
    s += 'finally {{\n//\n}}\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^try$']) , cmd_handler_ ))

#err
def cmd_handler_(arg):
    s = 'throw new Exception("_error_message");'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^err$']) , cmd_handler_ ))

#errif _expr
def cmd_handler_(arg):
    s = 'if ( {} ) {{\n'.format(arg[0])
    s += 'throw new Exception("{0!r}");\n'.format(arg[0])
    s += '}}\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^errif',sp,expr]) , cmd_handler_ ))

#debug
def cmd_handler_(arg):
    s = 'if ( DEBUG_FLAG == true ) {{\n//\n}}\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^debug$']) , cmd_handler_ ))

#typeof _expr
def cmd_handler_(arg):
    s = 'typeof ({0})\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^typeof',sp,expr]) , cmd_handler_ ))

#function _expr
def cmd_handler_(arg):
    s = 'function {}( _parameter, _parameter1) {{\n//return;\n}}\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^function',sp,expr]) , cmd_handler_ ))

#class _expr
def cmd_handler_(arg):
    s = 'class {}{{\n'.format(arg[0])
    s += 'constructor() {{\n'.format(arg[0])
    s += '//this.x = null; // property declaration\n'.format()
    s += '}}\n\n'.format()
    s += '// method declaration\n'.format()
    s += '_methodname() {{ \n'.format()
    s += '//console.log(this.x);\n'.format()
    s += '}}\n\n'.format()
    s += '// static method declaration\n'.format()
    s += 'static _methodname() {{ \n'.format()
    s += '//console.log(this.x);\n'.format()
    s += '}}\n'.format()
    s += '}}\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^class',sp,expr]) , cmd_handler_ ))

#// _digit
def cmd_handler_(arg):
    s = '//\n'
    for i in range(1,int(arg[0])):
        s += '//\n'
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^//',sp,expr]) , cmd_handler_ ))

#/// _digit
def cmd_handler_(arg):
    s = "/*\n"
    for i in range(1,int(arg[0])):
        s += '\n'
    s += "*/\n"
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^///',sp,expr]) , cmd_handler_ ))

#const _expr
def cmd_handler_(arg):
    s = 'const {} = null;\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^const',sp,expr]) , cmd_handler_ ))

#init
def cmd_handler_(arg):
    s = '\n\n\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^init$']) , cmd_handler_ ))

#include _expr
def cmd_handler_(arg):
    s = '// import statement cannot be used in embedded scripts unless such script has a type="module".;\n'
    s += 'include "{0}";\n'.format(arg[0])
    s += 'import defaultExport from "{0}";\n'.format(arg[0])
    s += 'import * as name from "{0}";\n'.format(arg[0])
    s += 'import {{ export }} from "{0}";\n'.format(arg[0])
    s += 'import {{ export as alias }} from "{0}";\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^include',sp,expr]) , cmd_handler_ ))

#print
def cmd_handler_(arg):
    s = 'console.log();\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^print$']) , cmd_handler_ ))

#printf
def cmd_handler_(arg):
    s = 'console.log();\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^printf$']) , cmd_handler_ ))

#input
def cmd_handler_(arg):
    s = 'var _userinput = prompt("_hint", "_default")'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^input$']) , cmd_handler_ ))

#var _expr
def cmd_handler_(arg):
    s = 'var {0} = null; // or {0} = undefined;\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^var',sp,expr]) , cmd_handler_ ))

#new _expr
def cmd_handler_(arg):
    s = 'var _varname = new {}();'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^new',sp,expr]) , cmd_handler_ ))

#=============================

#inline
def cmd_handler_(arg):
    s = '(_arg, _arg) => {{ return null; }}'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^inline$']) , cmd_handler_ ))

#array _expr
def cmd_handler_(arg):
    s = 'var {0} = []; // or: var {0} = new array();\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^array',sp,expr]) , cmd_handler_ ))

#map _expr
def cmd_handler_(arg):
    s = "var {0} = new Map(); // or: var {0} = new Map([[ 1, 'one' ],[ 2, 'two' ]]);\n".format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^map',sp,expr]) , cmd_handler_ ))

#thread
def cmd_handler_(arg):
    s = '//null'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^thread$']) , cmd_handler_ ))
