# GPSA Rulebook - Build System

This directory contains the source files and build system for the GPSA Rulebook, which is published in both **PDF** and **web** formats.

## Directory Structure

```
rulebook/
├── docs/                    # Modular markdown source files (edit these!)
│   ├── index.md            # Web home page
│   ├── definitions.md
│   ├── eligibility-and-rosters.md
│   ├── officials.md
│   ├── order-of-events.md
│   ├── conduct-of-meets.md
│   ├── scoring.md
│   ├── awards.md
│   ├── facilities.md
│   └── stylesheets/        # Custom CSS for web version
├── mkdocs.yml              # MkDocs configuration for web version
├── rulebook.md             # AUTO-GENERATED - Combined file for PDF
├── assemble-rulebook.sh    # Script to build rulebook.md from docs/
├── build-all.sh            # Master build script (PDF + Web)
├── Dockerfile              # Docker config for MkDocs preview
└── docker-compose.yml      # Docker Compose for easy MkDocs server
```

## Quick Start

### Editing Content

1. **Edit the modular files** in `docs/` directory
2. DO NOT edit `rulebook.md` directly - it's auto-generated!

### Building Both Formats

Run the master build script from anywhere in the project:

```bash
./dev-docs/rulebook/build-all.sh
```

This will:
1. ✅ Assemble `docs/*.md` files into `rulebook.md`
2. ✅ Generate PDF → `dev-docs/rulebook.pdf`
3. ✅ Build web version → `../../docs/rulebook/`

### Building Just the PDF

```bash
# From project root
./dev-docs/build.sh rulebook
```

### Building Just the Web Version

```bash
# From rulebook directory
cd dev-docs/rulebook
mkdocs build
```

## Development Workflow

### Preview Web Version Locally

**Option 1: Using MkDocs directly** (requires Python + mkdocs)
```bash
cd dev-docs/rulebook
mkdocs serve
# Open http://localhost:8000
```

**Option 2: Using Docker Compose** (no local dependencies)
```bash
cd dev-docs/rulebook
docker-compose up
# Open http://localhost:8000
# Note: This is for preview only. For building, use build-all.sh
```

### Making Changes

1. Edit files in `docs/` directory
2. Preview changes:
   - Web: MkDocs auto-reloads on save
   - PDF: Re-run `./build-all.sh` to regenerate
3. Commit changes to Git
4. GitHub Pages will automatically publish the web version

## File Order for PDF

The PDF is assembled from `docs/` files in this order (defined in `mkdocs.yml` nav):

1. definitions.md
2. eligibility-and-rosters.md
3. officials.md
4. order-of-events.md
5. conduct-of-meets.md
6. scoring.md
7. awards.md
8. facilities.md

Note: `index.md` is excluded from PDF (web-only intro page)

## YAML Front Matter

The `assemble-rulebook.sh` script automatically adds this front matter to `rulebook.md`:

```yaml
---
title: "GPSA Rulebook"
date: "December 2025"
draft: true
titlepage: true
titlepage-logo: "assets/gpsa_logo.png"
logo-width: 120mm
toc-own-page: true
numbersections: true
---
```

To update the cover page:
- Edit these values in `assemble-rulebook.sh`
- DO NOT edit `rulebook.md` (changes will be overwritten)

## Technical Details

### PDF Generation
- Uses Pandoc with custom LaTeX template (`dev-docs/_template/template.tex`)
- Runs in Docker container (`texlive/texlive:latest`)
- Configured for GPSA branding (logo, colors, formatting)

### Web Generation
- Uses MkDocs with Material theme
- Custom CSS for GPSA branding (`docs/stylesheets/gpsa-custom.css`)
- Configured to output to `../../docs/rulebook/` (repo root `/docs/rulebook/`)
- When building with Docker, the entire repo is mounted to ensure relative paths work correctly
- Output is served by GitHub Pages from `/docs/rulebook/`

## Troubleshooting

**PDF won't build:**
- Ensure Docker is running
- Check that `assemble-rulebook.sh` ran successfully
- Verify `rulebook.md` was generated

**Web version not updating:**
- Run `mkdocs build` manually
- Check `mkdocs.yml` for syntax errors
- Ensure files in `docs/` are valid Markdown

**Content out of sync:**
- Always run `./build-all.sh` to rebuild both formats
- Check Git status to ensure all changes are committed

## CI/CD Integration

The build process can be automated in GitHub Actions:

```yaml
- name: Build Rulebook
  run: |
    ./dev-docs/rulebook/build-all.sh

- name: Commit generated files
  run: |
    git add dev-docs/rulebook.pdf docs/rulebook/
    git commit -m "Update rulebook PDF and web version"
```

## Questions?

See the main project documentation at `/DOCUMENTATION.md` or contact the GPSA webmaster.
