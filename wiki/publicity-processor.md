---
layout: wiki
title: Publicity Processor
category: Tools
toc: true
last_updated: November 2025
---

The **GPSA Meet Publicity Tool** (also called the Publicity Processor) is a powerful web-based tool that converts SDIF format swim meet results into beautifully formatted HTML reports with team scores, event winners, and complete meet details.

## Quick Start

1. Visit [Publicity Processor Tool](/tools/publicity.html)
2. Upload your SDIF results file (.sd3, .txt, or .zip)
3. Review the parsed results in the preview
4. (Optional) Mark forfeit or special circumstances
5. Click "Export as HTML"
6. Save the file as `YYYY-MM-DD_TEAM1_v_TEAM2.html`

## What It Does

The Publicity Processor transforms raw SDIF (Swimming Data Interchange Format) data into professional HTML reports suitable for:

- Publishing meet results on team websites
- Archiving in the GPSA results directory
- Sharing with parents and swimmers
- Building season archives with the `build_archive.py` tool

### Key Features

- **SDIF Format Support** - Parses .sd3 and .txt files
- **Zip File Support** - Extracts SDIF files from .zip archives (up to 256KB)
- **Auto-Generated Titles** - Creates meet titles from host team and date
- **Team Scores** - Calculates and displays final team scores
- **Event Winners** - Lists winners for each event with times
- **Forfeit Handling** - Override scores for forfeits or special circumstances
- **Standardized Export** - Exports as `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- **GPSA Branding** - Uses official GPSA colors (#002366 navy, #d9242b red)

## Supported File Formats

### SDIF Files (.sd3, .txt)

SDIF (Swimming Data Interchange Format) is the standard format for swim meet data. SwimTopia exports results in this format.

**Supported File Types:**
- `.sd3` - Standard SDIF extension
- `.txt` - Text files containing SDIF data

### Zip Archives (.zip)

The tool can extract and process SDIF files from zip archives:

- **Maximum file size:** 256KB
- **Auto-extraction:** Automatically finds .sd3 or .txt files inside
- **Multi-file handling:** Uses first SDIF file found if multiple files present
- **Status notifications:** Toast messages show extraction progress

**Why Zip Support?** Some meet software exports results as .zip files, and this feature eliminates the need to manually extract files before processing.

## Getting SDIF Files

### Exporting from SwimTopia

1. Log in to SwimTopia as a meet administrator
2. Navigate to **Meets** > **Meet Results**
3. Select the meet you want to export
4. Click **Export Results**
5. Choose **SDIF/SD3 Format** (not HY3 format)
6. Save the file (e.g., `meet_results.sd3`)

### From Meet Management Software

Most meet management software (Hy-Tek, SwimTopia, Meet Manager) can export to SDIF format. Look for:
- Export options or buttons
- "SDIF" or "SD3" format choices
- Avoid "HY3" format (not supported)

**Note:** The tool does NOT support HY3/Hy-Tek 3.0 format files. HY3 files use a different structure and are 65-70% larger than SDIF files. Since SwimTopia exports SDIF by default and both formats contain identical data, always export as SDIF/SD3.

## Understanding SDIF Format

SDIF files contain meet data in a structured text format. Key record types:

| Record Type | Description | Example Data |
|-------------|-------------|--------------|
| **B1** | Meet information | Meet name, date (MMDDYYYY format) |
| **B2** | Host team information | Team name, location |
| **C1** | Team record | Team code, full team name |
| **D0** | Individual result | Event #, swimmer name, time, place, points |
| **E0** | Relay result | Relay team, time, place, points |
| **F0** | Relay swimmers | Individual names of relay swimmers |

The tool's `parseSdif()` function processes these records to extract:
- Meet title and date
- Competing teams
- Event details (distance, stroke, age group, gender)
- Individual and relay results
- Scoring information

## Using the Tool

### Step 1: Upload Results File

1. Click the **upload area** or drag-and-drop your file
2. Supported formats: `.sd3`, `.txt`, `.zip`
3. Wait for "File loaded successfully!" notification (green toast)

**If uploading a zip file:**
- Tool extracts automatically
- Shows "Extracting SDIF file from zip archive..." toast (blue)
- If successful, shows "SDIF file extracted successfully!" (green)

### Step 2: Process Results

1. Click **Process Results** button
2. Tool parses SDIF data and displays preview
3. Preview shows:
   - Meet title and date
   - Final team scores
   - Event-by-event results with winners

### Step 3: Special Circumstances (Optional)

If the meet had special circumstances (forfeit, cancellation, weather override), see [Forfeit and Override Functionality](#forfeit-and-override-functionality) section below.

### Step 4: Export HTML

1. Click **Export as HTML** button
2. Browser prompts you to save file
3. **Use this naming convention:** `YYYY-MM-DD_TEAM1_v_TEAM2.html`
   - Example: `2025-06-16_GG_v_WW.html`
4. Save to your results directory (e.g., `results/2025/`)

**Naming Convention is Critical!** The archive builder (`build_archive.py`) relies on this exact format to:
- Auto-detect season year
- Parse team matchups
- Generate division standings
- Build meet schedules

## Forfeit and Override Functionality

### When to Use Overrides

Use the special circumstances feature when:
- A team forfeits the meet (cannot field enough swimmers)
- Meet is cancelled but winner needs to be recorded
- League rules require score override (weather, safety, etc.)
- Administrative decision changes outcome

### How to Apply Forfeit/Override

1. **Check the box:** "This meet has special circumstances"
2. **Process results first:** Click "Process Results" to populate team dropdown
3. **Select winning team:** Choose from the dropdown
4. **Enter reason:** Explain why (e.g., "Team forfeited due to weather")
5. **Review preview:** Override banner appears in yellow with winner and reason
6. **Export:** File works normally with `build_archive.py`

### Standard Forfeit Scoring

When override is active:
- **Winning team:** 1.0 points
- **Losing team:** 0.0 points
- Team Scores table shows 1.0 vs 0.0 (ensures correct win/loss tracking)

### Override Banner in Exported HTML

Exported HTML includes a prominent yellow warning banner:

```
⚠️ SPECIAL CIRCUMSTANCES
Winner: [Winning Team Name]
Reason: [Your explanation text]
```

This banner:
- Appears at the top of the exported HTML
- Uses inline styles for portability
- Is clearly visible to anyone viewing results
- Persists in season archives

### Archive Builder Compatibility

Forfeit exports are **fully compatible** with `build_archive.py`:
- No special processing required
- Team Scores table shows 1.0 vs 0.0
- Follows standard `YYYY-MM-DD_TEAM1_v_TEAM2.html` naming
- Win/loss records calculated correctly
- Override banner preserved in archives

### Example Forfeit Workflow

**Scenario:** Glendale vs Wendwood meet on June 16, 2025. Wendwood forfeits due to insufficient swimmers.

1. Upload the SDIF file (may show actual meet scores before forfeit)
2. Check "This meet has special circumstances"
3. Click "Process Results"
4. Select "Glendale Gators" from winning team dropdown
5. Enter reason: "Wendwood forfeited due to insufficient swimmers"
6. Review preview - see yellow banner and 1.0 vs 0.0 scores
7. Export as `2025-06-16_GG_v_WW.html`
8. File works normally with archive builder

## Auto-Generated Meet Titles

The tool automatically generates meet titles for dual meets:

**Format:** `[Host Team Name] vs [Visiting Team Name] - [Date]`

**Example:** `Glendale Gators vs Wendwood Waves - June 16, 2025`

### How Host Team is Determined

The tool identifies the host team from:
1. SDIF B2 record (host team information)
2. Team code starting with "VA" (prefix is stripped)

### Team Name Handling

Team codes starting with "VA" have the prefix removed:
- `VAGG` → `GG` (Glendale)
- `VAWW` → `WW` (Wendwood)

This ensures consistent team abbreviations across all GPSA tools.

## Output Format

### HTML Structure

The exported HTML includes:

1. **Header** - GPSA logo and meet title
2. **Team Scores** - Final scores in large, prominent display
3. **Override Banner** (if applicable) - Yellow warning box
4. **Event Results** - Organized by event number
   - Event description (gender, age group, distance, stroke)
   - Winner's name, team, time, and points
   - Runner-up (if applicable)
5. **Footer** - GPSA branding and generation timestamp

### Styling

- **Tailwind CSS** via CDN for responsive design
- **GPSA Brand Colors:**
  - Navy Blue: `#002366` (headers, primary elements)
  - Red: `#d9242b` (accents, secondary elements)
- **Fully Responsive:** Works on desktop, tablet, and mobile
- **Print-Friendly:** Header hidden when printing

### Self-Contained Files

Exported HTML files are self-contained:
- All styling embedded (no external CSS dependencies)
- Can be moved anywhere without breaking
- Safe to archive long-term
- Display correctly offline

## Event Results Display

### Individual Events

For each individual swimming event, the tool displays:
- **Event Number and Description:** "Event 3: Girls 11-12 50 Freestyle"
- **Winner:** Name, team abbreviation, time, points earned
- **Runner-up:** (if different from winner)

**Example Output:**
```
Event 5: Boys 9-10 50 Butterfly
Winner: Smith, John (GG) - 35.42 - 5 points
```

### Relay Events

Relay events display:
- Event description with relay designation
- Team that won
- Individual relay swimmer names (on separate lines)
- Time and points

**Example Output:**
```
Event 23: Girls 13-14 200 Freestyle Relay
Winner: Glendale Gators - 2:08.56 - 7 points
  • Johnson, Sarah
  • Williams, Emily
  • Davis, Ashley
  • Martinez, Nicole
```

### Age Group Formats

The tool handles various age group formats:
- "8 & Under"
- "9-10"
- "11-12"
- "13-14"
- "15-18"
- "Open"

All are parsed and displayed consistently.

## Troubleshooting

### "Error parsing SDIF file" Message

**Cause:** File may be corrupted, not in SDIF format, or wrong format (HY3).

**Solution:**
- Verify file is in SDIF/SD3 format (not HY3)
- Re-export from SwimTopia or meet software
- Try opening file in text editor to verify contents
- Check file size (should be < 1MB for typical dual meet)

### "Failed to extract SDIF file from zip" Error

**Cause:** Zip file doesn't contain .sd3 or .txt file, or file is too large.

**Solution:**
- Unzip manually and upload SDIF file directly
- Verify zip contains SDIF file (not just HY3 or other formats)
- Check file is under 256KB

### Team Names Not Displaying

**Cause:** SDIF file may not have C1 (team record) entries.

**Solution:**
- Check SDIF file has team information records
- Team codes will display as abbreviations if full names missing
- Re-export with full team information

### Meet Date Shows as "Unknown"

**Cause:** SDIF file missing B1 record with meet date.

**Solution:**
- Re-export from source with complete meet information
- Manually add date when saving file (use filename convention)

### Relay Swimmer Names Missing

**Cause:** SDIF file missing F0 records following E0 relay records.

**Solution:**
- Some software doesn't export relay swimmer names
- Tool will show team that won relay but not individual names
- This is a limitation of the source SDIF file, not the tool

### Export Button Does Nothing

**Cause:** Browser may be blocking downloads or popup permissions.

**Solution:**
- Check browser's download settings
- Allow popups/downloads from the tool's domain
- Try different browser (Chrome, Firefox, Safari, Edge)

## Best Practices

### For Meet Directors

1. **Export immediately after meet** - While data is fresh
2. **Verify team scores** - Check against manual scoresheets
3. **Test export** - Open HTML file to verify display
4. **Use naming convention** - Critical for archive builder
5. **Upload to results directory** - Save in appropriate year folder
6. **Document forfeits** - Use override feature with clear reason

### For Webmasters

1. **Organize by year** - Keep files in `results/YYYY/` directories
2. **Consistent naming** - Enforce `YYYY-MM-DD_TEAM1_v_TEAM2.html` format
3. **Run archive builder** - After each meet to update standings
4. **Backup SDIF files** - Keep original .sd3 files for reference
5. **Test on mobile** - Verify results display on all devices

### For Data Verification

1. **Cross-check scores** - Verify against physical scoresheets
2. **Review relay names** - Ensure all relay swimmers are credited
3. **Check for DQs** - Disqualifications should be noted
4. **Verify age groups** - Confirm swimmers in correct age groups
5. **Look for anomalies** - Unusual times or missing events

## Security Features

### XSS Protection

All user-generated content is sanitized using `escapeHtml()` function:
- Prevents cross-site scripting attacks
- Escape special HTML characters
- Safe to display user-provided forfeit reasons

### Safe Output

Exported HTML is safe and portable:
- No inline JavaScript
- No external dependencies (except Tailwind CDN)
- No tracking or analytics code

## Technical Details

### Libraries Used

- **Tailwind CSS** - UI framework (via CDN)
- **JSZip v3.10.1** - Client-side zip extraction
- **GPSA Common Styles** - Shared GPSA branding CSS

### Browser Compatibility

Works in all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Note:** Internet Explorer is not supported.

### File Size Limits

- **SDIF files:** No practical limit (typical file < 100KB)
- **Zip archives:** 256KB maximum
- **Parsing time:** Usually under 1 second for typical dual meet

### SDIF Parser

The tool's parser (`parseSdif()` function) is approximately 130 lines of JavaScript and handles:
- B1, B2, C1 records (meet/team info)
- D0 records (individual results)
- E0 records (relay results)
- F0 records (relay swimmer names)

## Integration with Archive Builder

### Why Naming Convention Matters

The `build_archive.py` script relies on filenames to:

1. **Extract season year:** `2025-06-16_GG_v_WW.html` → Year: 2025
2. **Parse team matchup:** `GG` vs `WW`
3. **Sort chronologically:** By date in filename
4. **Build schedules:** Match teams with dates
5. **Calculate standings:** Win/loss records per team

### Archive Builder Workflow

1. Export meet results with this tool → `2025-06-16_GG_v_WW.html`
2. Save to results directory → `results/2025/`
3. Run archive builder:
   ```bash
   python dev-tools/build_archive.py -i results/2025 -o results/2025
   ```
4. Generated archive includes all meets with standings

### Forfeit Compatibility

Files with override scores work seamlessly:
- 1.0 vs 0.0 scores are recognized as wins/losses
- Override banner is preserved in archive
- No manual intervention needed

## Related Tools

- [Meet Schedule Generator](/wiki/meet-schedule-generator) - Format division schedules
- [Roster Formatter](/wiki/roster-formatter) - Format team rosters
- **Archive Builder** (`dev-tools/build_archive.py`) - Generate season archives

## FAQ

### Can I edit the HTML after export?

Yes! The exported HTML is standard HTML and can be edited in any text editor or HTML editor. However:
- Maintain consistent structure for archive builder compatibility
- Don't change team scores in the table
- Keep filename convention intact

### Why not support HY3 format?

HY3 files are 65-70% larger and use complex multi-line records requiring extensive parsing logic (250+ lines vs current 130 lines). Since SDIF and HY3 contain identical data and SwimTopia exports SDIF by default, supporting HY3 adds complexity without user benefit.

### Can I customize the styling?

The tool uses Tailwind CSS via CDN. To customize:
- Download the exported HTML
- Modify Tailwind classes directly in HTML
- Or add custom CSS `<style>` block

Note: Customizations won't persist when re-generating from SDIF.

### Does the tool store any data?

No. All processing happens client-side in your browser:
- SDIF files are not uploaded to any server
- No data is stored or transmitted
- All data is temporary in browser memory

### Can I process multiple meets at once?

No, the tool processes one meet at a time. For bulk processing:
- Use `dev-tools/bulk_process_results.py` Python script
- Or process files individually through the web tool

## Support

For issues or questions:

- **Tool Issues** - Contact GPSA webmaster
- **SDIF Export Issues** - Contact SwimTopia support or meet software vendor
- **Archive Builder Issues** - See `dev-tools/README.md`
- **Feature Requests** - Submit via team representative

---

**Quick Links:**
- [Access the Tool](/tools/publicity.html)
- [All GPSA Tools](/tools/)
- [Meet Management](/wiki/meet-management)
- [SwimTopia Guide](/wiki/swimtopia-guide)
