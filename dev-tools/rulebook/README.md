# GPSA Rulebook

This directory contains the GPSA official rulebook in Markdown format, which is automatically converted to a professional PDF using Pandoc and the Eisvogel LaTeX template.

## Files

- **`rulebook.md`** - Source rulebook content in Markdown with YAML front matter
- **`assets/logo.png`** - GPSA logo used in the PDF titlepage
- **`compose.yml`** - Docker Compose configuration for local builds (x86_64 only)
- **`build.sh`** - Convenience script to run local builds

## Automatic PDF Generation (GitHub Actions)

The rulebook PDF is **automatically generated** whenever changes are pushed to this directory.

### Workflow Details

**Trigger Events:**
- Push to `dev-tools/rulebook/**` (any file in this directory)
- Manual trigger via [Actions tab](../../actions/workflows/build-pdf.yml)

**Workflow Steps:**
1. Downloads the Eisvogel LaTeX template
2. Runs Pandoc with XeLaTeX engine to convert Markdown → PDF
3. Uploads PDF as workflow artifact (downloadable for 90 days)
4. Commits `GPSA_Rulebook.pdf` to repository root (push events only)

**Output Location:**
- Repository root: `GPSA_Rulebook.pdf` (committed to repo)
- Workflow artifacts: Available in [Actions tab](../../actions) under each run

### Manual Workflow Trigger

To manually generate the PDF without making changes:

1. Go to **Actions** → **Build GPSA Rulebook PDF**
2. Click **Run workflow** → **Run workflow**
3. Wait ~2-3 minutes for completion
4. Download artifact from the workflow run page

## Local PDF Generation (Optional)

**Note:** Local builds require x86_64 architecture. ARM Macs (M1/M2/M3/M4) will use emulation (Rosetta) which may be slower.

### Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

### Build Commands

```bash
# From this directory (dev-tools/rulebook/)
./build.sh

# OR use docker compose directly
docker compose up --abort-on-container-exit
```

**Output:** `GPSA_Rulebook.pdf` in this directory (ignored by git)

### Troubleshooting Local Builds

**ARM Mac Performance:**
- Local builds may take 2-5 minutes due to x86_64 emulation
- GitHub Actions builds are faster (run natively on x86_64 runners)

**Permission Errors:**
- PDF is created as root inside container
- File may require `sudo` to delete: `sudo rm GPSA_Rulebook.pdf`

## Editing the Rulebook

### Front Matter Configuration

The YAML front matter at the top of `rulebook.md` controls the PDF appearance:

```yaml
---
title: "GPSA Rulebook"
subtitle: "Official Rules"
author: "GPSA Rules Committee"
date: "November 2025"
titlepage: true
titlepage-color: "003366"          # Navy background
titlepage-text-color: "FFFFFF"     # White text
titlepage-rule-color: "FFCC00"     # Gold accent line
logo: "assets/logo.png"
book: true
toc-own-page: true
---
```

### Markdown Formatting

- **Headings:** Use `#` for chapters, `##` for sections, `###` for subsections
- **Tables:** Use standard Markdown tables (converted to LaTeX)
- **Lists:** Numbered lists use `1.`, bulleted lists use `-` or `*`
- **Anchors:** Use `{#anchor-name}` after headings for cross-references

### Common Edits

**Update Date:**
```yaml
date: "December 2025"
```

**Change Title:**
```yaml
title: "GPSA Rulebook 2026"
```

**Add New Section:**
```markdown
## NEW SECTION TITLE {#new-section}

Content here...
```

## PDF Features

The generated PDF includes:

- ✅ Professional titlepage with GPSA logo and navy/gold branding
- ✅ Automatically generated table of contents
- ✅ Numbered sections and subsections
- ✅ Page numbers and headers
- ✅ Two-sided layout (book format)
- ✅ Code listings support (if needed)
- ✅ Proper LaTeX typography and spacing

## Template Information

**Eisvogel LaTeX Template:**
- Repository: [Wandmalfarbe/pandoc-latex-template](https://github.com/Wandmalfarbe/pandoc-latex-template)
- Version: Latest (downloaded fresh on each build)
- License: BSD 3-Clause

**Pandoc:**
- Docker Image: `pandoc/latex:latest`
- Engine: XeLaTeX (better Unicode support than pdflatex)

## Workflow File Location

`.github/workflows/build-pdf.yml`
