# PWN/RE Agent Workspace

CTF PWN/Reverse Engineering agentic workspace using opencode + local LLM (qwen3:14b via Ollama) + Docker.

## Quick Start

```bash
# Build the container
docker-compose build

# Init a new challenge workspace
./tools/init_workspace.sh [binary_name]

# Run recon
./tools/recon.sh ./binary

# Decompile a function
./tools/decompile.sh main

# Debug with GDB batch
./tools/gdb_batch.py ./binary --cmds 'break main; run; bt; info registers'

# Fuzz for crashes
./tools/fuzz.py ./binary
```

## Docker Execution

All commands run inside the `pwn-re` container. Volume mount: `.:/workspace`

```bash
docker-compose run --rm pwn bash -c "cd /workspace && ./tools/recon.sh ./binary"
```

## Opencode Commands

After installing the skill, opencode provides these slash commands:

- `/pwn-init` — Initialize workspace with AGENTS.md, notes.md, exploit.py
- `/pwn-recon` — Run static reconnaissance on binary
- `/pwn-decompile` — Decompile a function by name or address
- `/pwn-gdb` — Run batched GDB commands
- `/pwn-fuzz` — Fuzz input to find crashes
- `/pwn-exploit` — Generate/update exploit.py from notes
- `/pwn-test` — Test exploit locally

## Architecture

4 autonomous agent roles defined in `SKILL.md`:

1. **Recon Agent** — Static analysis: file, checksec, readelf, strings, objdump
2. **Decompiler Agent** — Pseudo-C from radare2 (pdf fallback for r2ghidra-dec)
3. **Debugger Agent** — Non-interactive GDB with pwndbg
4. **Exploitation Agent** — Synthesize findings into working pwntools exploit

## Includes

- `pwntools` + `pwndbg` + `radare2`
- `ropgadget`, `one_gadget`, `seccomp-tools`
- Workspace init script with git tracking
- Exploit skeleton with tmux+GDB workflow preserved

## Requirements

- Docker (or Colima on macOS)
- Ollama with `qwen3:14b` model
- opencode with skill discovery enabled
