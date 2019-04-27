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
    s = 'for ( _type {0} : {1} ) {{\n//\n}}\n'.format(arg[0], arg[1])
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
    s = 'try {{\n//\n}}\n'.format()
    s += 'catch(Exception e) {{\n//System.out.println(e.toString());\n}}\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^try$']) , cmd_handler_ ))

#err
def cmd_handler_(arg):
    s = 'throw new Exception("_error_message");'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^err$']) , cmd_handler_ ))

#errif _expr
def cmd_handler_(arg):
    s = 'if ( {} ) {{\n'.format(arg[0])
    s += 'throw new Exception("{0!r}");\n'.format(arg[0])
    s += '}}\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^errif',sp,expr]) , cmd_handler_ ))

#debug
def cmd_handler_(arg):
    s = 'if ( DEBUG_FLAG == true ) {{\n//\n}}\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^debug$']) , cmd_handler_ ))

#typeof _expr
def cmd_handler_(arg):
    s = '{0} instanceof _type\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^typeof',sp,expr]) , cmd_handler_ ))

#function _expr
def cmd_handler_(arg):
    s = 'public static void {}( _type _parameter, _type _parameter1) {{\n//return;\n}}\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^function',sp,expr]) , cmd_handler_ ))

#class _expr
def cmd_handler_(arg):
    s = 'class {}{{\n'.format(arg[0])
    s += '_type _var = null; // property declaration\n'.format()
    s += 'static _type _var = null; // statc property declaration\n\n'.format()
    s += '//class constructor declaration\n'
    s += 'public {}() {{\n//\n}}\n\n'.format(arg[0])
    s += '// method declaration\n'.format()
    s += 'public void _methodname() {{ \n }}\n\n'.format()
    s += '// static method declaration\n'.format()
    s += 'public static _methodname() {{ \n }}\n'.format()
    s += '\n'
    s += 'public static void main(String[] args) {\n'
    s += '//\n'
    s += '}\n'
    s += '}\n'
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
    s = 'final _type {} = _val;\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^const',sp,expr]) , cmd_handler_ ))

#init
def cmd_handler_(arg):
    s = ''
    s += ('//package _package_name;\n'.format())
    s += ('\n'.format())
    s += ('import java.util.*;\n'.format())
    s += ('\n'.format())
    s += ('public class _ClassName {{\n'.format())
    s += ('public static void main(String[] args) {{\n'.format())
    s += ('//\n'.format())
    s += ('}}\n'.format())
    s += ('}}\n'.format())
    s += ('\n'.format())
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^init$']) , cmd_handler_ ))

#include _expr
def cmd_handler_(arg):
    s = 'import "{0}";\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^include',sp,expr]) , cmd_handler_ ))

#print
def cmd_handler_(arg):
    s = 'System.out.println();\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^print$']) , cmd_handler_ ))

#printf
def cmd_handler_(arg):
    s = 'System.out.printf("%s",_str)\n'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^printf$']) , cmd_handler_ ))

#input
def cmd_handler_(arg):
    s = ''
    s += ('Scanner _scanner = new Scanner(System.in);\n'.format())
    s += ('String _userInput = _scanner.nextLine();\n'.format())
    s += ('//int _userInput = _scanner.nextInt();\n'.format())
    s += ('//double _userInput = _scanner.nextDouble();\n'.format())
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^input$']) , cmd_handler_ ))

#var _expr
def cmd_handler_(arg):
    s = '_type {} = null;\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^var',sp,expr]) , cmd_handler_ ))

#new _expr
def cmd_handler_(arg):
    s = '{0} _varname = new {0}();'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^new',sp,expr]) , cmd_handler_ ))

#=============================


#inline
def cmd_handler_(arg):
    s = ''
    s += ('// Put this interface to in a class\n'.format())
    s += ('// Lambda parameter types and return type should match this interface\n'.format())
    s += ('//interface _LambdaInterface {{\n'.format())
    s += ('//_retType test(_argType _arg, _argType _arg);\n'.format())
    s += ('//}}\n'.format())
    s += ('\n'.format())
    s += ('_LambdaInterface _var = (_argType _arg, _argType _arg) -> _statment;\n'.format())
    s += ('//_LambdaInterface _var = (_argType _arg, _argType _arg) -> {{ return null; }};\n'.format())
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^inline$']) , cmd_handler_ ))


#array _expr
def cmd_handler_(arg):
    s = 'ArrayList<T> _var = new ArrayList<T>();\n'.format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^array',sp,expr]) , cmd_handler_ ))

#map _expr
def cmd_handler_(arg):
    s = "HashMap<Tkey, Tval> _var = new HashMap<Tkey, Tval>();\n".format(arg[0])
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^map',sp,expr]) , cmd_handler_ ))

#thread
def cmd_handler_(arg):
    s = '//null'.format()
    return s
cmd_handler_list.append( cmd_handler( ''.join(['^thread$']) , cmd_handler_ ))
