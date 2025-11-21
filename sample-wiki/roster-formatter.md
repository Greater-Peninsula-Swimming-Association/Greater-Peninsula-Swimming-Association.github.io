---
layout: sample-wiki
title: Roster Formatter
category: Tools
toc: true
last_updated: November 2025
---

The **GPSA Roster Formatter** is a comprehensive web-based tool that processes SwimTopia CSV roster exports and generates beautifully formatted HTML for team rosters, contact lists, and officials lists suitable for publishing on SwimTopia CMS pages.

## Quick Start

1. Visit [Roster Formatter Tool](/tools/roster.html)
2. Upload your SwimTopia roster CSV file
3. Add team contacts and officials information
4. Review the formatted preview
5. Copy the HTML output to your clipboard
6. Paste into your SwimTopia CMS page

## What It Does

The Roster Formatter provides three main functions:

1. **Roster Generation** - Formats swimmer lists by age group
2. **Contact Management** - Creates formatted contact information tables
3. **Officials Directory** - Generates officials lists with certifications

All outputs are HTML-only (no embedded CSS) designed to work seamlessly with external stylesheets hosted on SwimTopia CMS.

## Features Overview

### 2025 Enhanced Features

The tool includes modern enhancements for security, usability, and data persistence:

- **XSS Protection** - All user input sanitized to prevent security vulnerabilities
- **Data Persistence** - Contacts and officials auto-save to browser localStorage
- **Real-time Validation** - Email and phone number validation with visual feedback
- **Toast Notifications** - Professional, non-blocking notifications replace popup alerts
- **Accessibility** - Keyboard navigation, modal focus traps, and screen reader support
- **Duplicate Detection** - Warns about duplicate contact names

## Tab 1: Roster Input

### Getting the CSV File

#### Exporting from SwimTopia

1. Log in to your SwimTopia team admin account
2. Navigate to **Roster** > **Team Roster**
3. Click **Export** and select **CSV format**
4. Save the file (e.g., `glendale-2025-roster.csv`)

#### Required CSV Columns

The CSV must contain these columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| `AgeGroup` | Age group (may include gender prefix) | `9-10`, `Boys 11-12` |
| `AthleteCompetitionCategory` | Gender code | `M` or `F` |
| `AthleteDisplayName` | Swimmer's full name | `Smith, John` |
| `AthleteAge` | Numeric age | `10` |

**Note:** Gender prefixes in age groups (e.g., "Boys 9-10") are automatically stripped by the tool.

### Processing the Roster

1. Click **Choose File** or drag-and-drop your CSV
2. Wait for "CSV file loaded successfully!" toast notification (green)
3. Navigate to **Formatted Roster** tab to see preview
4. Click **Export Roster HTML** when ready

### Age Group Handling

The tool processes age groups as follows:

- **Strips Gender Prefixes**: "Boys 9-10" → "9-10"
- **Sorts Age Groups**: 8 & Under, 9-10, 11-12, 13-14, 15-18, Open
- **Sorts Swimmers**: Alphabetically by name within each age group

## Tab 2: Contacts

### Adding Contact Information

Contacts are team representatives, coordinators, or key personnel. To add a contact:

1. Click **Add Contact** button
2. Enter contact details in the form fields:
   - **Name** (required)
   - **Role/Title** (e.g., "Team Representative", "Head Coach")
   - **Email** (validated in real-time)
   - **Phone** (auto-formatted to (XXX) XXX-XXXX)

### Email Validation

- Email fields show **red border** if invalid (missing @, no domain, etc.)
- Email fields show **green border** when valid
- Export is blocked if any invalid emails are detected

### Phone Formatting

Phone numbers are automatically formatted as `(XXX) XXX-XXXX`:
- Input: `7575551234`
- Output: `(757) 555-1234`

### Duplicate Detection

The tool warns you (orange toast) if you enter a contact name that already exists, but doesn't prevent saving.

### Data Persistence

- Contacts **auto-save to browser localStorage** on every change
- Data persists across browser sessions and restarts
- Use **Clear Contacts** button to reset (removes both UI and localStorage)

### Removing Contacts

Click the **red trash icon** (🗑️) next to any contact to remove it. The removal is immediate and updates localStorage.

## Tab 3: Officials

### Adding Officials Information

Officials are certified volunteers who work meets. To add an official:

1. Click **Add Official** button
2. Enter official details:
   - **Name** (required)
   - **Certification Level** (e.g., "Stroke & Turn", "Starter", "Referee")
   - **Email** (validated in real-time)
   - **Phone** (auto-formatted)

### Certification Levels

Common GPSA official certification levels:
- **Stroke & Turn Judge**
- **Starter**
- **Referee**
- **Administrative Official**
- **Chief Judge**

### Data Persistence

Like contacts, officials also:
- Auto-save to localStorage
- Persist across browser sessions
- Can be cleared with **Clear Officials** button

## Tab 4: Formatted Roster

### Preview and Export

The **Formatted Roster** tab shows a live preview of all three outputs:

1. **Team Roster** - Swimmers organized by age group
2. **Contact Information** - Table of contacts with roles and info
3. **Officials** - List of officials with certifications

### Export Options

Three export buttons are available:

1. **Export Roster HTML** - Copies roster HTML to clipboard
2. **Export Contacts HTML** - Copies contacts table HTML to clipboard
3. **Export Officials HTML** - Copies officials list HTML to clipboard

Each export:
- Copies HTML to your clipboard via modern Clipboard API
- Shows green success toast notification
- Can be pasted directly into SwimTopia HTML editor

### Export Format

Exports are **HTML-only** (no embedded CSS) and reference external stylesheets:

- **Roster**: `/css/gpsa-roster.css`
- **Contacts**: `/css/gpsa-roster-contact.css`
- **Officials**: `/css/gpsa-roster-officials.css`

These stylesheets are hosted on `publicity.gpsaswimming.org` and automatically apply when the HTML is published on SwimTopia.

## Using the Formatted HTML

### Pasting into SwimTopia CMS

1. Click the appropriate **Export** button in the tool
2. Log in to your SwimTopia team admin account
3. Navigate to the page you want to update (e.g., "Team Roster" page)
4. Click **Edit** on the page
5. Switch to **HTML/Source** mode (usually a `<>` button)
6. **Select all existing content** and delete (or paste over it)
7. **Paste** the HTML from your clipboard (`Ctrl+V` or `Cmd+V`)
8. Switch back to visual mode to preview
9. Click **Save** and **Publish**

### Updating Existing Rosters

When the season changes or roster updates are needed:

1. Export fresh CSV from SwimTopia
2. Upload to Roster Formatter tool (replaces old data)
3. Contacts and officials **persist automatically** from localStorage
4. Verify contact info is still current
5. Export and publish updated HTML

## Troubleshooting

### "Missing required columns" Error

**Cause:** CSV doesn't have required `AgeGroup`, `AthleteCompetitionCategory`, `AthleteDisplayName`, or `AthleteAge` columns.

**Solution:**
- Re-export from SwimTopia using **Team Roster** export
- Verify you're exporting the roster, not meet results or entries

### "Please fix invalid email addresses before exporting" Error

**Cause:** One or more email fields have invalid format.

**Solution:**
- Look for email fields with **red borders**
- Correct the email format (must include `@` and domain)
- Email validation updates on blur (when you click away from field)

### Contacts/Officials Disappeared

**Cause:** Browser localStorage was cleared or you're using a different browser/device.

**Solution:**
- Re-enter contacts and officials (they'll auto-save)
- Consider keeping a backup document with contact info
- Use same browser/device for consistency

### Phone Numbers Not Formatting

**Cause:** Phone formatting only applies to 10-digit US phone numbers.

**Solution:**
- Enter exactly 10 digits (no spaces, dashes, or parentheses)
- Formatting applies when you click away from field (on blur)
- For non-US numbers, enter with desired formatting

### Export Button Does Nothing

**Cause:** Browser may not support modern Clipboard API or permission denied.

**Solution:**
- Use a modern browser (Chrome, Firefox, Safari, Edge)
- Ensure you've granted clipboard permissions if prompted
- Try refreshing the page and re-uploading data

### Roster Preview Looks Unstyled

**Cause:** External CSS files may not be loading in preview.

**Solution:**
- Preview is for content verification only
- Final styling will apply when published on SwimTopia
- Trust that the CSS is hosted and will load on production site

## Data Persistence Details

### What Gets Saved

The tool saves to browser localStorage:
- **Contacts** - Stored as `gpsa_roster_contacts`
- **Officials** - Stored as `gpsa_roster_officials`
- **Roster Data** - NOT saved (must re-upload CSV each time)

### When Data is Saved

- Auto-saves on every input field change (on blur)
- Saves when adding/removing contacts or officials
- No manual "Save" button needed

### Clearing Saved Data

1. Use **Clear Contacts** button to remove all contacts
2. Use **Clear Officials** button to remove all officials
3. Or use **Reset All** to clear everything at once

**Note:** Clearing also removes data from localStorage.

### localStorage Limits

- Browser localStorage limit: ~5-10 MB per domain
- This is more than sufficient for typical team contacts/officials
- If limit reached, browser will show an error (extremely rare)

## Best Practices

### For Team Reps

1. **Export CSV at season start** - Get complete roster from SwimTopia
2. **Enter contacts/officials once** - They persist automatically
3. **Update mid-season** - Re-upload CSV if swimmers join/leave
4. **Verify emails before export** - Check for red borders
5. **Test in preview** - Review formatted output before publishing
6. **Keep backup** - Document contacts/officials outside the tool

### For Webmasters

1. **Use consistent formatting** - Same tool for all teams
2. **Update external CSS** - Ensure stylesheets on publicity.gpsaswimming.org are current
3. **Test on mobile** - Verify responsive display on phones/tablets
4. **Archive old rosters** - Save HTML for historical reference

### For Data Entry

1. **Copy/paste carefully** - When entering multiple contacts
2. **Use Tab key** - Navigate between fields efficiently
3. **Verify phone format** - Ensure 10 digits for auto-formatting
4. **Check for duplicates** - Watch for orange warning toasts
5. **Save as you go** - Data auto-saves, but verify before closing

## Security Features

### XSS Protection

All user input is sanitized using the `escapeHtml()` function to prevent cross-site scripting (XSS) attacks. This means:

- Special characters are escaped in output
- HTML tags in input are rendered as text, not executed
- Scripts cannot be injected via contact names or emails

### Safe HTML Output

The generated HTML is safe to paste into SwimTopia CMS without security concerns:
- No inline JavaScript
- No event handlers
- Only semantic HTML structure with CSS classes

## Technical Details

### Libraries Used

- **PapaParse v5.4.1** - CSV parsing library
- **Tailwind CSS** - UI framework (via CDN)
- **GPSA Common Styles** - Shared GPSA branding CSS

### Browser Compatibility

Works in all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Note:** Internet Explorer is not supported.

### Browser Storage

- Uses **localStorage API** (not cookies or sessionStorage)
- Data stored locally on user's device only
- Not transmitted to any server
- Persists indefinitely until cleared

### Accessibility Features

- **Keyboard navigation** - Full Tab/Shift+Tab support
- **ARIA labels** - Dynamic aria-labels on remove buttons
- **Focus traps** - Modals trap focus for keyboard users
- **Esc to close** - Press Escape to close modals
- **Click outside** - Click outside modal to close

## Related Tools

- [Meet Schedule Generator](/wiki/meet-schedule-generator) - Format division schedules
- [Publicity Processor](/wiki/publicity-processor) - Generate meet result reports
- [SwimTopia Guide](/wiki/swimtopia-guide) - Complete SwimTopia documentation

## Support

For issues or questions:

- **Tool Issues** - Contact GPSA webmaster
- **SwimTopia Export Issues** - Contact your SwimTopia administrator
- **Feature Requests** - Submit via your team representative

---

**Quick Links:**
- [Access the Tool](/tools/roster.html)
- [All GPSA Tools](/tools/)
- [Team Rep Duties](/wiki/team-rep-duties)
- [SwimTopia Guide](/wiki/swimtopia-guide)
