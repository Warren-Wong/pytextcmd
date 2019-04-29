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
    s = 'for ( {0} = {1}; {0} < {2}; {0} = {0} + 1) {{\n//\n}}\n'.format(arg[0],arg[1],arg[2])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^for',sp,expr,sp,'from',sp,expr,sp,'to',sp,expr]) , cmd_handler_ ))

# foreach _expr in _expr
def cmd_handler_(arg):
    s = 'foreach ( {1} as {0} ) {{\n//\n}}\n'.format(arg[0], arg[1])
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
        s += 'elseif ( {} ) {{\n//\n}}\n'.format(arg[0])
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
    s = 'try {{\n//\n}}\n\n'.format()
    s += 'catch(Exception $e) {{\n//echo \'Message: \'.$e->getMessage();\n}}\n'.format()
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
    s = 'if ( $DEBUG_FLAG == true ) {{\n//\n}}\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^debug$']) , cmd_handler_ ))

#typeof _expr
def cmd_handler_(arg):
    s = 'gettype({})'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^typeof',sp,expr]) , cmd_handler_ ))

#function _expr
def cmd_handler_(arg):
    s = 'function {}($_passbyval, &$_passbyfref) {{   // arg: &$_passbyfref, $_passbyval = = "_default"\n//return $_ret;\n}}\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^function',sp,expr]) , cmd_handler_ ))

#class _expr
def cmd_handler_(arg):
    s = 'class {}{{\n'.format(arg[0])
    s += '// property declaration\n'.format()
    s += 'public $var1 = \'a default value\';\n\n'.format()
    s += '// constructor declaration\n'.format()
    s += 'public function {}() {{\n'.format(arg[0])
    s += '//$this->var2 = null; // property declaration\n'.format()
    s += '}}\n\n'.format()
    s += '// method declaration\n'.format()
    s += 'public function _methodname() {{  // arg: &$_passbyfref, $_passbyval = = "_default"\n'.format()
    s += '//echo $this->var;\n'.format()
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
    s = 'define("{0}", "_string_value", true); // third arg is case-insensitive. use: ${0}\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^const',sp,expr]) , cmd_handler_ ))

#init
def cmd_handler_(arg):
    s = '<?php\n\n\n\n\n\n?>\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^init$']) , cmd_handler_ ))

#include _expr
def cmd_handler_(arg):
    s = 'include \'{0}\'; // or: require \'{0}\';\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^include',sp,expr]) , cmd_handler_ ))

#print
def cmd_handler_(arg):
    s = 'echo ""; // or: print "";\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^print$']) , cmd_handler_ ))

#printf
def cmd_handler_(arg):
    s = 'printf("%s",$_str);\n'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^printf$']) , cmd_handler_ ))

#input
def cmd_handler_(arg):
    s = '// use $_GET["_key"] or $_POST["_key"] to get input'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^input$']) , cmd_handler_ ))

#var _expr
def cmd_handler_(arg):
    s = '${0} = null;  // use: ${0}\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^var',sp,expr]) , cmd_handler_ ))

#new _expr
def cmd_handler_(arg):
    s = '$_var = new {}();'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^new',sp,expr]) , cmd_handler_ ))

#=============================

#inline
def cmd_handler_(arg):
    s = 'function ($_arg, $_arg) {{ return null; }}'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^inline$']) , cmd_handler_ ))

#array _expr
def cmd_handler_(arg):
    s = '${0} = new array(); // or: ${0} = new array( obj, obj, obj);\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^array',sp,expr]) , cmd_handler_ ))

#map _expr
def cmd_handler_(arg):
    s = '${0} = new array(); // or: ${0} = new array( key => obj, key => obj, key => obj);\n'.format(arg[0])
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^map',sp,expr]) , cmd_handler_ ))

#thread
def cmd_handler_(arg):
    s = '//null'.format()
    return s
cmd_handler_list.append( util.cmd_handler( ''.join(['^thread$']) , cmd_handler_ ))
