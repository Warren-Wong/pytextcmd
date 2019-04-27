import re

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

class cmd_handler:
    def __init__(self,p,handler):
        self.p = p
        self.handler = handler
    def match_cmd(self, cmd):
        cmd = cmd.strip()
        m = re.match( self.p, cmd)
        print("==={} {} {}".format(cmd,self.p,m))
        g = []
        if m != None:
            for arg in m.groups():
                g.append(str(arg).strip())
        else:
            g = None
        return g
    def exec_cmd(self,arg):
        return self.handler( arg)


# for _expr from _expr to _expr
def cmd_handler_(arg):
    s = 'for ( {0} = {1}; {0} < {2} ; {0} = {0} + 1) {{\n//\n}}\n'.format(arg[0],arg[1],arg[2])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^for',sp,expr,sp,'from',sp,expr,sp,'to',sp,expr]) , cmd_handler_ ))

# foreach _expr in _expr
def cmd_handler_(arg):
    s = 'for ( int _i = 0; _i < _len({1} ; _i = _i + 1) {{\n{0} = *({1}+_i);\n//\n}}\n'.format(arg[0],arg[1])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^foreach',sp,expr,sp,'in',sp,expr]) , cmd_handler_ ))

# while _expr
def cmd_handler_(arg):
    s = 'while ( {} ) {{\n//\n}}\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^while',sp,expr]) , cmd_handler_ ))

# dowhile _expr
def cmd_handler_(arg):
    s = 'do {{\n//\n}} while ( {} );\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^dowhile',sp,expr]) , cmd_handler_ ))

# if _expr _num
def cmd_handler_(arg):
    s = 'if ( {} ) {{\n//\n}}\n'.format(arg[0])
    for i in range(1,int(arg[1])):
        s += 'else if ( {} ) {{\n//\n}}\n'.format(arg[0])
    s += 'else {{\n//\n}}\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^if',sp,expr,sp,digit]) , cmd_handler_ ))

# switch _expr _num
def cmd_handler_(arg):
    s = 'switch ( {} ) {{\n'.format(arg[0])
    s += 'case _label:\n//\nbreak;\n'.format()
    for i in range(1,int(arg[1])):
        s += 'case _label:\n//\nbreak;\n'.format()
    s += 'default:\n//\n}}\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^switch',sp,expr,sp,digit]) , cmd_handler_ ))

#try
def cmd_handler_(arg):
    s = '//Not defined'
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^try$']) , cmd_handler_ ))

#err
def cmd_handler_(arg):
    s = 'perror("error");'
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^err$']) , cmd_handler_ ))

#errif _expr
def cmd_handler_(arg):
    s = 'if ( {} ) {{\n'.format(arg[0])
    s += 'perror("error");\n'.format(arg[0])
    s += '}}\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^errif',sp,expr]) , cmd_handler_ ))

#debug
def cmd_handler_(arg):
    s = '#ifdef DEBUG\n'
    s += '//\n'
    s += '#endif\n'
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^debug$']) , cmd_handler_ ))

#typeof _expr
def cmd_handler_(arg):
    s = '//Not defined'
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^typeof',sp,expr]) , cmd_handler_ ))

#function _expr
def cmd_handler_(arg):
    s = 'void {}( _type _parameter, _type _parameter1) {{\n//return;\n}}\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^function',sp,expr]) , cmd_handler_ ))

#class _expr
def cmd_handler_(arg):
    s = 'typedef struct _{}{{\n'.format(arg[0])
    s += '_type _var; // property declaration\n'.format()
    s += '}} {};\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^class',sp,expr]) , cmd_handler_ ))

#// _digit
def cmd_handler_(arg):
    s = '//\n'
    for i in range(1,int(arg[0])):
        s += '//\n'
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^//',sp,expr]) , cmd_handler_ ))

#/// _digit
def cmd_handler_(arg):
    s = "/*\n"
    for i in range(1,int(arg[0])):
        s += '\n'
    s += "*/\n"
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^///',sp,expr]) , cmd_handler_ ))

#const _expr
def cmd_handler_(arg):
    s = 'const _type {} = _val;\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^const',sp,expr]) , cmd_handler_ ))

#init
def cmd_handler_(arg):
    s = ''
    s += ('#include <stdio.h>\n'.format())
    s += ('#include <errno.h>\n'.format())
    s += ('#include <stdlib.h>\n'.format())
    s += ('#include <string.h>\n'.format())
    s += ('#include <ctype.h>\n'.format())
    s += ('\n')*2
    s += ('#define DEBUG\n')
    s += ('\n')*2
    s += 'int main( int argc, char** argv){\n//\n}\n'
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^init$']) , cmd_handler_ ))

#include _expr
def cmd_handler_(arg):
    s = '#include "{0}"\n'.format(arg[0])
    s += '// or include <{0}>\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^include',sp,expr]) , cmd_handler_ ))

#print
def cmd_handler_(arg):
    s = 'printf("%s",_str);\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^print$']) , cmd_handler_ ))

#printf
def cmd_handler_(arg):
    s = 'printf("%s",_str);\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^printf$']) , cmd_handler_ ))

#input
def cmd_handler_(arg):
    s = ''
    s += ('scanf("%s", _str_p );\n'.format())
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^input$']) , cmd_handler_ ))

#var _expr
def cmd_handler_(arg):
    s = '_type {} = NULL;\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^var',sp,expr]) , cmd_handler_ ))

#new _expr
def cmd_handler_(arg):
    s = '{0}* _varname = malloc( sizeof({0}));'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^new',sp,expr]) , cmd_handler_ ))

#=============================


#inline
def cmd_handler_(arg):
    s = ''
    s += ('#define FUNC_NAME( P1, P2) ((P1)+(P2))\n'.format())
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^inline$']) , cmd_handler_ ))


#array _expr
def cmd_handler_(arg):
    s = '_type* {} = malloc( _len * sizeof( _type));\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^array',sp,expr]) , cmd_handler_ ))

#map _expr
def cmd_handler_(arg):
    s = "//Not defined\n".format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^map',sp,expr]) , cmd_handler_ ))

#enum _expr
def cmd_handler_(arg):
    s = ''
    s += ('enum {} {{ _E1=0, _E2=3, E3=5 }};\n'.format(arg[0]))
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^enum',sp,expr]) , cmd_handler_ ))

#thread
def cmd_handler_(arg):
    s = '//Not defined'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^thread$']) , cmd_handler_ ))
