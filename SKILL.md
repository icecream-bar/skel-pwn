---
name: pwn-re
description: >
  CTF PWN/RE agentic workspace for binary exploitation and reverse engineering.
  Deployed inside a Docker container. Supports x86_64 Linux ELF binaries.
  Uses qwen3:14b via Ollama as the reasoning engine.
  Provides slash commands: /pwn-init, /pwn-recon, /pwn-decompile, /pwn-gdb, /pwn-fuzz, /pwn-exploit, /pwn-test.
---

# PWN/RE Agent Skill

## Purpose

Analyze Linux ELF binaries for CTF challenges. Identify vulnerabilities, perform reverse engineering, and develop working exploits using `pwntools`, `gdb`+`pwndbg`, and `radare2`.

## Target Environment

- **Host**: Intel x86_64 macOS (Docker Desktop)
- **Container**: `pwn-re:latest` (extends `pwntools/pwntools:stable`)
- **Model**: `qwen3:14b` via Ollama (tool-calling enabled, thinking mode)
- **Execution**: All analysis/debugging/exploitation happens inside the Docker container via `docker compose run --rm pwn <cmd>`

## When to Use This Skill

Invoke when the user:
- Says "run recon", "analyze binary", "check protections"
- Says "decompile main", "show me <func>", "what does this function do"
- Says "set breakpoint", "inspect stack", "run gdb", "debug this"
- Says "fuzz input", "find crash", "test buffer"
- Says "create exploit", "build rop", "write exploit"
- Says "test exploit", "run locally"
- Uses slash commands: `/pwn-init`, `/pwn-recon`, `/pwn-decompile`, `/pwn-gdb`, `/pwn-fuzz`, `/pwn-exploit`, `/pwn-test`

## Agent Roles & Autonomy

The skill defines 4 autonomous agent roles. Agents explore the binary freely and consult `notes.md` before asking the user for direction.

### Recon Agent
- **Tools**: `recon.sh`
- **Goal**: Discover binary metadata, protections, symbols, strings.
- **Autonomy**: Can run recon up to 3 times per session without user intervention.

### Decompiler Agent
- **Tools**: `decompile.sh`
- **Goal**: Request decompilation of any function by name or address.
- **Output**: Pseudo-C from `r2ghidra-dec` (fallback to disassembly via `pdf`).

### Debugger Agent
- **Tools**: `gdb_batch.py`
- **Goal**: Non-interactive GDB execution. Inspect registers, memory, stack, backtraces.
- **Shortcuts**: `telescope`, `vmmap`, `regs`, `disas <func>`, `bt`

### Exploitation Agent
- **Tools**: `exploit.py` template, `fuzz.py`
- **Goal**: Synthesize findings from `notes.md` into a working exploit.
- **Constraint**: Must verify offsets and gadgets against recon notes before generating code.

## Workflow

### Step 1 — Initialize Workspace

User says: `/pwn-init` or "init pwn workspace"

```bash
./tools/init_workspace.sh
```

This generates:
- `AGENTS.md` — per-project context with binary metadata
- `exploit.py` — pwntools exploit template
- `notes.md` — structured reverse engineering notes
- `.git/` — initialized repo

### Step 2 — Reconnaissance

User says: `/pwn-recon` or "run recon"

```bash
./tools/recon.sh ./binary
```

Captures: file type, checksec, symbols, strings, entry point disassembly. Updates `notes.md`. Auto-commits.

### Step 3 — Decompilation

User says: `/pwn-decompile main` or "decompile main"

```bash
./tools/decompile.sh main
```

Appends pseudo-C to `notes.md`. Auto-commits.

### Step 4 — Dynamic Analysis

User says: `/pwn-gdb 'break main; run'` or "set breakpoint at main"

```bash
./tools/gdb_batch.py ./binary --cmds 'break main; run; bt; info registers'
```

Captures stdout, signals, register state. Updates `notes.md`.

### Step 5 — Fuzzing

User says: `/pwn-fuzz` or "fuzz input"

```bash
./tools/fuzz.py ./binary
```

Runs cyclic pattern, identifies crash offset. Updates `notes.md`.

### Step 6 — Exploit Development

User says: `/pwn-exploit` or "create exploit"

Agent reads `notes.md`, fills in `exploit.py` template with:
- Overflow offset
- ROP gadgets / libc offsets
- Shellcode or ret2libc strategy

### Step 7 — Exploit Testing

User says: `/pwn-test` or "test exploit"

```bash
docker compose run --rm pwn python3 /workspace/exploit.py
```

Reports: local success/failure, shell obtained flag.

## Docker Execution

All commands run inside the `pwn-re` container. Volume mount: `.:/workspace`

```bash
docker compose run --rm pwn bash -c "cd /workspace && <cmd>"
```

## Notes & Git History

Agents auto-commit `notes.md` after each significant analysis step:
- `recon: identified protections for <binary>`
- `decompile: documented main() logic`
- `debug: crash at offset <N> in <func>`
- `exploit: local test successful`

Local-only. User manually pushes when ready.

## Model Considerations (qwen3:14b)

- Excellent at static recon and summarizing disassembly
- Good at understanding C logic from decompiled output
- Good at identifying buffer overflows and format string bugs
- ROP chain construction: hit or miss — always verify gadgets
- Heap exploitation (tcache, fastbin): needs guidance — document constraints explicitly
- Blind exploitation: struggles — feed it recon data generously

**Prompting strategy**: When asking qwen3 to build an exploit, always provide the current `notes.md` content as context. Ask it to verify offsets before emitting code.
