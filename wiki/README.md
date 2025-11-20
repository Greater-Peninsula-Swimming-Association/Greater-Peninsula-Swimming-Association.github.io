# GPSA Wiki - Usage Guide

This document explains how to create, edit, and manage GPSA wiki pages using Jekyll and Markdown.

## Overview

The GPSA Wiki uses **Jekyll** (a static site generator built into GitHub Pages) to convert Markdown files into beautifully formatted HTML pages with GPSA branding.

**Benefits:**
- ✅ Write content in simple Markdown syntax
- ✅ Automatic GPSA styling applied to all pages
- ✅ Navigation sidebar auto-highlights current page
- ✅ Table of contents auto-generated from headings
- ✅ Version controlled with Git
- ✅ No database or server required

## Quick Start

### Creating a New Wiki Page

1. Create a new `.md` file in the `/wiki/` directory
2. Add front matter at the top
3. Write your content in Markdown
4. Commit and push to GitHub
5. Page goes live automatically!

**Example:**

```markdown
---
layout: wiki
title: My New Page
category: Getting Started
toc: true
last_updated: November 2025
---

# My New Page

Your content here...
```

### Front Matter Explained

Front matter is the YAML block at the top of each file between `---` markers:

```yaml
---
layout: wiki              # Always use "wiki" for wiki pages
title: Page Title         # Shown at top of page and in browser tab
category: Category Name   # Used in breadcrumbs (optional)
toc: true                # Auto-generate table of contents (optional)
last_updated: Nov 2025   # Display last update date (optional)
---
```

**Required fields:**
- `layout: wiki` - Uses the wiki page template
- `title: Your Title` - Page title

**Optional fields:**
- `category` - Category name for breadcrumbs
- `toc: true` - Auto-generates table of contents from H2/H3 headings
- `last_updated` - Shows "Last updated" footer

## Markdown Syntax

### Headings

```markdown
# Heading 1 (Page title - use once)
## Heading 2 (Major sections)
### Heading 3 (Subsections)
#### Heading 4 (Minor subsections)
```

**Result:**
- H1 gets blue underline (GPSA red accent)
- H2 gets gray underline
- H3 and H4 are styled but no underline

### Text Formatting

```markdown
**Bold text**
*Italic text*
***Bold and italic***
`inline code`
~~Strikethrough~~
```

### Links

```markdown
[Link text](/wiki/other-page)           # Link to another wiki page
[External link](https://example.com)    # External link
[Home](/)                                # Link to main site
```

### Lists

**Unordered:**
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3
```

**Ordered:**
```markdown
1. First item
2. Second item
3. Third item
```

**Checklist:**
```markdown
- [x] Completed task
- [ ] Pending task
- [ ] Another pending task
```

### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

**Result:**
- Headers get GPSA navy background with white text
- Alternating row colors (white/light gray)
- Bordered cells

### Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.
```

**Result:** Left border in GPSA red, gray italic text

### Code Blocks

**Inline code:**
```markdown
Use `code` for inline code.
```

**Code blocks:**
````markdown
```python
def hello_world():
    print("Hello, GPSA!")
```
````

**Result:**
- Dark background
- Syntax highlighting
- Horizontal scroll for long lines

### Images

```markdown
![Alt text](/path/to/image.jpg)
![GPSA Logo](https://publicity.gpsaswimming.org/assets/gpsa_logo.png)
```

### Horizontal Rules

```markdown
---
```

Creates a horizontal line separator.

## Advanced Features

### Table of Contents

Enable auto-generated TOC by setting `toc: true` in front matter:

```yaml
---
layout: wiki
title: My Page
toc: true
---
```

The TOC will:
- Include all H2 and H3 headings
- Auto-generate anchor links
- Display in a styled box below the title
- Hide if no headings are found

### Custom Heading IDs

Link directly to a section:

```markdown
## My Section {#custom-id}

Later, link to it: [Jump to My Section](#custom-id)
```

### Emoji Support

GitHub-flavored Markdown supports emoji:

```markdown
:swimmer: :trophy: :medal: :star:
```

### Task Lists

```markdown
- [x] Set up wiki structure
- [x] Create sample pages
- [ ] Add more content
```

## Navigation Management

### Adding a Page to Sidebar

Edit `/_includes/wiki-nav.html`:

```html
<div class="wiki-nav-category">Category Name</div>
<a href="/wiki/your-new-page" class="wiki-nav-item {% if page.url contains '/wiki/your-new-page' %}active{% endif %}">
    Your Page Title
</a>
```

**Tips:**
- Group related pages under category headers
- Use descriptive link text
- Keep URLs lowercase with hyphens
- Active page is highlighted automatically

### Navigation Categories

Current categories:
- Getting Started
- Rules & Regulations
- For Officials
- For Team Representatives
- Resources
- Historical

Add new categories as needed.

## File Naming

**Best practices:**
- Use lowercase
- Use hyphens (not underscores or spaces)
- Be descriptive but concise
- Match the page title

**Examples:**
- ✅ `league-rules.md`
- ✅ `how-to-join.md`
- ✅ `officiating-guide.md`
- ❌ `League Rules.md` (spaces)
- ❌ `rules_and_regs.md` (underscores)
- ❌ `page1.md` (not descriptive)

## Testing Locally

To preview changes before pushing to GitHub:

### Install Jekyll (one-time setup)

```bash
# macOS
gem install bundler jekyll

# Create Gemfile in repo root
echo "source 'https://rubygems.org'" > Gemfile
echo "gem 'github-pages', group: :jekyll_plugins" >> Gemfile

# Install dependencies
bundle install
```

### Run Local Server

```bash
# From repo root
bundle exec jekyll serve

# Open browser to:
http://localhost:4000/wiki/
```

Changes auto-reload as you edit files!

### Troubleshooting Local Testing

**Error: "Could not find gem"**
```bash
bundle install
```

**Port 4000 already in use:**
```bash
bundle exec jekyll serve --port 4001
```

## Publishing Workflow

### Method 1: Git Command Line

```bash
# 1. Create/edit your wiki page
# 2. Stage changes
git add wiki/your-new-page.md
git add _includes/wiki-nav.html  # if you updated navigation

# 3. Commit
git commit -m "Add wiki page: Your Page Title"

# 4. Push to GitHub
git push origin main

# 5. Wait 1-2 minutes for GitHub Pages to rebuild
# 6. Visit https://www.gpsaswimming.org/wiki/your-new-page
```

### Method 2: GitHub Web Interface

1. Navigate to `/wiki/` folder on GitHub
2. Click "Add file" → "Create new file"
3. Name your file (e.g., `my-page.md`)
4. Add front matter and content
5. Scroll down and click "Commit new file"
6. Page goes live in 1-2 minutes

## Content Guidelines

### Writing Style

- **Be clear and concise** - Use simple language
- **Use active voice** - "Swimmers must touch the wall" not "The wall must be touched"
- **Break up text** - Use headings, lists, and tables
- **Link to related pages** - Help readers navigate
- **Include examples** - Show, don't just tell

### Accessibility

- Use descriptive link text (not "click here")
- Provide alt text for images
- Use proper heading hierarchy (don't skip levels)
- Ensure sufficient color contrast

### GPSA Voice

- Professional but friendly
- Focus on helping swimmers and families
- Emphasize fun and sportsmanship
- Be inclusive and welcoming

## Common Tasks

### Updating an Existing Page

1. Edit the `.md` file
2. Update `last_updated` in front matter
3. Commit and push

### Moving a Page

1. Rename the file (keep `.md` extension)
2. Update links in other pages that reference it
3. Update navigation in `_includes/wiki-nav.html`
4. Commit and push all changes

### Deleting a Page

1. Delete the `.md` file
2. Remove from navigation in `_includes/wiki-nav.html`
3. Remove any links to it from other pages
4. Commit and push

### Creating a Category

1. Add category header in `_includes/wiki-nav.html`:
   ```html
   <div class="wiki-nav-category">New Category</div>
   ```
2. Add pages under that category
3. Commit and push

## File Structure

```
/
├── _config.yml              # Jekyll configuration
├── _layouts/
│   └── wiki.html            # Wiki page template
├── _includes/
│   └── wiki-nav.html        # Sidebar navigation
└── wiki/
    ├── README.md            # This file
    ├── index.md             # Wiki home page
    ├── about.md             # Sample page
    ├── faq.md               # Sample page
    └── meet-procedures.md   # Sample page
```

## Markdown Editors

**Recommended tools:**
- [VS Code](https://code.visualstudio.com/) with Markdown Preview
- [Typora](https://typora.io/) - WYSIWYG Markdown editor
- [StackEdit](https://stackedit.io/) - Online Markdown editor
- [MacDown](https://macdown.uranusjr.com/) - macOS Markdown editor

## Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Liquid Template Language](https://shopify.github.io/liquid/)

## Need Help?

- Check existing wiki pages for examples
- Review this README
- Test locally before pushing
- Ask the GPSA webmaster

---

**Happy wiki editing!** 🏊‍♂️
