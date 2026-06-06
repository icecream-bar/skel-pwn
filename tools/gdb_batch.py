#!/usr/bin/env python3
"""
gdb_batch.py — Non-interactive GDB wrapper for agentic analysis.
Usage: gdb_batch.py <binary> [options]

Commands can be passed as a semicolon-separated string via --cmds.
Supports shortcuts:
    telescope       → x/10gx $rsp
    vmmap          → info proc mappings
    regs           → info registers
    disas <func>   → disassemble <func>
    bt             → backtrace
"""

import argparse
import subprocess
import sys
import tempfile
import os
import signal

GDB_PATH = os.environ.get("GDB", "/usr/local/bin/pwndbg")

SHORTCUTS = {
    "telescope": "x/10gx $rsp",
    "vmmap": "info proc mappings",
    "regs": "info registers",
    "bt": "backtrace",
}

def expand_shortcuts(cmds_str):
    cmds = []
    for cmd in cmds_str.split(";"):
        cmd = cmd.strip()
        if cmd in SHORTCUTS:
            cmds.append(SHORTCUTS[cmd])
        elif cmd.startswith("disas "):
            func = cmd[6:].strip()
            cmds.append(f"disassemble {func}")
        else:
            cmds.append(cmd)
    return cmds

def run_gdb(binary, cmds, timeout=30):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".gdb", delete=False) as f:
        f.write("set pagination off\n")
        f.write("set confirm off\n")
        for cmd in cmds:
            f.write(cmd + "\n")
        f.write("quit\n")
        script = f.name

    try:
        proc = subprocess.run(
            [GDB_PATH, "-q", "-batch", "-x", script, "--", binary],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return "", "[ERROR] GDB timed out", -1
    finally:
        os.unlink(script)

def main():
    parser = argparse.ArgumentParser(description="Non-interactive GDB batch runner")
    parser.add_argument("binary", help="Target binary")
    parser.add_argument("--cmds", default="", help="Semicolon-separated GDB commands")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--output", default="notes.md", help="Notes file to append")
    args = parser.parse_args()

    if not os.path.exists(args.binary):
        print(f"[ERROR] Binary not found: {args.binary}")
        sys.exit(1)

    cmds = expand_shortcuts(args.cmds)
    print(f"[INFO] Running GDB with commands: {cmds}")

    stdout, stderr, rc = run_gdb(args.binary, cmds, args.timeout)

    print("========== GDB STDOUT ==========")
    print(stdout)
    if stderr:
        print("========== GDB STDERR ==========")
        print(stderr)
    print(f"========== RETURN CODE: {rc} ==========")

    # Append to notes.md
    if args.output and os.path.exists(args.output):
        with open(args.output, "a") as f:
            f.write(f"\n## GDB Batch: {args.cmds} ({os.path.basename(args.binary)})\n\n")
            f.write("```\n")
            f.write(stdout)
            if stderr:
                f.write("\n[stderr]\n")
                f.write(stderr)
            f.write("\n```\n")

    sys.exit(rc if rc is not None else 0)

if __name__ == "__main__":
    main()
