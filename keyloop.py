from pynput.keyboard import Key, KeyCode, Listener
import util
import queue
from time import sleep
import copy

class KeyEventCallback:
    def __init__(self):
        self.listen = False
    def start(self):
        self.listen = True
    def stop(self):
        self.listen = False
    def is_listen(self):
        return self.listen
    def on_press(self,key):
            pass
    def on_release(self,key):
            pass
    def on_char(self,c):
            pass

class Logger(KeyEventCallback):
    def __init__(self):
        KeyEventCallback.__init__(self)
        self.log_press = []
        self.log_release = []
    def on_press(self, key):
        if self.is_listen():
            self.log_press.append(util.get_key_code(key))
    def on_release(self, key):
        if self.is_listen():
            self.log_release.append(util.get_key_code(key))

class Guard(KeyEventCallback):
    def __init__(self):
        KeyEventCallback.__init__(self)
        self.next_press = -1
        self.next_release = -1
        self.queue_press = queue.Queue()
        self.queue_release = queue.Queue()
    def on_press(self, key):
        kcode = util.get_key_code(key)
        if self.next_press < 0:
            try:
                self.next_press = self.queue_press.get_nowait()
            except Exception as err:
                self.next_press = -1
        if self.next_press == kcode:
            self.next_press = -1
            return False
        else:
            return True
    def on_release(self, key):
        kcode = util.get_key_code(key)
        if self.next_release < 0:
            try:
                self.next_release = self.queue_release.get_nowait()
            except Exception as err:
                self.next_release = -1
        if self.next_release == kcode:
            self.next_release = -1
            return False
        else:
            return True
    def put_press(self, kcode):
        self.queue_press.put(kcode)
    def clear_press(self):
        with self.queue_press.mutex:
            self.queue_press.queue.clear()
    def clear_release(self):
        with self.queue_release.mutex:
            self.queue_release.queue.clear()
    def put_release(self, kcode):
        self.queue_release.put(kcode)

class BotKeyFilter(KeyEventCallback):
    def __init__(self):
        KeyEventCallback.__init__(self)
        self.reset()
    def reset(self):
        self.shift = False
        self.ctrl = False
        self.alt = False
        self.cmd = False
    def on_press_filter(self, key):
        if util.is_shift(key):
            self.shift = True
        elif util.is_ctrl(key):
            self.ctrl = True
        elif util.is_alt(key):
            self.alt = True
        elif util.is_cmd(key):
            self.cmd = True
        else:
            key = self.change_key(key)
            self.reset()
        return key
    def change_key(self,key):
        key_bot = copy.copy(key)
        if util.is_shiftable(key):
            key_bot.char = util.key2char_bot(key,self.shift)
        return key_bot
    def __str__(self):
        return "BotKeyFilter:"+str((self.shift,self.ctrl,self.alt,self.cmd))
    def __repr__(self):
        return self.__str__()


guard = Guard()
logger = Logger() # is close by default
filter = BotKeyFilter()

class CharIO(KeyEventCallback):
    def __init__(self):
        KeyEventCallback.__init__(self)
        self.buff = ''
        self.writeList = []
    def write(self, outStr):
        if outStr == None or len(outStr) == 0:
            return
        else:
            self.writeList.append(outStr)
    def flush(self):
        writeStr = ''
        for outStr in self.writeList:
            writeStr += outStr
            for kclist in map( util.char2keycode, outStr):
                for kc in kclist:
                    guard.put_press( kc)
        self.writeList.clear()
        util.press_char(writeStr)
    def read(self):
        return self.buff
    def on_press(self, key):
        c = util.key2char(key)
        if c != None and c != '':
            self.buff = c
        else:
            self.buff = ''

chario = CharIO()
charEventCallbackList = []

def add_callback( cec):
    if isinstance( cec, KeyEventCallback):
        charEventCallbackList.append(cec)
        return True
    return False

def remove_callback( cec):
    if isinstance( cec, KeyEventCallback):
        charEventCallbackList.remove(cec)
        return True
    return False


qPress = queue.Queue()
qRelease = queue.Queue()

def _on_press(key):
    try:
        qPress.put(key)
    except Exception as err:
        print('EVENT exception: {}'.format(err))

def _on_release(key):
    try:
        qRelease.put(key)
    except Exception as err:
        print('EVENT exception: {}'.format(err))

listener = Listener(on_press=_on_press,on_release=_on_release)

def on_press(key):
    try:
        logger.on_press(key)
        key_bot = filter.on_press_filter(key)
        if guard.on_press(key) == True:
            chario.on_press(key)
            for cec in charEventCallbackList:
                cec.on_press(key)
        print("Guard[out].len({!r}) <= {!r} {!r}".format(guard.queue_press.qsize(), util.get_key_name(key), util.get_key_code(key)))
        chario.flush()
    except Exception as err:
        print('LOOP exception: {}'.format(err))

def on_release(key):
    try:
        logger.on_release(key)
        if util.get_key_code(key) == 0 and util.get_key_name(key) == '':
            print("LOOP BUG KEY:",dir(key))
    except Exception as err:
        print('LOOP exception: {}'.format(err))

def loop():
    listener.start()
    while True:
        key = qPress.get()
        on_press(key)
        key = qRelease.get()
        on_release(key)
