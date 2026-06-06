#!/bin/bash
# init_workspace.sh — Initialize a new CTF challenge workspace
# Usage: init_workspace.sh [binary_name]

set -e

BINARY="${1:-binary}"

echo "========== INIT PWN WORKSPACE =========="
echo "Binary: $BINARY"
echo ""

# Detect binary in current directory
if [[ -f "$BINARY" ]]; then
    echo "[OK] Found binary: $BINARY"
else
    echo "[WARN] Binary '$BINARY' not found. Please copy it to this directory."
fi

# Initialize git if not present
if [[ ! -d ".git" ]]; then
    git init
    echo "[OK] Git initialized"
fi

# Generate AGENTS.md
cat > AGENTS.md <<EOF
# CTF PWN/RE Agent Context

## Binary
- Name: ${BINARY}
- Path: ./${BINARY}
- Architecture: (to be filled by recon)
- Format: (to be filled by recon)

## Protections
- NX: (unknown)
- PIE: (unknown)
- Canary: (unknown)
- RELRO: (unknown)

## Interesting Functions
- main: (to be decompiled)

## Vulnerabilities
- (to be discovered)

## Exploit Strategy
- (to be determined)

## Building Blocks
- Overflow offset: (to be fuzzed)
- libc base: (if needed)
- Gadgets: (if ROP)
EOF

echo "[OK] Generated AGENTS.md"

# Generate notes.md skeleton
cat > notes.md <<EOF
# Reverse Engineering Notes

## Binary Metadata
- Binary: ${BINARY}
- Date: $(date)

## Recon

## Decompilation

## Dynamic Analysis

## Fuzzing / Crashes

## Exploit Development
EOF

echo "[OK] Generated notes.md"

# Generate exploit.py from template
if [[ ! -f "exploit.py" ]]; then
    cat > exploit.py <<PYEOF
#!/usr/bin/env python3
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.bits = 64
gs = '''
continue
'''

elf = context.binary = ELF('./${BINARY}')
# libc = ELF(elf.runpath + b'/libc.so.6')
rop = ROP(elf)

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    if args.REMOTE:
        return remote('127.0.0.1', 5555)
    else:
        return process(elf.path)

r = start()

# ============ exploit here ================

# ==========================================

r.interactive()
PYEOF
    chmod +x exploit.py
    echo "[OK] Generated exploit.py"
else
    echo "[SKIP] exploit.py already exists"
fi

# Create tools directory symlink or copy
if [[ ! -d "tools" ]]; then
    mkdir -p tools
    echo "[OK] Created tools/ directory"
fi

# First commit
git add AGENTS.md notes.md exploit.py tools/ 2>/dev/null || true
git commit -m "init: pwn workspace for ${BINARY}" || true

echo ""
echo "[SUCCESS] Workspace initialized!"
echo "Next steps:"
echo "  1. Place your binary as './${BINARY}'"
echo "  2. Run /pwn-recon or './tools/recon.sh ./${BINARY}'"
echo "  3. Run /pwn-decompile main"