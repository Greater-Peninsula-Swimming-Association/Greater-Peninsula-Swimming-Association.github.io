FROM python:3.11-slim

# Set working directory
WORKDIR /docs

# Install MkDocs and Material theme
RUN pip install --no-cache-dir mkdocs mkdocs-material

# Expose MkDocs development server port
EXPOSE 8000

# Set environment variable for Python output
ENV PYTHONUNBUFFERED=1

# Run MkDocs server
# --dev-addr=0.0.0.0:8000 makes it accessible from outside the container
# --watch enables polling-based file watching (works better on macOS with Docker)
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000", "--watch", "docs", "--watch", "mkdocs.yml"]
