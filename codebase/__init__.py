import os

def load_file_to_lines( path):
    lines = []
    _file = open(path, "r")
    for _line in _file:
        lines.append(_line)
    _file.close()
    return lines

def is_tag_line( line):
    return len(line) >= 3 and line.find('###') == 0

def is_empty_line( line):
    return len(line.strip()) == 0

def tag_line_to_list( tagline):
    taglist = []
    for t in tagline[3:].split(','):
        if len(t.strip()) > 0:
            taglist.append( t.strip())
    return taglist

def strip_empty_line( lines):
    while len(lines) > 0:
        if is_empty_line(lines[0]):
            lines.remove( lines[0])
        else:
            break
    while len(lines) > 0:
        if is_empty_line(lines[-1]):
            lines.pop()
        else:
            break
    return lines

def find_tag_code_block( lines):
    codebase = []
    block = None
    for line in lines:
        if is_tag_line(line):
            if block != None:
                codebase.append( block)
            block = {'tag':line, 'code':[]}
            continue
        elif block != None:
            block['code'].append(line)
    return codebase

def format_tag_code( tagcode):
    tagcode['tag'] = tag_line_to_list(tagcode['tag'])
    tagcode['code'] = strip_empty_line(tagcode['code'])
    return tagcode

class TagCode:
    def __init__(self, taglist, codelines=[]):
        self.taglist = taglist
        self.codelines = codelines
    def has(self, otherlist):
        cnt = 0
        if otherlist == None:
            return 0
        if isinstance(otherlist,str):
            otherlist = [ otherlist ]
        for ot in otherlist:
            for t in self.taglist:
                if tag_is_equal(t,ot):
                    cnt += 1
        return cnt
    def add_tag(self, otherlist):
        if isinstance(otherlist,str):
            otherlist = [ otherlist ]
        self.taglist.extend(otherlist)
    @classmethod
    def tag_is_equal( clr, t1, t2):
        if (t1.find(t2) == 0 or t2.find(t1) == 0):
            return True
        else:
            return False
    def __str__(self):
        ret = ''
        ret += str(self.taglist)
        ret += "\n"
        for l in self.codelines:
            ret += l
        return ret

def get_codebase_root():
    dir_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'base')
    return dir_path

def make_file( path):
    filename, file_extension = os.path.splitext(os.path.basename(path))
    fileTags = [ t for t in filename.split('_') if len(t) > 0]
    lines = load_file_to_lines(path)
    codebase_raw = find_tag_code_block( lines)
    codebase = []
    for tc in codebase_raw:
        tc = format_tag_code(tc)
        tc['tag'].extend(fileTags)
        codebase.append( TagCode( tc['tag'], tc['code']))
    return codebase

def get_all_filepath( path):
    flist = [ os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.find('.') != 0 and f.find('_') != 0]
    return flist

def get_all_dirpath( path):
    dlist = [ os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d.find('.') != 0 and d.find('_') != 0]
    return dlist

def get_all_codefile( rootdir):
    flist = []
    rootdir = os.path.realpath(rootdir)
    f = get_all_filepath(rootdir)
    d = get_all_dirpath(rootdir)
    flist.extend( f)
    for sub in d:
        subflist = get_all_codefile(sub)
        flist.extend( subflist)
    return flist

def get_path_tag( path, rootdir):
    path = path.replace(rootdir,'')
    taglist = [ t for t in path.split(os.path.sep) if len(t) > 0]
    return taglist

def make( rootdir):
    codebase = []
    flist = get_all_codefile( rootdir)
    for f in flist:
        taglist = get_path_tag(os.path.dirname(f),rootdir)
        tclist = make_file(f)
        for tc in tclist:
            tc.add_tag(taglist)
        codebase.extend(tclist)
    return codebase

rootdir = os.path.dirname(os.getcwd())
codebase = make(rootdir)

def search( taglist):
    if not isinstance(taglist,list):
        taglist = [ taglist ]
    for tc in codebase:
        if tc.has( taglist) == len(taglist):
            print(tc)


'''
file = ' '.join(lines)

import statistics

def cal_loc_sim( a, b):
    if len(a) < len(b):
        a,b = b,a
    maxlen = max(len(a),len(b))+1
    base = len(a)-len(b)+1
    dff = a.find(b)
    dff = dff if dff >= 0  else base
    d = base/maxlen
    r = dff/base
    return (1-d)*(1-r)

def cal_sim( a, b):
    if len(a) < len(b):
        a,b = b,a
    maxlen = max(len(a),len(b))+1
    base = len(a)-len(b)+1
    dff = a.find(b)
    dff = dff if dff >= 0  else base
    d = base/maxlen
    r = dff/base
    return (1-r)

def cal_bool( a, b):
    if len(a) < len(b):
        a,b = b,a
    dff = a.find(b)
    if dff < 0:
        return 0
    else:
        return 1

def rank0(a, b, sym):
    return a,b

def rank1(a, b, sym):
    a,b = rank0(a, b, sym)
    for c in sym:
        a = a.replace(c,'.')
        b = b.replace(c,'.')
    return a,b

def rank2(a, b, sym):
    a,b = rank1( a,b,sym)
    a = a.replace('..','.')
    b = b.replace('..','.')
    return a,b

def rank3(a, b, sym):
    a,b = rank1( a,b,sym)
    a = a.replace('.','')
    b = b.replace('.','')
    return a,b

sym0 = ['']
print(sym0)

sym1 = ['aeiou','mn','lr','bp','td','ck','yi','fv','sxc']
print(sym1)

sym2 = []
for s in sym1:
    for ss in sym1:
        if ss.find(s) < 0:
            sym2.append(s+ss)
print(sym2)

sym3 = []
for s in sym1:
    for ss in sym2:
        if ss.find(s) < 0:
            sym3.append(s+ss)
print(sym3)

sym = [sym0,sym1,sym2,sym3]
rank = [rank0,rank1,rank2,rank3]

def compare(a, b, s, r):
    c = []
    for w in s:
        aa,bb = r(a,b,w)
        c.append( cal_bool(aa,bb))
    return c

a = 'funt'
s = 'rite'
s = 'inheritanc'
b = file
s = 'emheritanc'
s = 'extend'

print(a,b)
for i in range(0,4):
    c = compare(a,b,sym[i],rank[i])
    if len(c) > 1:
        print('s',i,'r',i,
                statistics.mean(c),
                max(c))
    else:
        print('s',i,'r',i,
                c[0],
                c[0])
'''
