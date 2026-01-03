#!/bin/bash

# This script assembles the modular markdown files from docs/ into a single
# rulebook.md file for PDF generation using pandoc.
#
# It preserves the YAML front matter and concatenates files in the order
# specified in mkdocs.yml navigation.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DOCS_DIR="$SCRIPT_DIR/docs"
OUTPUT_FILE="$SCRIPT_DIR/rulebook.md"

echo "Assembling rulebook from modular markdown files..."

# Start with YAML front matter (preserved from original rulebook.md)
cat > "$OUTPUT_FILE" << 'EOF'
---
title: "GPSA Rulebook"
date: "December 2025"
draft: true
titlepage: true
titlepage-color: "FFFFFF"
titlepage-text-color: "002366"
titlepage-rule-color: "002366"
titlepage-rule-height: 1
titlepage-logo: "assets/gpsa_logo.png"
logo-width: 120mm
toc-own-page: true
classoption: twoside
numbersections: true
toc: 'heading=false'
---

EOF

# Define the order of files based on mkdocs.yml navigation
# Skip index.md as it's just an introduction for the web version
FILES=(
    "definitions.md"
    "eligibility-and-rosters.md"
    "officials.md"
    "order-of-events.md"
    "conduct-of-meets.md"
    "scoring.md"
    "awards.md"
    "facilities.md"
)

# Concatenate each file
for file in "${FILES[@]}"; do
    if [ -f "$DOCS_DIR/$file" ]; then
        echo "Adding $file..."

        # Add file content normally, skipping any YAML front matter
        awk '
            BEGIN { in_yaml = 0 }
            /^---$/ {
                if (NR == 1) { in_yaml = 1; next }
                else if (in_yaml) { in_yaml = 0; next }
            }
            !in_yaml { print }
        ' "$DOCS_DIR/$file" >> "$OUTPUT_FILE"

        # Add a blank line between files for safety
        echo "" >> "$OUTPUT_FILE"
    else
        echo "Warning: $file not found in $DOCS_DIR"
    fi
done

echo "✓ Assembled rulebook.md successfully"
echo "  Output: $OUTPUT_FILE"
