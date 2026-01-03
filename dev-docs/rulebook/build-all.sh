#!/bin/bash

# This script builds both the PDF and web versions of the GPSA Rulebook
# Usage: ./dev-docs/rulebook/build-all.sh

set -e  # Exit on any error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "=========================================="
echo "GPSA Rulebook - Full Build Process"
echo "=========================================="
echo ""

# Step 1: Assemble the modular markdown files into rulebook.md
echo "Step 1: Assembling modular markdown files..."
bash "$SCRIPT_DIR/assemble-rulebook.sh"
echo ""

# Step 2: Build PDF using the existing dev-docs/build.sh
echo "Step 2: Building PDF..."
bash "$PROJECT_ROOT/dev-docs/build.sh" rulebook
echo ""

# Step 3: Build web version using mkdocs
echo "Step 3: Building web version with MkDocs..."

# Check if mkdocs is available
if ! command -v mkdocs &> /dev/null; then
    echo "Warning: mkdocs not found. Attempting to build using Docker..."

    # Build Docker image from rulebook directory
    cd "$SCRIPT_DIR"
    docker build -t gpsa-mkdocs-builder .

    # Run mkdocs build with repo root mounted (so relative paths work)
    echo "Building site with Docker..."
    docker run --rm \
        -v "$PROJECT_ROOT:/work" \
        -w /work/dev-docs/rulebook \
        gpsa-mkdocs-builder \
        mkdocs build
else
    # Build using local mkdocs installation
    cd "$SCRIPT_DIR"
    mkdocs build
fi

echo ""
echo "=========================================="
echo "Build Complete!"
echo "=========================================="
echo "PDF:  dev-docs/rulebook.pdf"
echo "Web:  docs/rulebook/ (served from GitHub Pages)"
echo ""
echo "To preview web version locally:"
echo "  cd dev-docs/rulebook && mkdocs serve"
echo "  or: docker-compose up"
echo ""
