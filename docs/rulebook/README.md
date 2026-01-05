# GPSA Rulebook - Quarto Build System

This directory contains the source files and build system for the GPSA Rulebook, which is published in both **PDF** and **HTML** formats using [Quarto](https://quarto.org).

## Directory Structure

```
rulebook/
├── _quarto.yml             # Quarto configuration (main settings)
├── _metadata.yml           # Document metadata (DRAFT STATUS HERE!)
├── _custom.scss            # GPSA brand styling (navy #002366, red #d9242b)
├── docs/                   # Modular markdown source files (edit these!)
│   ├── index.md           # Web home page (edit in root, not here)
│   ├── definitions.md
│   ├── eligibility-and-rosters.md
│   ├── officials.md
│   ├── order-of-events.md
│   ├── conduct-of-meets.md
│   ├── scoring.md
│   ├── awards.md
│   └── facilities.md
├── index.md                # Homepage (at root level for Quarto)
└── build-quarto.sh         # Build script for both PDF and HTML

# Output directories (auto-generated):
../../docs/rulebook/         # HTML output (GitHub Pages)
../../docs/rulebook/GPSA-Rulebook.pdf  # PDF output
```

## 🚨 Draft Mode

**IMPORTANT:** The draft status is controlled by `_metadata.yml`:

```yaml
gpsa_draft: true   # Document is a DRAFT (shows banner, blocks merge to main)
gpsa_draft: false  # Document is FINAL (no banner, ready for production)
```

### How Draft Mode Works

**When `draft: true`:**

- ✅ HTML: Automatic draft banner at top of every page
- ✅ GitHub Actions: Prevents merging to `main` branch
- ✅ Clear visual indicator that content is not final

**When `draft: false`:**

- ✅ No draft banners
- ✅ Can merge to `main` branch
- ✅ Production-ready

### Changing Draft Status

**To mark as draft:**

```bash
# Edit _metadata.yml
draft: true
```

**To mark as final:**

```bash
# Edit _metadata.yml
draft: false
```

**That's it!** Quarto handles everything else automatically.

## Quick Start

### Prerequisites

**Install Quarto:**

**macOS (Homebrew):**

```bash
brew install quarto
```

**Alternative:**
Download from https://quarto.org/docs/get-started/

**Install TinyTeX (for PDF):**

```bash
quarto install tinytex
```

**Verify installation:**

```bash
quarto --version
```

### Building Both Formats

Run the build script from anywhere in the project:

```bash
./dev-docs/rulebook/build-quarto.sh
```

This single command will:

1. ✅ Generate PDF → `docs/rulebook/GPSA-Rulebook.pdf`
2. ✅ Build HTML website → `docs/rulebook/`

**Or build manually from the rulebook directory:**

```bash
cd dev-docs/rulebook
quarto render
```

### Building Individual Formats

**PDF only:**

```bash
cd dev-docs/rulebook
quarto render --to pdf
```

**HTML only:**

```bash
cd dev-docs/rulebook
quarto render --to html
```

## Development Workflow

### Editing Content

1. **Edit files in `docs/` directory** (NOT the auto-generated outputs)
2. Preview changes (see below)
3. Build final outputs when ready
4. Commit changes to Git

### Preview While Editing

**Live preview with auto-reload:**

```bash
cd dev-docs/rulebook
quarto preview
```

This opens a browser window that automatically updates when you save changes. Press `Ctrl+C` to stop.

### Making Changes

The workflow is simpler than the old MkDocs+Pandoc system:

**Old system:** Edit docs → Run assembly script → Build PDF → Build HTML (3 steps)
**Quarto system:** Edit docs → `quarto render` (1 step)

## Configuration

### Book Metadata

Edit `_quarto.yml` to change:

- Title, subtitle, author, date
- Chapter order
- Theme settings
- Headers and footers

### Draft Status

Edit `_metadata.yml`:

```yaml
draft: true   # or false
```

### Styling

**GPSA Brand Colors** (defined in `_custom.scss`):

- **Navy Blue:** `#002366` (primary color, headings)
- **Light Blue:** `#0033a0` (links)
- **Red:** `#d9242b` (secondary/accent)
- **Dark Red:** `#b81e24` (hover states)

**To customize styling:**

- Edit `_custom.scss` for global changes
- HTML themes: Set in `_quarto.yml` under `format.html.theme`
- PDF layout: Set in `_quarto.yml` under `format.pdf`

### Chapter Order

Chapters are listed in `_quarto.yml` under `book.chapters`:

```yaml
chapters:
  - index.md
  - docs/definitions.md
  - docs/eligibility-and-rosters.md
  # ... etc
```

To add a new chapter:

1. Create `.md` file in `docs/`
2. Add to `chapters` list in `_quarto.yml`
3. Run `quarto render`

## Output Details

### HTML Website

- **Location:** `../../docs/rulebook/` (served by GitHub Pages)
- **Theme:** Cosmo (light) / Darkly (dark) with GPSA customization
- **Features:**
   - Responsive navigation
   - Automatic table of contents
   - Full-text search
   - Dark mode toggle
   - Mobile-friendly
   - Sticky header with breadcrumbs
   - GPSA branded colors throughout

### PDF Document

- **Location:** `../../docs/rulebook/GPSA-Rulebook.pdf`
- **Format:** Letter size, report class, single-sided
- **Features:**
   - Custom GPSA-branded cover page with logo
   - Numbered sections (no "Chapter" labels)
   - Navy blue section headings with red underlines
   - Professional headers and footers
   - GPSA colors throughout
   - Optimized for digital viewing and printing

## GitHub Actions

A workflow (`.github/workflows/check-drafts.yml`) automatically:

- ✅ Checks all `_metadata.yml` files for `draft: true`
- ✅ Prevents merging to `main` if any drafts are found
- ✅ Displays helpful error messages

**To merge to main:**

1. Ensure `_metadata.yml` has `draft: false`
2. Build and verify outputs
3. Commit and push
4. GitHub Actions will verify no drafts exist
5. Merge PR

## Troubleshooting

**Quarto not found:**

- Install Quarto: `brew install quarto` (macOS)
- Or download: https://quarto.org/docs/get-started/

**PDF won't build:**

- Ensure TinyTeX is installed: `quarto install tinytex`
- Check for LaTeX errors in console output

**HTML output location wrong:**

- Check `output-dir` in `_quarto.yml`
- Should be: `../../docs/rulebook`

**Changes not appearing:**

- Clear cache: `quarto render --cache-refresh`
- Check you're editing files in `docs/`, not the output directories

**Styling issues:**

- Check `_custom.scss` for syntax errors
- Verify SCSS variables are defined before use

**Draft banner not appearing:**

- Check `_metadata.yml` has `draft: true`
- Rebuild with `quarto render`

**Can't merge to main:**

- Check `_metadata.yml` - must be `draft: false`
- GitHub Actions will block merge if draft is true

## GitHub Pages Integration

The HTML output is automatically generated to `docs/rulebook/`, which is served by GitHub Pages.

**Workflow:**

1. Edit markdown files in `docs/`
2. Run `quarto render`
3. Commit changes (including generated HTML in `docs/rulebook/`)
4. Push to GitHub
5. GitHub Pages auto-updates in 1-2 minutes

**Note:** You need to commit the generated HTML files in `docs/rulebook/` to Git.

## Advantages Over MkDocs+Pandoc

**Simpler:**

- ✅ One config file instead of multiple
- ✅ One build command instead of chained scripts
- ✅ No assembly step needed
- ✅ Native multi-file support

**More Powerful:**

- ✅ Better cross-references: `@sec-officials` syntax
- ✅ Native callouts: `:::{.callout-note}` for important info
- ✅ Built-in draft mode
- ✅ Code execution support (if needed for calculations)
- ✅ Publication-quality PDF by default
- ✅ Better table handling

**Easier Maintenance:**

- ✅ Single source of truth
- ✅ Industry-standard tool (used by RStudio, Observable, academic publishers)
- ✅ Active development and community support
- ✅ Native draft/production workflow

## Questions?

**Quarto Documentation:** https://quarto.org/docs/guide/
**Quarto Books:** https://quarto.org/docs/books/
**Draft Mode:** https://quarto.org/docs/websites/website-tools.html#draft-content
**GPSA Webmaster:** Contact through your GPSA Representative
