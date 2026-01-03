# GPSA Rulebook - Quarto Build System

This directory contains the source files and build system for the GPSA Rulebook, which is published in both **PDF** and **HTML** formats using [Quarto](https://quarto.org).

## Directory Structure

```
rulebook/
├── _quarto.yml             # Quarto configuration (replaces mkdocs.yml + assembly scripts)
├── _custom.scss            # GPSA brand styling (navy #002366, red #d9242b)
├── docs/                   # Modular markdown source files (edit these!)
│   ├── index.md           # Web home page
│   ├── definitions.md
│   ├── eligibility-and-rosters.md
│   ├── officials.md
│   ├── order-of-events.md
│   ├── conduct-of-meets.md
│   ├── scoring.md
│   ├── awards.md
│   └── facilities.md
└── build-quarto.sh         # Build script for both PDF and HTML

# Output directories (auto-generated):
../../docs/rulebook/         # HTML output (GitHub Pages)
../rulebook.pdf             # PDF output
```

## Quick Start

### Prerequisites

**Install Quarto:**

**macOS (Homebrew):**
```bash
brew install quarto
```

**Alternative:**
Download from https://quarto.org/docs/get-started/

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
1. ✅ Generate PDF → `dev-docs/rulebook.pdf`
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
- Cover image
- Chapter order
- Theme settings

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
  - index: docs/index.md
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

### PDF Document
- **Location:** `../rulebook.pdf`
- **Format:** Letter size, book class, two-sided
- **Features:**
  - Numbered sections
  - Table of contents
  - Professional typesetting
  - GPSA logo on cover

## Advantages Over MkDocs+Pandoc

**Simpler:**
- ✅ One config file instead of multiple
- ✅ One build command instead of chained scripts
- ✅ No assembly step needed
- ✅ Native multi-file support

**More Powerful:**
- ✅ Better cross-references: `@sec-officials` syntax
- ✅ Native callouts: `:::{.callout-note}` for important info
- ✅ Code execution support (if needed for calculations)
- ✅ Publication-quality PDF by default
- ✅ Better table handling

**Easier Maintenance:**
- ✅ Single source of truth
- ✅ Industry-standard tool (used by RStudio, Observable, academic publishers)
- ✅ Active development and community support

## Troubleshooting

**Quarto not found:**
- Install Quarto: `brew install quarto` (macOS)
- Or download: https://quarto.org/docs/get-started/

**PDF won't build:**
- Ensure LaTeX is installed (Quarto will prompt to install TinyTeX if needed)
- Run: `quarto install tinytex`

**HTML output location wrong:**
- Check `output-dir` in `_quarto.yml`
- Should be: `../../docs/rulebook`

**Changes not appearing:**
- Clear cache: `quarto render --cache-refresh`
- Check you're editing files in `docs/`, not the output directories

**Styling issues:**
- Check `_custom.scss` for syntax errors
- Verify SCSS variables are defined before use

## GitHub Pages Integration

The HTML output is automatically generated to `docs/rulebook/`, which is served by GitHub Pages.

**Workflow:**
1. Edit markdown files in `docs/`
2. Run `quarto render`
3. Commit changes (including generated HTML in `docs/rulebook/`)
4. Push to GitHub
5. GitHub Pages auto-updates in 1-2 minutes

**Note:** Unlike the old MkDocs system, you need to commit the generated HTML files in `docs/rulebook/` to Git.

## Advanced Features

### Cross-References

Reference sections by ID:
```markdown
See @sec-officials for details.
```

Add IDs to sections:
```markdown
## Officials {#sec-officials}
```

### Callouts

Add styled callout boxes:
```markdown
:::{.callout-note}
This is an important note.
:::

:::{.callout-important}
Critical information here.
:::
```

### Custom Divs

Add custom HTML classes:
```markdown
:::{.custom-class}
Content here
:::
```

## Migration Notes

**From MkDocs+Pandoc system:**
- ✅ Markdown files unchanged (except removed LaTeX wrappers)
- ✅ GPSA branding preserved
- ✅ Same output locations for GitHub Pages
- ⚠️ Navigation structure slightly different (book vs material theme)
- ⚠️ Need to commit generated HTML files

**Old files (can be removed after successful transition):**
- `mkdocs.yml` → replaced by `_quarto.yml`
- `assemble-rulebook.sh` → not needed (Quarto handles assembly)
- `build-all.sh` → replaced by `build-quarto.sh`
- `Dockerfile` (MkDocs) → not needed
- `docker-compose.yml` → not needed
- `rulebook.md` (assembled file) → not needed
- `pandoc-filter.lua` → not needed

## Questions?

**Quarto Documentation:** https://quarto.org/docs/guide/
**Quarto Books:** https://quarto.org/docs/books/
**GPSA Webmaster:** Contact through your GPSA Representative
