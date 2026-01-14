---
layout: wiki
title: Roster Submittal Process
category: Team Administration
toc: true
last_updated: January 2026
---

This guide walks GPSA team representatives and administrators through the complete process of publishing team rosters to the league SwimTopia site, from exporting data from your team's SwimTopia through formatting and publishing.

## Quick Reference

- **When to publish:** Prior to first dual meet and whenever roster changes
- **Tool used:** [GPSA Roster Formatter](/tools/roster.html)
- **Data source:** SwimTopia Athlete Roster CSV export
- **Where to publish:** Your team's roster page on the league SwimTopia site

## Overview

Each GPSA team is responsible for publishing the following roster information to their team's roster page on the league SwimTopia website:

1. **Athlete Roster** - All registered swimmers organized by age group and gender
2. **Team Contacts** - GPSA Representatives and coaching staff contact information
3. **Certified Officials** - List of officials with their certification levels

The [GPSA Roster Formatter](/tools/roster.html) tool streamlines this process by converting SwimTopia exports into properly formatted HTML ready to paste into the league SwimTopia CMS.

## Step 1: Export Your Roster from SwimTopia

Before using the formatter tool, you need to export your current roster data from SwimTopia.

### Export Process

1. Log in to your team's SwimTopia website with admin access
2. Navigate to **Reports > Athlete Roster**
3. Click the **Generate Report** button
4. On the top right, click **Download Athlete Roster Data (CSV)**
5. Save the file to your computer (e.g., `teamname-2026-roster.csv`)

### Required CSV Columns

The exported CSV must contain these columns (automatically included in SwimTopia exports):

| Column Name | Description | Example |
|-------------|-------------|---------|
| `AgeGroup` | Age group (may include gender prefix) | `9-10`, `Boys 11-12` |
| `AthleteCompetitionCategory` | Gender code | `M` or `F` |
| `AthleteDisplayName` | Swimmer's full name | `Smith, John` |
| `AthleteAge` | Numeric age | `10` |

**Tip:** If you receive a "Missing required columns" error when uploading, verify you exported using **Reports > Athlete Roster** (not a different report type).

## Step 2: Prepare Contact Information

Before using the formatter tool, gather the following contact information:

### GPSA Representatives

Your team's designated GPSA representatives who attend league meetings and coordinate meet operations:

- Full name
- Phone number
- Email address

Most teams have 1-2 GPSA Representatives.

### Coaches

Head coach and any assistant coaches:

- Full name
- Phone number (optional)
- Email address

## Step 3: Prepare Officials List

Gather the names of all certified officials affiliated with your team:

### Stroke & Turn Judges

Officials certified to judge stroke technique and turn legality. List one name per line.

### Starter / Referee

Officials certified as starters or meet referees. List one name per line.

**Note:** Officials should have current certifications on file with USA Swimming or have completed GPSA-approved training.

## Step 4: Use the Roster Formatter Tool

Now you're ready to use the [GPSA Roster Formatter](/tools/roster.html) to process and format your data.

### Upload Your CSV

1. Navigate to the [Roster Formatter Tool](/tools/roster.html)
2. On the **Roster Input** tab, click in the upload area or drag-and-drop your CSV file
3. Wait for the green "Roster processed successfully!" notification
4. The tool will automatically switch to the **Formatted Roster** tab showing your preview

### Enter Contact Information

1. Click the **Contacts** tab
2. Under **GPSA Representatives**, click **Add Rep** for each representative
3. Enter name, phone, and email for each rep
4. Under **Coaches**, click **Add Coach** for each coach
5. Enter name, phone (optional), and email

**Important:** The tool validates email addresses in real-time:
- **Red border** = Invalid email format (must fix before export)
- **Green border** = Valid email format

Phone numbers are automatically formatted to `(XXX) XXX-XXXX` when you enter 10 digits.

### Enter Officials Information

1. Click the **Officials** tab
2. In the **Stroke & Turn** box, paste or type official names (one per line)
3. In the **Starter / Referee** box, paste or type official names (one per line)

### Data Persistence

The tool automatically saves your contacts and officials to your browser's local storage:

- Contacts and officials persist between browser sessions
- Roster data (CSV) is NOT saved and must be re-uploaded each time
- Use the same browser/device for consistency
- Use **Clear** buttons to reset saved data if needed

## Step 5: Review and Export

### Preview Your Data

1. Click the **Formatted Roster** tab
2. Review the athlete roster for accuracy:
   - Swimmers organized by age group
   - Names sorted alphabetically within each group
   - Correct gender assignments
3. Verify contact information is complete
4. Check officials list for completeness

### Export HTML Files

The tool provides three separate exports:

1. **Export Roster HTML** - Click to copy the athlete roster HTML
2. **Export Contacts HTML** - Click to copy the contacts table HTML
3. **Export Officials HTML** - Click to copy the officials list HTML

Each export:
- Copies HTML to your clipboard
- Shows a green success notification
- Produces clean HTML ready for publishing

## Step 6: Publish to League SwimTopia Site

Each team is responsible for publishing their formatted roster to their team's roster page on the league SwimTopia website.

### Publishing Process

1. Log in to the **league** SwimTopia site (not your team site) with admin access
2. Navigate to your team's roster page
3. Click **Edit** on the page
4. Switch to **HTML/Source** mode (usually a `<>` button in the editor toolbar)
5. Select all existing content and delete it (or paste over it)
6. Paste the exported Roster HTML from the formatter tool
7. Switch back to visual mode to preview
8. Click **Save** and **Publish**
9. Repeat for Contacts and Officials sections as needed

### Page Structure

Your team's roster page typically includes three sections:

1. **Athlete Roster** - Use the "Export Roster HTML" output
2. **Team Contacts** - Use the "Export Contacts HTML" output
3. **Certified Officials** - Use the "Export Officials HTML" output

You can publish all three sections on a single page, or your team may have separate pages for each.

## Roster Update Process

### When to Update

Submit roster updates when:
- New swimmers join your team
- Swimmers leave your team
- Contact information changes
- Officials certifications change

### How to Update

1. Export fresh CSV from SwimTopia (roster data changes)
2. Upload to the Roster Formatter tool
3. Your contacts and officials will load automatically from local storage
4. Update any changes to contacts or officials
5. Export and resubmit to GPSA

**Tip:** For minor contact updates only, you can skip the CSV upload and just export the updated contacts HTML.

## Troubleshooting

### "Missing required columns" Error

**Cause:** The CSV doesn't have the required columns.

**Solution:** Re-export from SwimTopia using **Reports > Athlete Roster**. Other report types may not include all required fields.

### Swimmers Appear in Wrong Age Group

**Cause:** SwimTopia age group assignments may not match GPSA age groups.

**Solution:**
- Verify swimmer birthdates in SwimTopia
- Check the age-up date setting for your team
- The tool strips gender prefixes automatically (e.g., "Boys 9-10" becomes "9-10")

### Contacts/Officials Didn't Save

**Cause:** Browser localStorage was cleared, or you're using a different browser/device.

**Solution:**
- Re-enter the information (it will auto-save)
- Use the same browser and device consistently
- Consider keeping a backup document with contact information

### Email Shows Red Border

**Cause:** The email format is invalid.

**Solution:**
- Verify the email includes `@` and a domain (e.g., `name@example.com`)
- Check for extra spaces or typos
- The border turns green when the format is valid

### Export Button Doesn't Work

**Cause:** Browser clipboard permissions or compatibility issue.

**Solution:**
- Use a modern browser (Chrome, Firefox, Safari, Edge)
- Allow clipboard permissions if prompted
- Refresh the page and try again
- The modal shows a "Copy Code" button as backup

## Checklist

Use this checklist to ensure complete roster submittal:

### Before You Start

- [ ] SwimTopia admin access available
- [ ] Current roster finalized in SwimTopia
- [ ] GPSA Representative contact info gathered
- [ ] Coach contact info gathered
- [ ] Officials names and certifications gathered

### Export and Format

- [ ] CSV exported from SwimTopia (Reports > Athlete Roster)
- [ ] CSV uploaded to Roster Formatter tool
- [ ] Roster preview reviewed for accuracy
- [ ] All GPSA Representatives added with valid emails
- [ ] All coaches added
- [ ] Stroke & Turn officials entered
- [ ] Starter/Referee officials entered

### Publish

- [ ] Roster HTML exported and published to league SwimTopia
- [ ] Contacts HTML exported and published
- [ ] Officials HTML exported and published
- [ ] Published page reviewed for accuracy

## Related Resources

- [Roster Formatter Tool](/tools/roster.html) - The formatting tool
- [Roster Formatter Documentation](/wiki/roster-formatter) - Detailed tool documentation
- [SwimTopia Guidelines](/wiki/swimtopia-guidelines) - Complete SwimTopia guide
- [Meet Preparation Guide](/wiki/meet-preparation) - Pre-meet checklist

## Questions?

For questions about the roster submittal process:

- **Tool issues:** Contact the GPSA webmaster
- **SwimTopia export issues:** Contact SwimTopia support or your team administrator
- **Deadline questions:** Contact your division representative
