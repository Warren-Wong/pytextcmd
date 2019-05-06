from pynput.keyboard import Key, KeyCode, Controller
from keymap import k2c_special, k2c, k2c_shift, c2k_special, c2k, c2k_shift
from time import sleep

def is_esc(key):
    if isinstance(key, Key) and key == Key.esc:
        return True
    else:
        return False

def is_shift(key):
    if isinstance(key, Key) and ( key == Key.shift or key == Key.shift_r ):
        return True
    else:
        return False

def is_ctrl(key):
    if isinstance(key, Key) and ( key == Key.ctrl or key == Key.ctrl_r ):
        return True
    else:
        return False

def is_alt(key):
    if isinstance(key, Key) and ( key == Key.alt or key == Key.alt_r ):
        return True
    else:
        return False

def is_cmd(key):
    if isinstance(key, Key) and ( key == Key.cmd or key == Key.cmd_r ):
        return True
    else:
        return False

def is_upper_alpha(key):
    if isinstance(key, KeyCode) and key.char != None and key.char.isalpha() and key.char.isupper():
        return True
    else:
        return False

def is_lower_alpha(key):
    if isinstance(key, KeyCode) and key.char != None and key.char.isalpha() and key.char.islower():
        return True
    else:
        return False

def is_shiftable(key):
    if get_key_code(key) in k2c_shift:
        return True
    else:
        return False

def get_key_code(key):
    if isinstance(key, Key):
        return key.value.vk
    elif isinstance(key, KeyCode):
        return key.vk
    else:
        return -1

def get_key_name(key):
    if isinstance(key, Key):
        name = key.name
    elif isinstance(key, KeyCode):
        name = key.char
    else:
        name = '' #'<{!r},{!r},ELSE>".format(type(key),key)'
    if name == None:
        name = '' #"<{!r},{!r},None>".format(type(key),key)
    return name

def char2keycode(c):
    k = c2k.get(c)
    ksf = c2k_shift.get(c)
    if k != None:
        return [k]
    elif ksf != None:
        return [c2k_special['shift'],ksf]
    else:
        return []

def key2char(key):
    k = get_key_code(key)
    n = get_key_name(key)
    if k in k2c_shift:
        return n if n != None else ''
    elif k in k2c:
        return k2c[k]
    else:
        return ''

def key2char_bot(key, shift):
    k = get_key_code(key)
    if is_upper_alpha(key):
        shift = True
    c = k2c.get(k)
    csf = k2c_shift.get(k)
    if shift == False and c != None:
        return c
    elif shift == True and csf != None:
        return csf
    else:
        return ''

def keycode2name(keycode):
    name1 = k2c_special.get(keycode)
    name2 = k2c.get(keycode)
    if name1 != None:
        return '{!r}'.format(name1)
    elif name2 != None:
        return '{!r}'.format(name2)
    else:
        return 'Unknow<{}>'.format(keycode)

controller = Controller()

def press_key(keylist):
    if len(keylist) == 0:
        pass
    elif len(keylist) == 1:
        with controller.pressed( KeyCode( keylist[0])):
            pass
    elif len(keylist) == 2:
        with controller.pressed( KeyCode( keylist[0])):
            with controller.pressed( KeyCode( keylist[1])):
                pass

def press_char(charlist):
    for c in charlist:
        klist = char2keycode(c)
        press_key( klist)
