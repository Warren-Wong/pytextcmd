import keyloop
import util
from handler import tpy, tjs, tphp, tjava, bash, echo, thtml, tc
from time import sleep

class HandlerSystem:
    def __init__(self):
        self.cmd_handler = ''
        self.cmd_handler_map = {
            'tpy':tpy.exec_cmd,
            'tphp':tphp.exec_cmd,
            'tjs':tjs.exec_cmd,
            'tjava':tjava.exec_cmd,
            'bash':bash.exec_cmd,
            'echo':echo.exec_cmd,
            'thtml':thtml.exec_cmd,
            'tc':tc.exec_cmd
        }
    def help(self):
        return str(self.cmd_handler_map.keys());
    def get_resp(self, cmd):
        cmd_h = self.cmd_handler_map.get(self.cmd_handler)
        if cmd_h == None: # Do not have a handler yet, try to set one
            if cmd == 'help':
                return self.help();
            elif self.cmd_handler_map.get(cmd) != None:
                self.cmd_handler = cmd
                return '' #'Handler Set to {}'.format(cmd)
            else:
                return '' #'Handler {} not found'.format(cmd)
        else: # has a command handler, run command
            resp = cmd_h( cmd)
            if resp == None:
                resp = ''
            return resp
    def get_prompt(self):
        if self.cmd_handler == '':
            return '#'
        else:
            return self.cmd_handler+'#'

class CmdLine:
    def __init__(self):
        self.is_active = False
        self.prompt = ''
        self.buff = []
        self.input = []
    def __str__(self):
        return "CmdLine[{!r}]<prompt:{!r} buff:{!r} input:{!r}>".format( self.is_active, self.prompt, ''.join(self.buff), ''.join(self.input))
    def write_prompt(self):
        self.buff.extend(self.prompt)
        keyloop.chario.write(self.prompt)
    def erase_all(self):
         erace = '\b'*( len(self.buff) )
         keyloop.chario.write(erace)
    def active(self):
        self.buff.clear()
        self.input.clear()
        self.is_active = True
    def inactive(self):
        self.is_active = False
    def update(self,c):
        print("CmdLine.update <= {!r}".format(c))
        ret = ''
        if c is '':
            pass
        elif self.is_active == False and c == '`':
            self.active()
            self.buff.append(c)
            self.write_prompt()
        elif self.is_active == True and c == '`':
            self.buff.append(c)
            self.erase_all()
            self.inactive()
            ret = ''.join(self.input)
        elif self.is_active == True and c == '\b':
            if len(self.input) > 0:
                self.input.pop()
                self.buff.pop()
            else:
                self.buff.pop()
                self.erase_all()
                self.inactive()
        elif self.is_active == True:
            self.input.append(c)
            self.buff.append(c)
        return ret

class Admin(keyloop.KeyEventCallback):
    def __init__(self):
        keyloop.KeyEventCallback.__init__(self)
        self.cmdline = CmdLine()
        self.hsys = HandlerSystem()
        self.tags = []
        self.cmdline.prompt = self.hsys.get_prompt()
    def on_press(self,key):
        c = keyloop.chario.read()
        cmd = self.cmdline.update(c)
        print("cmd={!r}".format(cmd))
        print(self.cmdline)
        if len(cmd) > 0:
            outStr = self.hsys.get_resp(cmd)
            keyloop.chario.write(outStr)
            self.cmdline.prompt = self.hsys.get_prompt()


admin = Admin()
keyloop.add_callback(admin)
keyloop.loop()
