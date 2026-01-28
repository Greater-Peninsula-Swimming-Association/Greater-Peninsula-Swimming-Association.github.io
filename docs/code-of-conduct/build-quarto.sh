#!/bin/bash

# This script builds both PDF and HTML versions of the GPSA Code of Conduct using Quarto
# Usage: ./docs/code-of-conduct/build-quarto.sh

set -e  # Exit on any error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "=========================================="
echo "GPSA Code of Conduct - Quarto Build"
echo "=========================================="
echo ""

# Check if Quarto is installed
if ! command -v quarto &> /dev/null; then
    echo "Error: Quarto is not installed."
    echo ""
    echo "Please install Quarto:"
    echo "  - macOS: brew install quarto"
    echo "  - Or download from: https://quarto.org/docs/get-started/"
    echo ""
    exit 1
fi

# Display Quarto version
echo "Using Quarto version: $(quarto --version)"
echo ""

# Navigate to code-of-conduct directory
cd "$SCRIPT_DIR"

# Render both formats
echo "Rendering Code of Conduct (HTML + PDF)..."
quarto render

echo ""
echo "=========================================="
echo "Build Complete!"
echo "=========================================="
echo "PDF:  docs/code-of-conduct/public-html/GPSA-Code-of-Conduct.pdf"
echo "HTML: docs/code-of-conduct/public-html/ (can be served from GitHub Pages)"
echo ""
echo "To preview HTML locally:"
echo "  cd docs/code-of-conduct"
echo "  quarto preview"
echo ""
