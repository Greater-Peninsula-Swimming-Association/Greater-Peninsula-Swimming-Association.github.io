# GPSA Website Maintenance Guide

Testing checklists, troubleshooting guides, and maintenance procedures.

## Table of Contents
- [Testing Checklists](#testing-checklists)
- [Troubleshooting](#troubleshooting)
- [Known Limitations](#known-limitations)
- [Maintenance Procedures](#maintenance-procedures)

---

## Testing Checklists

### Roster Tool (tools/roster.html)

**Pre-Release Checklist:**
- [ ] Upload valid SwimTopia CSV and verify roster displays correctly
- [ ] Test email validation with invalid formats (missing @, no domain)
- [ ] Verify phone auto-formatting with 10-digit numbers
- [ ] Confirm localStorage persists after browser restart
- [ ] Test all three exports (roster, contacts, officials)
- [ ] Verify toast notifications appear and auto-dismiss
- [ ] Test modal focus trap with Tab/Shift+Tab
- [ ] Confirm Esc key closes modal
- [ ] Test clear buttons and confirm localStorage is wiped
- [ ] Test with empty CSV file
- [ ] Test with CSV missing required columns
- [ ] Test duplicate contact names trigger warnings
- [ ] Verify export blocked with invalid emails
- [ ] Test click-outside-to-close for modals
- [ ] Verify aria-labels update dynamically

**Browser Compatibility:**
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

### Publicity Tool (tools/publicity.html)

**Pre-Release Checklist:**
- [ ] Test with .sd3 file
- [ ] Test with .txt file (SDIF format)
- [ ] Test with .zip file containing SDIF
- [ ] Test with multi-file .zip (uses first SDIF found)
- [ ] Verify forfeit override UI works correctly
- [ ] Test override banner appears in exported HTML
- [ ] Verify exported HTML follows naming convention
- [ ] Test with empty/malformed SDIF file
- [ ] Verify toast notifications for errors
- [ ] Test relay events display swimmer names
- [ ] Verify team codes strip "VA" prefix
- [ ] Test exported HTML is self-contained (no external dependencies)
- [ ] Verify GPSA brand colors used correctly

**Edge Cases:**
- [ ] SDIF file with no meet date
- [ ] SDIF file with no team names
- [ ] Very large meet (100+ events)
- [ ] Meet with only relay events
- [ ] Meet with only individual events
- [ ] File size at 256KB limit

---

### Season Archive Generator (dev-tools/build_archive.py)

**Pre-Release Checklist:**
- [ ] Test with complete season (40+ meets)
- [ ] Test with incomplete season (10-20 meets)
- [ ] Verify year auto-detection works
- [ ] Test division clustering with 3 divisions
- [ ] Test with mixed years (should warn)
- [ ] Verify interactive prompts work correctly
- [ ] Test verbose logging mode
- [ ] Verify output HTML is responsive
- [ ] Test breadcrumb navigation in output
- [ ] Verify win/loss records calculate correctly
- [ ] Test with forfeit meets (1.0 vs 0.0 scores)
- [ ] Verify mobile date abbreviations work

**Edge Cases:**
- [ ] Only 2 divisions detected
- [ ] 4+ divisions detected
- [ ] Team competed in multiple divisions
- [ ] Meet filename doesn't match pattern
- [ ] HTML file missing required data

---

### Directory Index Generator (dev-tools/generate_index.py)

**Pre-Release Checklist:**
- [ ] Run from repository root
- [ ] Run from subdirectory
- [ ] Run from nested subdirectory
- [ ] Verify breadcrumb navigation correct
- [ ] Verify relative CSS paths correct
- [ ] Test with empty directory
- [ ] Test with directory containing only files
- [ ] Test with directory containing only subdirectories
- [ ] Verify excluded directories are skipped
- [ ] Verify hidden files/folders ignored
- [ ] Check GPSA header renders correctly
- [ ] Verify hover effects work

---

## Troubleshooting

### Roster Tool Issues

**Issue: Roster not displaying after CSV upload**
- Check CSV has required headers: `AgeGroup`, `AthleteCompetitionCategory`, `AthleteDisplayName`, `AthleteAge`
- Verify CSV is from SwimTopia export (not manually created)
- Check browser console for JavaScript errors
- Try clearing localStorage: `localStorage.clear()`

**Issue: Exports missing styling**
- External CSS must be hosted on `publicity.gpsaswimming.org`
- Verify CSS files exist:
  - `css/gpsa-roster.css`
  - `css/gpsa-roster-contact.css`
  - `css/gpsa-roster-officials.css`
- SwimTopia CMS must reference external stylesheets

**Issue: localStorage not persisting**
- Check browser privacy settings (may block localStorage)
- Verify not in Private/Incognito mode
- Check localStorage quota not exceeded (~5-10MB limit)

**Issue: Phone formatting not working**
- Ensure 10-digit number entered
- Format only applies on blur (leaving the field)
- Non-US formats not supported

---

### Publicity Tool Issues

**Issue: SDIF file not processing**
- Verify file is SDIF format (.sd3 or .txt), not HY3
- Check file size under 256KB for .zip files
- Verify SDIF has required records: B1, C1
- Check browser console for parsing errors

**Issue: Zip file extraction fails**
- Check .zip file size under 256KB
- Verify .zip contains .sd3 or .txt file
- Ensure not password-protected
- Try extracting manually to verify contents

**Issue: Forfeit override not working**
- Ensure "Process Results" clicked before selecting winning team
- Verify team selected from dropdown (not typed)
- Check reason field is not empty
- Look for validation toast messages

**Issue: Exported HTML not opening**
- Verify HTML file saved completely (check file size > 0)
- Try opening in different browser
- Check for JavaScript errors in console

---

### Season Archive Generator Issues

**Issue: Year detection fails**
- Verify filenames match `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- Check YYYY is valid 4-digit year
- Ensure at least one file exists in directory

**Issue: Expected 3 divisions but detected X**
- **Fewer than 3**: Season incomplete or teams competed cross-division
  - Wait for more meets
  - Manually verify team schedules
- **More than 3**: Teams split into smaller clusters
  - Check for data errors in meet files
  - Verify teams competed within correct divisions

**Issue: Team not found in any division**
- Team may only have competed in non-division meets (invitationals)
- Check meet files include team correctly
- Verify team name matches in all files

**Issue: Win/loss records incorrect**
- Verify team scores in source HTML files
- Check forfeit meets have 1.0 vs 0.0 scores
- Ensure no duplicate meets in directory

---

### Directory Index Generator Issues

**Issue: CSS not loading**
- Verify `css/gpsa-tools-common.css` exists
- Check relative path calculation is correct
- Try running from repository root

**Issue: Breadcrumbs incorrect**
- Verify script can find repository root
- Check path calculation logic
- Ensure index.html exists in parent directories

---

## Known Limitations

### Roster Tool
- **localStorage Limit**: ~5-10MB per domain (sufficient for typical use)
- **Phone Formatting**: Assumes US format (XXX) XXX-XXXX only
- **Email Validation**: Basic regex (accepts most valid formats but not comprehensive)
- **CSV Parsing**: Requires exact SwimTopia column headers
- **No File Download**: Tool designed for copy/paste to SwimTopia CMS only
- **No PDF Export**: Out of scope for this tool
- **No Team Logos**: Not needed for current workflow

### Publicity Tool
- **No HY3 Support**: Only SDIF format supported (see DOCUMENTATION.md for rationale)
- **Zip File Size**: 256KB maximum for .zip files
- **Single Meet Only**: Cannot process multiple meets in one operation
- **Date Format**: Expects MMDDYYYY in SDIF B1 record
- **Team Code Stripping**: Hardcoded to strip "VA" prefix only

### Season Archive Generator
- **3 Divisions Required**: Assumes exactly Red, White, Blue divisions
- **Dual Meets Only**: Invitationals not included in standings
- **Filename Dependency**: Requires strict `YYYY-MM-DD_TEAM1_v_TEAM2.html` format
- **Team Name Mapping**: Requires updates in script for new teams
- **No Mid-Season Changes**: Cannot handle team moving between divisions

### Directory Index Generator
- **Hardcoded Exclusions**: `.git`, `dev-tools`, `assets`, `resources`, `css`, `tools`
- **Icon Limitation**: Only 📁 and 📄 (no file-type specific icons)
- **No Sorting Options**: Always alphabetical
- **No File Size Display**: Only shows file names

---

## Maintenance Procedures

### Roster Tool Maintenance

**What to Maintain:**
- Keep PapaParse library updated (currently CDN v5.4.1)
- Ensure GPSA brand colors consistent: `#002366`, `#d9242b`
- Test localStorage compatibility with new browsers
- Maintain XSS protection - never remove `escapeHtml()` sanitization

**What NOT to Add:**
- File download features (purpose is copy/paste to CMS only)
- Embedded CSS in exports (external CSS is intentional)
- PDF export (out of scope)
- Team logo uploads (not needed)

**Update Schedule:**
- **Quarterly**: Check PapaParse for updates
- **Annually**: Test with latest browsers
- **As Needed**: Update when SwimTopia changes CSV format

---

### Publicity Tool Maintenance

**What to Maintain:**
- Keep JSZip library updated (currently v3.10.1)
- Test SDIF parsing with new SwimTopia exports
- Verify Tailwind CDN availability
- Maintain escapeHtml() for security

**What NOT to Add:**
- HY3 format support (intentionally excluded)
- Bulk processing (use dev-tools/bulk_process_results.py)
- Database storage (standalone tool by design)

**Update Schedule:**
- **Quarterly**: Check JSZip and Tailwind for updates
- **Pre-Season**: Test with sample SDIF files
- **As Needed**: Update when SDIF format changes

---

### Season Archive Generator Maintenance

**What to Maintain:**
- Keep BeautifulSoup4 updated: `pip install --upgrade beautifulsoup4`
- Update team name mappings when teams join/leave league
- Test responsive design on new mobile devices
- Verify division clustering algorithm accuracy

**Team Name Updates Required When:**
- New team joins league
- Team changes name
- Team abbreviation changes

**Update Locations:**
```python
# In build_archive.py:
TEAM_NAME_MAP = {...}           # Full name → abbreviation
TEAM_SCHEDULE_NAME_MAP = {...}  # Full name → short display
FILENAME_ABBR_MAP = {...}       # Filename abbr → official abbr
```

**Update Schedule:**
- **Pre-Season**: Update team mappings
- **Mid-Season**: Verify division clustering works correctly
- **Post-Season**: Review for improvements

---

### Directory Index Generator Maintenance

**What to Maintain:**
- Keep shared CSS file updated (`css/gpsa-tools-common.css`)
- Verify Tailwind CDN availability
- Update exclusion list if new directories added

**Update Schedule:**
- **Annually**: Review exclusion list
- **As Needed**: Update when site structure changes

---

### CSS and Shared Resources

**css/gpsa-tools-common.css Maintenance:**
- Keep GPSA brand colors consistent
- Test responsive breakpoints on new devices
- Verify toast notification animations work
- Maintain print styles

**Update Schedule:**
- **Quarterly**: Review for improvements
- **As Needed**: Update when adding new tools

---

### Wiki System Maintenance

**What to Maintain:**
- Keep Jekyll compatible with GitHub Pages
- Update wiki pages as tools change
- Verify sidebar navigation stays current
- Test responsive design

**Update Schedule:**
- **Monthly**: Review wiki pages for accuracy
- **After Tool Updates**: Update corresponding wiki docs
- **Annually**: Review entire wiki for outdated content

---

## Security Notes

### XSS Protection
All user input MUST be sanitized using `escapeHtml()`:
```javascript
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

**Where to Apply:**
- All form inputs displayed in HTML
- All CSV/file data displayed in results
- All toast notification messages
- All exported HTML content

### localStorage Security
- Never store sensitive data (passwords, tokens)
- Data is domain-specific (not shared across sites)
- Users can clear via browser settings
- No encryption (data is client-side only)

### File Upload Security
- Client-side processing only (no server uploads)
- File size limits enforced (256KB for .zip)
- File type validation (accept attribute + MIME check)
- No executable files accepted

---

## Performance Notes

### Optimization Opportunities
- **Roster Tool**: PapaParse handles up to 1000+ rows efficiently
- **Publicity Tool**: SDIF parsing optimized for typical meet size (50-80 events)
- **Archive Generator**: BeautifulSoup can handle 100+ meet files
- **All Tools**: Tailwind CDN cached by browsers

### Performance Monitoring
- Monitor browser console for warnings
- Check page load times periodically
- Test with large datasets occasionally
- Verify mobile performance

---

## Backup and Recovery

### localStorage Backup
Users should periodically export:
- Contacts (copy from tool to text file)
- Officials (copy from tool to text file)

No automated backup available.

### Git Repository
- All code version controlled
- Commit frequently
- Use descriptive commit messages
- Keep main branch stable

### Generated Files
- Season archives: Keep copies in multiple locations
- Directory indexes: Can be regenerated from script
- Meet results: Store SDIF source files separately

---

## Support and Reporting Issues

### When to Contact Maintainer
- Critical bugs affecting data accuracy
- Security vulnerabilities
- Breaking changes in external dependencies
- New team requirements

### Information to Provide
- Browser/OS version
- Steps to reproduce
- Screenshots/error messages
- Sample data (if applicable, sanitized)

### Self-Service Troubleshooting
1. Check browser console for errors
2. Verify file formats match requirements
3. Clear localStorage and retry
4. Test in different browser
5. Review documentation
