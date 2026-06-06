#!/usr/bin/env python3
"""
fuzz.py — Phase 3: Automated fuzzing with pwntools cyclic pattern.
Usage: fuzz.py <binary>

Runs the binary with a cyclic(1024) payload. Captures crashes,
extracts the offset, and reports register state.
"""

import argparse
import sys
import os
from pwn import *

def fuzz_binary(binary_path, timeout=5):
    context.log_level = "error"

    payload = cyclic(1024, n=8)  # 64-bit by default

    try:
        p = process(binary_path, timeout=timeout)
        p.sendline(payload)
        p.wait_for_close(timeout=timeout)
    except EOFError:
        pass  # Binary might exit early
    except Exception as e:
        print(f"[WARN] Exception during fuzzing: {e}")

    # Check for core dump
    core_path = f"/tmp/core.{binary_path.split('/')[-1]}"
    if os.path.exists(f"core.{binary_path.split('/')[-1]}"):
        core_path = f"core.{binary_path.split('/')[-1]}"

    if not os.path.exists(core_path):
        # Try to find core dump in cwd
        cores = [f for f in os.listdir(".") if f.startswith("core.")]
        if cores:
            core_path = cores[0]

    if os.path.exists(core_path):
        core = Corefile(core_path)
        rip = core.registers.get("rip", 0)
        rsp = core.registers.get("rsp", 0)
        print(f"========== CRASH REPORT ==========")
        print(f"Signal: {core.signal}")
        print(f"Faulting address: {hex(core.fault_addr)}")
        print(f"RIP: {hex(rip)}")
        print(f"RSP: {hex(rsp)}")
        try:
            offset = cyclic_find(rip & 0xFFFFFFFF_FFFFFFFF, n=8)
            print(f"Cyclic offset (RIP): {offset}")
        except:
            pass
        try:
            offset_rsp = cyclic_find(rsp & 0xFFFFFFFF_FFFFFFFF, n=8)
            print(f"Cyclic offset (RSP): {offset_rsp}")
        except:
            pass
        print(f"Core dump: {core_path}")
        return True, core
    else:
        print("[INFO] No crash detected (no core dump found).")
        return False, None

def main():
    parser = argparse.ArgumentParser(description="Fuzz binary with cyclic pattern")
    parser.add_argument("binary", help="Target binary")
    parser.add_argument("--timeout", type=int, default=5, help="Timeout in seconds")
    parser.add_argument("--output", default="notes.md", help="Notes file to append")
    parser.add_argument("--length", type=int, default=1024, help="Cyclic length")
    args = parser.parse_args()

    if not os.path.exists(args.binary):
        print(f"[ERROR] Binary not found: {args.binary}")
        sys.exit(1)

    # Generate payload of requested length
    global cyclic
    payload = cyclic(args.length, n=8)

    crashed, core = fuzz_binary(args.binary, args.timeout)

    if crashed and core and args.output and os.path.exists(args.output):
        with open(args.output, "a") as f:
            f.write(f"\n## Fuzzing: {args.binary} ({os.path.basename(args.binary)})\n\n")
            f.write(f"- Signal: {core.signal}\n")
            f.write(f"- Fault address: {hex(core.fault_addr)}\n")
            f.write(f"- RIP: {hex(core.registers.get('rip', 0))}\n")
            f.write(f"- RSP: {hex(core.registers.get('rsp', 0))}\n")
            try:
                off = cyclic_find(core.registers.get("rip", 0) & 0xFFFFFFFF_FFFFFFFF, n=8)
                f.write(f"- Offset to RIP: {off}\n")
            except:
                pass

if __name__ == "__main__":
    main()
