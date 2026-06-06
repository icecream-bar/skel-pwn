#!/bin/bash
# decompile.sh — Phase 2: Decompilation via radare2
# Usage: ./decompile.sh <binary> <function_name_or_address>

set -e

BINARY="${1:-./binary}"
FUNC="${2:-main}"
OUTDIR="${3:-.}"
NOTES="$OUTDIR/notes.md"

if [[ ! -f "$BINARY" ]]; then
    echo "[ERROR] Binary not found: $BINARY"
    exit 1
fi

echo "========== DECOMPILATION: $FUNC =========="
echo "Binary: $BINARY"
echo "Function: $FUNC"
echo ""

# Try r2ghidra-dec first (pdg), fallback to pdf
OUTPUT=$(r2 -A -q -c "s $FUNC; pdg" "$BINARY" 2>/dev/null) || true

if [[ -z "$OUTPUT" ]] || echo "$OUTPUT" | grep -q "Cannot find function"; then
    echo "[WARN] r2ghidra-dec failed or function not found. Falling back to disassembly (pdf)."
    OUTPUT=$(r2 -A -q -c "s $FUNC; pdf" "$BINARY" 2>/dev/null) || true
fi

if [[ -z "$OUTPUT" ]]; then
    echo "[ERROR] Failed to decompile/disassemble $FUNC"
    exit 1
fi

echo "$OUTPUT"
echo ""

# Update notes.md
if [[ -f "$NOTES" ]]; then
    {
        echo ""
        echo "## Decompile: $FUNC ($(date))"
        echo ""
        echo "\`\`\`c"
        echo "$OUTPUT"
        echo "\`\`\`"
    } >> "$NOTES"
fi

echo "[OK] Decompilation complete. Notes appended to $NOTES"
