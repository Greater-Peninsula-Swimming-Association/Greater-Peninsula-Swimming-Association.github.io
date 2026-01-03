# Quarto Setup Complete - Ready for Installation

The Quarto configuration is now complete and ready to use. This document outlines what has been set up and the next steps.

## What's Been Configured

### ✅ Core Configuration Files

1. **`_quarto.yml`** - Main configuration file
   - Book project type
   - Chapter structure (all 8 sections + index)
   - PDF and HTML output settings
   - GPSA branding (logo, colors, metadata)
   - Output directory: `../../docs/rulebook/` (GitHub Pages compatible)

2. **`_custom.scss`** - GPSA brand styling
   - Navy blue (#002366) - primary
   - Red (#d9242b) - secondary/accent
   - Custom table styling
   - Callout/admonition styling

3. **`build-quarto.sh`** - Simplified build script
   - Checks for Quarto installation
   - Runs `quarto render` for both PDF + HTML
   - Provides helpful error messages

4. **`README.md`** - Comprehensive documentation
   - Installation instructions
   - Build commands
   - Development workflow
   - Troubleshooting guide
   - Migration notes from MkDocs

5. **`.gitignore`** - Quarto-specific ignores
   - Ignores `.quarto/` cache directory
   - Ignores `_freeze/` directory
   - Keeps output files for GitHub Pages

### ✅ Markdown Files Updated

- **`docs/order-of-events.md`** - Removed LaTeX wrappers around tables
  - Quarto handles tables natively (no need for `\begin{minipage}` wrappers)
  - Clean markdown tables work better

### ✅ File Structure

```
dev-docs/rulebook/
├── _quarto.yml          ← Quarto config (NEW)
├── _custom.scss         ← GPSA styling (NEW)
├── build-quarto.sh      ← Build script (NEW)
├── .gitignore           ← Quarto ignores (NEW)
├── README.md            ← Updated documentation
├── QUARTO-SETUP.md      ← This file (NEW)
└── docs/                ← Source markdown (updated)
    ├── index.md
    ├── definitions.md
    ├── eligibility-and-rosters.md
    ├── officials.md
    ├── order-of-events.md  ← Updated (removed LaTeX)
    ├── conduct-of-meets.md
    ├── scoring.md
    ├── awards.md
    └── facilities.md

OLD FILES (can be removed after successful test):
├── mkdocs.yml           ← Replaced by _quarto.yml
├── assemble-rulebook.sh ← Not needed (Quarto handles this)
├── build-all.sh         ← Replaced by build-quarto.sh
├── Dockerfile           ← Not needed
├── docker-compose.yml   ← Not needed
├── pandoc-filter.lua    ← Not needed
└── rulebook.md          ← Not needed (Quarto assembles internally)
```

## Next Steps

### 1. Install Quarto

**macOS (Homebrew):**
```bash
brew install quarto
```

**Or download installer:**
https://quarto.org/docs/get-started/

**Verify installation:**
```bash
quarto --version
# Should show: 1.8.x or higher
```

### 2. Install TinyTeX (for PDF generation)

Quarto will prompt you to install TinyTeX when you first try to generate a PDF. You can install it proactively:

```bash
quarto install tinytex
```

### 3. Test the Build

**From project root:**
```bash
./dev-docs/rulebook/build-quarto.sh
```

**Or from rulebook directory:**
```bash
cd dev-docs/rulebook
quarto render
```

**Expected outputs:**
- `dev-docs/rulebook.pdf` - PDF version
- `docs/rulebook/` - HTML website

### 4. Preview Locally

**Start live preview server:**
```bash
cd dev-docs/rulebook
quarto preview
```

This will:
- Open browser to `http://localhost:XXXX`
- Auto-reload when you save changes
- Let you test before committing

### 5. Compare Outputs

**Check the HTML:**
- Navigate to `docs/rulebook/index.html` in browser
- Compare styling to old MkDocs version
- Verify all sections are present
- Test navigation and search
- Check dark mode toggle

**Check the PDF:**
- Open `dev-docs/rulebook.pdf`
- Compare to old `rulebook.pdf`
- Verify formatting, TOC, page numbers
- Check GPSA logo on cover

### 6. Commit Changes

If everything looks good:

```bash
git add .
git commit -m "Transition to Quarto build system"
git push origin rulebook-development
```

**Note:** Quarto outputs (`docs/rulebook/` HTML and PDF) should be committed to git.

### 7. Clean Up Old Files (Optional)

After confirming Quarto works:

```bash
# Remove old MkDocs/Pandoc files
rm dev-docs/rulebook/mkdocs.yml
rm dev-docs/rulebook/assemble-rulebook.sh
rm dev-docs/rulebook/build-all.sh
rm dev-docs/rulebook/Dockerfile
rm dev-docs/rulebook/docker-compose.yml
rm dev-docs/rulebook/pandoc-filter.lua
rm dev-docs/rulebook/rulebook.md
rm dev-docs/rulebook/.dockerignore

# Also update dev-docs/build.sh to remove rulebook (if no longer needed)
```

## Troubleshooting

### Quarto Installation Issues

**macOS sudo password required:**
- The Homebrew cask installation requires admin password
- Alternative: Download the `.pkg` installer from quarto.org

**Command not found after install:**
```bash
# Restart terminal or reload shell
exec $SHELL

# Or add to PATH manually
export PATH="/Applications/quarto/bin:$PATH"
```

### Build Issues

**LaTeX/TinyTeX errors:**
```bash
# Install/reinstall TinyTeX
quarto install tinytex

# Or use system LaTeX
brew install --cask mactex
```

**Output directory errors:**
- Check `output-dir` in `_quarto.yml`
- Ensure parent directories exist: `mkdir -p ../../docs/rulebook`

**SCSS compilation errors:**
- Check `_custom.scss` for syntax errors
- Variables must be defined before use
- Ensure proper nesting

### Styling Differences

**If HTML looks different from MkDocs:**
- This is expected - different theme system
- Adjust in `_custom.scss` to match branding
- Colors and key styling preserved

**If PDF formatting is off:**
- Adjust settings in `_quarto.yml` under `format.pdf`
- Can add custom LaTeX header if needed
- Margins, fonts, spacing all configurable

## Configuration Reference

### Quick Config Changes

**Change theme:**
```yaml
# In _quarto.yml
format:
  html:
    theme:
      light: [flatly, _custom.scss]  # Try: cosmo, flatly, litera, minty
      dark: [darkly, _custom.scss]   # Try: darkly, superhero, slate
```

**Change PDF margins:**
```yaml
# In _quarto.yml
format:
  pdf:
    geometry:
      - margin=1.5in
      - top=1in
      - bottom=1in
```

**Add chapter:**
```yaml
# In _quarto.yml
book:
  chapters:
    - docs/new-section.md  # Add to list
```

## Questions?

- **Quarto Docs:** https://quarto.org/docs/guide/
- **Quarto Books:** https://quarto.org/docs/books/
- **This README:** `dev-docs/rulebook/README.md`

## Summary

✅ **Configuration complete** - All files ready
⏳ **Waiting for:** Quarto installation
🎯 **Next action:** Install Quarto and run `quarto render`
📝 **Result:** PDF + HTML generated in one command
