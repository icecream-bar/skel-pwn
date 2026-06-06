#!/bin/bash
# recon.sh — Phase 1: Static reconnaissance
# Usage: ./recon.sh <binary>

set -e

BINARY="${1:-./binary}"
OUTDIR="${2:-.}"
NOTES="$OUTDIR/notes.md"

if [[ ! -f "$BINARY" ]]; then
    echo "[ERROR] Binary not found: $BINARY"
    exit 1
fi

echo "========== RECON REPORT =========="
echo "Binary: $BINARY"
echo "Date: $(date)"
echo ""

echo "--- file ---"
file "$BINARY"
echo ""

echo "--- checksec ---"
checksec --file="$BINARY" 2>/dev/null || echo "checksec not found"
echo ""

echo "--- readelf -h ---"
readelf -h "$BINARY"
echo ""

echo "--- readelf -s ---"
readelf -s "$BINARY" | head -n 100
echo ""

echo "--- strings ---"
strings -n 6 "$BINARY" | grep -E '[a-zA-Z]{6,}' | head -n 50
echo ""

echo "--- objdump entry point (first 200 lines) ---"
objdump -d "$BINARY" | head -n 200
echo ""

# Update notes.md
if [[ -f "$NOTES" ]]; then
    {
        echo ""
        echo "## Recon: $(date)"
        echo ""
        echo "\`\`\`"
        file "$BINARY"
        echo "\`\`\`"
    } >> "$NOTES"
fi

echo "[OK] Recon complete. Notes appended to $NOTES"
