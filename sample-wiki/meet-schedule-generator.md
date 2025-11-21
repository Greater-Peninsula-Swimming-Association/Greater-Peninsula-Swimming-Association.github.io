---
layout: sample-wiki
title: Meet Schedule Generator
category: Tools
toc: true
last_updated: November 2025
---

The **GPSA Meet Schedule Generator** is a web-based tool that converts the master schedule CSV file (used to submit schedules to SwimTopia) into beautifully formatted HTML tables for display on the GPSA website or team websites.

## Quick Start

1. Obtain the master schedule CSV file from your league administrator
2. Visit [Meet Schedule Generator Tool](/tools/meet-schedule.html)
3. Upload the schedule CSV file
4. Select the division (Red, White, or Blue)
5. Click "Generate Schedule"
6. Copy the formatted HTML to your clipboard
7. Paste into the GPSA website, SwimTopia CMS, or team website

## What It Does

The Meet Schedule Generator transforms the master schedule CSV data into professional, responsive HTML tables that match GPSA's visual branding. The tool:

- Parses schedule CSV files containing meet dates and team matchups
- Groups meets by date with formatted date headers (e.g., "MONDAY JUNE 16")
- Converts team abbreviations to readable team names
- Generates responsive HTML tables styled with GPSA colors
- Provides copy-to-clipboard functionality for easy publishing

## Getting the CSV File

### Source of the CSV File

The CSV file used by this tool is the **master schedule file** that is uploaded to SwimTopia to populate all team schedules at the beginning of the season. This is typically:

- Created by the GPSA league administrator or scheduler
- Contains the complete season schedule for a division
- Used to submit meets to SwimTopia so they appear on all team calendars
- Maintained as the authoritative source for the season schedule

**Who has this file?**
- League officers (President, VP, Scheduler)
- Division coordinators
- GPSA webmaster

**When is it created?**
- Before the season starts (typically May)
- Updated if meet dates or matchups change

If you need the CSV file, contact your league administrator or division coordinator.

### Required CSV Format

The CSV file must contain these columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| `MeetDate` | Date of the meet | `6/16/2025` |
| `HomeTeam` | Home team abbreviation | `GG` |
| `VisitingTeam` | Away team abbreviation | `WW` |

**Note:** The tool ignores all other columns, so if your CSV has additional columns (location, time, etc.) they won't affect the output.

## Division Selection

The tool requires you to specify which division the schedule is for:

- **Red Division**
- **White Division**
- **Blue Division**

### Auto-Detection

The tool will automatically detect the division if your filename contains one of these keywords:
- `red` → Selects Red Division
- `white` → Selects White Division
- `blue` → Selects Blue Division

**Example:** Uploading `2025-red-division-schedule.csv` will auto-select Red Division.

## Team Name Mapping

The tool automatically converts SwimTopia team abbreviations to readable names:

| Abbreviation | Display Name |
|--------------|--------------|
| BLMAR | Beaconsdale |
| COL | Colony |
| CV | Coventry |
| EL | Elizabeth Lake |
| GG | Glendale |
| GWRA | George Wythe |
| HW | Hidenwood |
| JRCC | James River |
| KCD | Kiln Creek |
| MBKMT | Marlbank |
| NHM | Northampton |
| POQ | Poquoson |
| RRST | Riverdale |
| RMMR | Running Man |
| WW | Wendwood |
| WO | Willow Oaks |
| WPPIR | Windy Point |
| WYCC | Warwick Yacht |

If a team abbreviation is not in this list, it will be displayed as-is.

## Generated Output Format

The tool generates HTML that renders as:

```
MONDAY JUNE 16
----------------------------------
Glendale          vs    Wendwood
Beaconsdale       vs    Riverdale

THURSDAY JUNE 19
----------------------------------
Elizabeth Lake    vs    Kiln Creek
James River       vs    Northampton
```

The output uses:
- GPSA brand colors (Navy Blue #002366)
- Responsive table design (mobile-friendly)
- Consistent formatting matching other GPSA pages
- External CSS reference to `/css/gpsa-main.css`

## Using the Generated HTML

### For GPSA Website

The primary use case is publishing division schedules to the main GPSA website:

1. Click **Copy to Clipboard** button in the tool
2. Save the HTML to a file (e.g., `red-division-schedule.html`)
3. Upload to the appropriate location on the GPSA website
4. Link from the main schedule page

**Note:** The HTML references external CSS at `https://publicity.gpsaswimming.org/css/gpsa-main.css` which provides the styling.

### For SwimTopia Team Pages

Individual teams can also publish division schedules on their team sites:

1. Click **Copy to Clipboard** button in the tool
2. Log in to your SwimTopia team site admin
3. Navigate to the page where you want to display the schedule
4. Switch to **HTML/Source** editing mode
5. Paste the HTML code
6. Save and publish

### For Other Websites

If embedding on another platform:

1. Ensure the external CSS file is accessible: `https://publicity.gpsaswimming.org/css/gpsa-main.css`
2. Paste the HTML into your page source
3. Test responsiveness on mobile devices

## Features

### Responsive Design

The generated schedules are fully responsive and display well on:
- **Desktop** - Full width with proper spacing
- **Tablet** - Optimized for medium screens
- **Mobile** - Stacked layout for readability

### Accessibility

- Semantic HTML table structure
- Proper table headers for screen readers
- High contrast text for visibility

### Toast Notifications

The tool uses modern toast notifications instead of popup alerts:
- ✓ **Success** (green) - CSV loaded successfully
- ✕ **Error** (red) - CSV parsing errors or missing columns
- ℹ **Info** (blue) - Processing updates

## Troubleshooting

### "Missing required columns" Error

**Cause:** Your CSV doesn't have the required `MeetDate`, `HomeTeam`, or `VisitingTeam` columns.

**Solution:** Verify the CSV file has the correct column headers. Contact your league administrator if the file format appears incorrect.

### "Error parsing CSV file" Message

**Cause:** The file may be corrupted or not a valid CSV format.

**Solution:**
1. Open the CSV in a text editor to verify it looks correct
2. Check that the file is saved as CSV format (not `.xlsx` or other spreadsheet format)
3. Contact your league administrator for a fresh copy of the schedule CSV

### Team Names Not Displaying Correctly

**Cause:** Team abbreviation not in the mapping table.

**Solution:** The tool will display the abbreviation as-is. If this is a new team, contact the GPSA webmaster to update the tool's team mapping.

### Division Not Auto-Detecting

**Cause:** Filename doesn't contain "red", "white", or "blue".

**Solution:** Manually select the division using the radio buttons before clicking "Generate Schedule".

## Technical Details

### Libraries Used

- **PapaParse v5.4.1** - CSV parsing library
- **Tailwind CSS** - UI framework (via CDN)
- **GPSA Common Styles** - Shared GPSA branding CSS

### Browser Compatibility

The tool works in all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Note:** Internet Explorer is not supported.

### File Size Limits

- Maximum CSV file size: 5 MB
- Recommended: Keep schedules to one division per file
- No limit on number of meets per file

## Best Practices

### For League Administrators

1. **Maintain master CSV** - Keep the authoritative schedule CSV in a central location
2. **Name files clearly** - Include division and year (e.g., `2025-red-division-schedule.csv`)
3. **Version control** - Save dated versions if schedule changes (e.g., `2025-red-schedule-v2.csv`)
4. **Coordinate updates** - If dates change, regenerate HTML and notify teams

### For Webmasters

1. **Test in preview** - Review the generated HTML before publishing
2. **Verify styling** - Ensure external CSS loads correctly on production site
3. **Mobile testing** - Check display on phones and tablets
4. **Link prominently** - Make schedules easy to find from main navigation

### For All Users

1. **Contact admin for CSV** - Don't try to create the CSV yourself unless you're the scheduler
2. **Check division** - Ensure you've selected the correct division before generating
3. **Preserve formatting** - Don't manually edit the CSV unless you understand the structure

## Related Tools

- [Roster Formatter](/wiki/roster-formatter) - Format team rosters for SwimTopia
- [Publicity Processor](/wiki/publicity-processor) - Generate meet result reports

## Support

For issues or questions about the Meet Schedule Generator:

- **Need the CSV file?** - Contact your league administrator or division coordinator
- **Technical Issues** - Contact the GPSA webmaster
- **Schedule Changes** - Contact your league scheduler or division coordinator
- **Feature Requests** - Submit via your team representative or league officers

---

**Quick Links:**
- [Access the Tool](/tools/meet-schedule.html)
- [All GPSA Tools](/tools/)
- [Meet Management](/wiki/meet-management)
