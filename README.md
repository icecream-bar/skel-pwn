# PWN/RE Agent Workspace

CTF PWN/Reverse Engineering agentic workspace using opencode + local LLM (qwen3:14b via Ollama) + Docker.

## Quick Start

### 1. Build the environment once

```bash
docker-compose build
```

> This builds the `pwn-re:latest` image. You only need to run this once, or again after pulling updates to the Dockerfile.

### 2. Use the helper script per-challenge

The `pwn-run` script wraps `docker run` with the correct volume mounts, security options, and platform settings. Use it for every command you'd normally run inside the container:

```bash
# Initialize a new challenge workspace
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

If `pwn-re:latest` doesn't exist locally, `./pwn-run` will warn you and trigger `docker-compose build` automatically.

### Manual `docker run` (advanced)

If you prefer to call Docker directly (e.g., from CI or another script), use:

```bash
docker run \
    --rm \
    -v "$(pwd):/workspace" \
    -w /workspace \
    --platform linux/amd64 \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    pwn-re:latest \
    <command>
```

Or the legacy `docker-compose run` form:

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
