#!/usr/bin/env python
import re

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

if __name__ == "__main__":
    pass
