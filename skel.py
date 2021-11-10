#!/usr/bin/python3

import sys
import os

if len(sys.argv)<2:
    print("Usage: skel <binary>")
    sys.exit(0)

program = str(sys.argv[1])
current = os.getcwd()

skel = '''#!/usr/bin/python3
from pwn import *
gs = \'\'\'
continue
\'\'\'
#REMOTE = True      # test remote
REMOTE =False       # test local

elf = context.binary = ELF('./{}')

if REMOTE :
    #p = remote('REMOTEIP',PORT) # test remote
    p = remote('',PORT)
else:
	p = process('./{}')

#========= exploit here ===================


p.recvline()
p.sendline(payload)

#========= interactive ====================
p.interactive()
'''.format(program, program, program)
try:
    with open('xpl.py', 'w') as f:
        f.write(skel)
        f.close()
except:
    print("Can't write xpl.py!")
