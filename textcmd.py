# pytextcmd-0.1.2

from enum import Enum
from pynput import keyboard
from keymap import kbctrl, char2press, key2char
from handler import tpy, tjs, tphp, tjava, bash, echo, thtml, tc


class gsys_status(Enum):
    wait_signal = 0
    read_cmd = 1
    resp_cmd = 2

class global_system:
    def __init__(self):
        self.signal = ['`','`']
        self.status = gsys_status.wait_signal
        self.input_buff = ''
        self.output_buff = ''
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

    def clear_buffer(self):
        self.input_buff = ''
        self.output_buff = ''

    def debug_print(self):
        print('DEBUG:')
        print('    self.cmd_handler => {0}'.format( self.cmd_handler))
        print('    self.input_buff => {0}'.format( self.input_buff))
        print('    self.output_buff => {0}'.format( self.output_buff))

    def output_erase_cmd(self): # erase command, include begin and end signal char
        if self.status == gsys_status.resp_cmd:
            for i in range(0, len(self.input_buff)+2):
                char2press('\b')

    def output_write_resp(self, resp):
        if resp == None:
            resp = ''
        self.output_buff = resp
        for i in range(0,len(resp)):
            char2press(resp[i])

    def get_resp(self, cmd):
        cmd_h = self.cmd_handler_map.get(self.cmd_handler)
        if cmd_h == None: # No not have a handler yet, try to set one
            if self.cmd_handler_map.get(cmd) != None:
                self.cmd_handler = cmd
                return 'Handler Set to {}'.format(cmd)
            else:
                return 'Handler {} not found'.format(cmd)
        else: # has a command handler, run command
            resp = cmd_h( cmd)
            return resp

    def change_status(self, status):
        if status == gsys_status.read_cmd:
            self.clear_buffer()
        elif status == gsys_status.wait_signal:
            self.clear_buffer()
        elif status == gsys_status.resp_cmd:
            pass
        else:
            raise Exception('Unknow status')
        print("stats change: {} => {}".format(self.status,status))
        self.status = status

    def process(self, key):
        c = key2char(key)
        if self.status == gsys_status.wait_signal:
            if c == self.signal[0]:
                self.change_status( gsys_status.read_cmd)
        elif self.status == gsys_status.read_cmd:
            if c != self.signal[1]:
                if c == '\b' and len(self.input_buff)>0:
                    self.input_buff = self.input_buff[:-1]
                elif c == '\b' and len(self.input_buff)==0:
                    self.change_status(gsys_status.wait_signal)
                else:
                    self.input_buff += c
            else:
                self.change_status(gsys_status.resp_cmd)
                self.output_erase_cmd()
                if len(self.input_buff)==0:
                    self.change_status(gsys_status.wait_signal)
                else:
                    resp = self.get_resp( self.input_buff)
                    self.output_write_resp( resp)
        elif self.status == gsys_status.resp_cmd:
            if len(self.output_buff) > 1:
                self.output_buff = self.output_buff[1:]
            else:
                self.change_status(gsys_status.wait_signal)

gsys = global_system()

def on_press(key):
    try:
        print('key {0}: char: {1}'.format( str(key), key2char(key)))
        if key == keyboard.Key.esc:
            if gsys.cmd_handler != None and len(gsys.cmd_handler)>0:
                gsys.cmd_handler = ''
            else:
                return False
        else:
            gsys.process( key)
    except AttributeError as err:
        print('AttributeError: key {0}: {1}'.format( str(key),err))
        gsys.debug_print()
    except Exception as err:
        print('Exception: key {0}: {1}'.format( str(key),err))
        gsys.debug_print()

def on_release(key):
    pass

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
