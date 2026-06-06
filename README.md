# PWN/RE Agent Workspace

CTF PWN/Reverse Engineering agentic workspace using opencode + local LLM (qwen3:14b via Ollama) + Docker.

## Quick Start

### 1. One-time setup: build the Docker image

```bash
docker-compose build
```

This creates the `pwn-re:latest` image locally. You only need to run this once (or when the `Dockerfile` changes).

### 2. Per-challenge workflow

Use the `pwn-run` helper to execute any command inside the container. It automatically builds the image if missing.

```bash
# Init a new challenge workspace
./pwn-run ./tools/init_workspace.sh [binary_name]

# Run recon
./pwn-run ./tools/recon.sh ./binary

# Decompile a function
./pwn-run ./tools/decompile.sh main

# Debug with GDB batch
./pwn-run ./tools/gdb_batch.py ./binary --cmds 'break main; run; bt; info registers'

# Fuzz for crashes
./pwn-run ./tools/fuzz.py ./binary
```

## `pwn-run` Helper

`pwn-run` is a lightweight wrapper around `docker run` that:

- Auto-builds `pwn-re:latest` if the image is not found locally.
- Mounts the current directory to `/workspace` inside the container.
- Adds the required Docker flags for PWN/RE work (`--cap-add=SYS_PTRACE`, `--security-opt seccomp=unconfined`, `--platform linux/amd64`).
- Passes all remaining arguments through as the command to run inside the container.

```bash
# Usage
./pwn-run <command> [args...]
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

## Docker Execution (Manual)

All commands run inside the `pwn-re` container with volume mount `.:/workspace`.

If you prefer not to use the `pwn-run` helper, you can run commands manually:

```bash
docker-compose run --rm pwn bash -c "cd /workspace && ./tools/recon.sh ./binary"
```

Or with plain `docker run`:

```bash
docker run --rm -v "$(pwd):/workspace" -w /workspace \
    --platform linux/amd64 \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    pwn-re:latest ./tools/recon.sh ./binary
```

## Requirements

- Docker (or Colima on macOS)
- Ollama with `qwen3:14b` model
- opencode with skill discovery enabled
