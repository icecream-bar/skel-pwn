#!/usr/bin/env python3

from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.bits = 64
gs = \'\'\'
continue
\'\'\'

elf = context.binary = ELF('./{}')
libc = ELF(elf.runpath + b'/libc.so.6')
rop = ROP(elf)

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    if args.REMOTE:
        return remote('127.0.0.1', 5555)
    else:
        return process(elf.path)
r = start()

#============ exploit here ================

#============= interactive ================

r.interactive()
