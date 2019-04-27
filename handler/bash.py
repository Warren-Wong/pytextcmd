import os
import pty
import sys
import time
import subprocess
import select
import re

class bash:
    def __init__(self):
        self.m, self.s = pty.openpty()
        self.proc = subprocess.Popen("/bin/bash", stdin=self.s, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,close_fds=True,preexec_fn=os.setsid)
        self.stdin('cd ~\n')

    def stdin(self, cmd):
        os.write(self.m,cmd.encode())

    def stdout(self):
        s = ''
        rds, wds, nds = select.select([self.proc.stdout.fileno()],[],[],0.1)
        if len(rds)>0:
            for d in rds:
                s += self.proc.stdout.read1().decode()
        rds, wds, nds = select.select([self.proc.stderr.fileno()],[],[],0)
        if len(rds)>0:
            for d in rds:
                s += self.proc.stderr.read1().decode()
        return s

    def close(self):
        os.close(self.m)
        os.close(self.s)
        self.proc.kill()

gbash = bash()

def exec_cmd( cmd):
    gbash.stdin(cmd)
    resp = gbash.stdout()
    resp = cmd + resp
    return resp
