from pynput import keyboard

kbctrl = keyboard.Controller()

char_key_map = {
None:[],
'':[],
'`':[keyboard.KeyCode(vk=50)],
'1':[keyboard.KeyCode(vk=18)],
'2':[keyboard.KeyCode(vk=19)],
'3':[keyboard.KeyCode(vk=20)],
'4':[keyboard.KeyCode(vk=21)],
'5':[keyboard.KeyCode(vk=23)],
'6':[keyboard.KeyCode(vk=22)],
'7':[keyboard.KeyCode(vk=26)],
'8':[keyboard.KeyCode(vk=28)],
'9':[keyboard.KeyCode(vk=25)],
'0':[keyboard.KeyCode(vk=29)],
'-':[keyboard.KeyCode(vk=27)],
'=':[keyboard.KeyCode(vk=24)],
'~':[keyboard.Key.shift,keyboard.KeyCode(vk=50)],
'!':[keyboard.Key.shift,keyboard.KeyCode(vk=18)],
'@':[keyboard.Key.shift,keyboard.KeyCode(vk=19)],
'#':[keyboard.Key.shift,keyboard.KeyCode(vk=20)],
'$':[keyboard.Key.shift,keyboard.KeyCode(vk=21)],
'%':[keyboard.Key.shift,keyboard.KeyCode(vk=23)],
'^':[keyboard.Key.shift,keyboard.KeyCode(vk=22)],
'&':[keyboard.Key.shift,keyboard.KeyCode(vk=26)],
'*':[keyboard.Key.shift,keyboard.KeyCode(vk=28)],
'(':[keyboard.Key.shift,keyboard.KeyCode(vk=25)],
')':[keyboard.Key.shift,keyboard.KeyCode(vk=29)],
'_':[keyboard.Key.shift,keyboard.KeyCode(vk=27)],
'+':[keyboard.Key.shift,keyboard.KeyCode(vk=24)],
'q':[keyboard.KeyCode(vk=12)],
'w':[keyboard.KeyCode(vk=13)],
'e':[keyboard.KeyCode(vk=14)],
'r':[keyboard.KeyCode(vk=15)],
't':[keyboard.KeyCode(vk=17)],
'y':[keyboard.KeyCode(vk=16)],
'u':[keyboard.KeyCode(vk=32)],
'i':[keyboard.KeyCode(vk=34)],
'o':[keyboard.KeyCode(vk=31)],
'p':[keyboard.KeyCode(vk=35)],
'[':[keyboard.KeyCode(vk=33)],
']':[keyboard.KeyCode(vk=30)],
'\\':[keyboard.KeyCode(vk=42)],
'Q':[keyboard.Key.shift,keyboard.KeyCode(vk=12)],
'W':[keyboard.Key.shift,keyboard.KeyCode(vk=13)],
'E':[keyboard.Key.shift,keyboard.KeyCode(vk=14)],
'R':[keyboard.Key.shift,keyboard.KeyCode(vk=15)],
'T':[keyboard.Key.shift,keyboard.KeyCode(vk=17)],
'Y':[keyboard.Key.shift,keyboard.KeyCode(vk=16)],
'U':[keyboard.Key.shift,keyboard.KeyCode(vk=32)],
'I':[keyboard.Key.shift,keyboard.KeyCode(vk=34)],
'O':[keyboard.Key.shift,keyboard.KeyCode(vk=31)],
'P':[keyboard.Key.shift,keyboard.KeyCode(vk=35)],
'{':[keyboard.Key.shift,keyboard.KeyCode(vk=33)],
'}':[keyboard.Key.shift,keyboard.KeyCode(vk=30)],
'|':[keyboard.Key.shift,keyboard.KeyCode(vk=42)],
'a':[keyboard.KeyCode(vk=0)],
's':[keyboard.KeyCode(vk=1)],
'd':[keyboard.KeyCode(vk=2)],
'f':[keyboard.KeyCode(vk=3)],
'g':[keyboard.KeyCode(vk=5)],
'h':[keyboard.KeyCode(vk=4)],
'j':[keyboard.KeyCode(vk=38)],
'k':[keyboard.KeyCode(vk=40)],
'l':[keyboard.KeyCode(vk=37)],
';':[keyboard.KeyCode(vk=41)],
"'":[keyboard.KeyCode(vk=39)],
'A':[keyboard.Key.shift,keyboard.KeyCode(vk=0)],
'S':[keyboard.Key.shift,keyboard.KeyCode(vk=1)],
'D':[keyboard.Key.shift,keyboard.KeyCode(vk=2)],
'F':[keyboard.Key.shift,keyboard.KeyCode(vk=3)],
'G':[keyboard.Key.shift,keyboard.KeyCode(vk=5)],
'H':[keyboard.Key.shift,keyboard.KeyCode(vk=4)],
'J':[keyboard.Key.shift,keyboard.KeyCode(vk=38)],
'K':[keyboard.Key.shift,keyboard.KeyCode(vk=40)],
'L':[keyboard.Key.shift,keyboard.KeyCode(vk=37)],
':':[keyboard.Key.shift,keyboard.KeyCode(vk=41)],
'"':[keyboard.Key.shift,keyboard.KeyCode(vk=39)],
'z':[keyboard.KeyCode(vk=6)],
'x':[keyboard.KeyCode(vk=7)],
'c':[keyboard.KeyCode(vk=8)],
'v':[keyboard.KeyCode(vk=9)],
'b':[keyboard.KeyCode(vk=11)],
'n':[keyboard.KeyCode(vk=45)],
'm':[keyboard.KeyCode(vk=46)],
',':[keyboard.KeyCode(vk=43)],
'.':[keyboard.KeyCode(vk=47)],
'/':[keyboard.KeyCode(vk=44)],
'Z':[keyboard.Key.shift,keyboard.KeyCode(vk=6)],
'X':[keyboard.Key.shift,keyboard.KeyCode(vk=7)],
'C':[keyboard.Key.shift,keyboard.KeyCode(vk=8)],
'V':[keyboard.Key.shift,keyboard.KeyCode(vk=9)],
'B':[keyboard.Key.shift,keyboard.KeyCode(vk=11)],
'N':[keyboard.Key.shift,keyboard.KeyCode(vk=45)],
'M':[keyboard.Key.shift,keyboard.KeyCode(vk=46)],
'<':[keyboard.Key.shift,keyboard.KeyCode(vk=43)],
'>':[keyboard.Key.shift,keyboard.KeyCode(vk=47)],
'?':[keyboard.Key.shift,keyboard.KeyCode(vk=44)],
'\n':[keyboard.Key.enter],
'\t':[keyboard.Key.tab],
'\b':[keyboard.Key.backspace],
' ':[keyboard.Key.space]
}

def char2key(c):
    return char_key_map.get(c)

def char2press(c):
    key = char2key(c)
    if key == None or len(key) == 0:
        raise Exception('char2press: unknown char')
    elif len(key) == 1:
        kbctrl.press(key[0])
    else:
        with kbctrl.pressed(key[0]):
            kbctrl.press(key[1])

def key2char(key):
    c = None
    if(type(key) == keyboard.Key):
        if( key == keyboard.Key.enter):
            c = '\n'
        elif( key == keyboard.Key.backspace):
            c = '\b'
        elif( key == keyboard.Key.tab):
            c = '\t'
        elif( key == keyboard.Key.space):
            c = ' '
    elif( type(key) == keyboard.KeyCode):
        c = str(key)[1]
    else:
        raise Exception('key2char: cannot match char')
    return c
