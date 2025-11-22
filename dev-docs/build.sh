#!/bin/bash

# This script compiles a Markdown document to PDF using Docker and pandoc.
# Usage: ./dev-docs/build.sh <document_name>
# Example: ./dev-docs/build.sh rulebook

# Check for document name
if [ -z "$1" ]; then
    echo "Usage: ./dev-docs/build.sh <document_name>"
    exit 1
fi

DOC_NAME=$1
DEV_DOCS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT=$(dirname "$DEV_DOCS_DIR")

DOCKER_IMAGE_NAME="gpsa-doc-builder"

# Build the docker image
echo "Building Docker image..."
docker build -t $DOCKER_IMAGE_NAME "$DEV_DOCS_DIR"

# Run the compilation in a docker container
echo "Running pandoc compilation in Docker..."
docker run --rm -v "$PROJECT_ROOT:/work" --workdir /work "$DOCKER_IMAGE_NAME" /bin/sh -c "
    pandoc --template=dev-docs/_template/template.tex \
           -s dev-docs/$DOC_NAME/$DOC_NAME.md \
           -o dev-docs/$DOC_NAME.pdf \
           --number-sections \
           --toc
"

if [ $? -eq 0 ]; then
    echo "PDF generated: dev-docs/$DOC_NAME.pdf"
else
    echo "Error during Docker execution."
fi
