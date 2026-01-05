# Continuation Prompt - Legacy Rulebook Review

**Last Session Date:** 2026-01-04
**Branch:** `rulebook-development`
**Last Commit:** `398144e` - Complete methodical legacy rulebook section-by-section review

---

## Quick Context Resume

We are conducting a **methodical section-by-section review** of the legacy GPSA rulebook against the new Quarto-based rulebook to ensure complete coverage of all rules and requirements. The goal is to identify gaps, make necessary additions, and document decisions for institutional memory.

---

## What We've Completed

### 12 Sections Fully Reviewed

1. ✅ **GENERAL** - Added general principles, officials rule review requirement
2. ✅ **TROPHIES AND BANNERS** - 100% coverage, no changes needed
3. ✅ **ELIGIBILITY** - Added grace period for disbanded teams, roster responsibilities
4. ✅ **TIME FOR MEETS** - Added meet start definition, warm-up minimums
5. ✅ **OFFICIALS/EQUIPMENT** - Added mutual agreement provisions
6. ✅ **ORDER OF EVENTS** - 100% coverage via USA Swimming references
7. ✅ **MEET OPERATIONS** - 100% coverage (dual meet focus maintained)
8. ✅ **STARTS** - 100% coverage via USA Swimming references
9. ✅ **SWIMMING STROKES AND DISQUALIFICATIONS** - 100% coverage
10. ✅ **SCORING** - Added publicity requirements, postponed meet entries
11. ✅ **PROTESTS** - 100% coverage (even improved over legacy)
12. ⏸️ **DUTIES OF OFFICIALS** - Too large to complete, documented for later

### Key Files Modified

- `docs/rulebook/index.qmd` - General Principles section
- `docs/rulebook/eligibility-and-rosters.md` - Grace period, roster duties
- `docs/rulebook/officials.md` - GPSA Rep duties, artifacts retention, publicity
- `docs/rulebook/conduct-of-meets.md` - Meet start, warm-ups, flexibility, conflict rules

---

## Critical Reference Documents Created

### 1. `docs/rulebook/DUTIES-OF-OFFICIALS-TODO.md`

**Purpose:** Documents pending items from the DUTIES OF OFFICIALS section that require review and decision.

**Key Contents:**
- **Section 1:** 5 critical rulebook additions with proposed wording
  - A. Code of Conduct enforcement (major gap - needs decision)
  - B. Stroke & Turn Judge hand signal requirement
  - C. Referee entry verification before meet
  - D. Referee postponement authority
  - E. Meet Maestro heat sheet publishing rules
- **Section 2:** Wiki/operational guide items (pre-meet conferences, equipment checks, etc.)
- **Section 3:** Items skipped (covered by USA Swimming)
- **Section 4:** Items already well-covered in new rulebook

**Questions Needing Answers:**
- Does a GPSA Code of Conduct document exist?
- Are Code of Conduct enforcement rules still current?
- Are Meet Maestro publishing restrictions still needed?

### 2. `docs/rulebook/LEGACY-DIFFERENCES-INTENTIONALLY-SKIPPED.md`

**Purpose:** Historical record of ~25 items intentionally skipped or ignored with detailed rationale.

**Categories of Skipped Items:**
- Covered by USA Swimming references (8 items)
- Better suited for wiki/operational docs (6 items)
- Invitational-specific rules (3 items)
- Already in other sections (2 items)
- New language is superior (4 items)
- Operational details subject to change (2 items)

**Value:** Provides institutional memory for future boards/committees about why certain legacy rules weren't carried forward.

---

## What's Next - Action Items

### Immediate Priority: DUTIES OF OFFICIALS Section

**Task:** Review and make decisions on the 5 critical items in `DUTIES-OF-OFFICIALS-TODO.md` Section 1.

**Recommended Approach:**

1. **Start with straightforward items** (low-hanging fruit):
   - Item B: Stroke & Turn Judge hand signal (likely add)
   - Item C: Referee entry verification (likely add)
   - Item D: Referee postponement authority (likely add)

2. **Address complex items** (need discussion):
   - Item A: Code of Conduct enforcement (research needed)
   - Item E: Meet Maestro publishing rules (policy decision)

3. **Create wiki content** for Section 2 items (operational guides)

### Secondary Priority: Resolve Deferred Items

Two items have placeholder notes in the rulebook for future discussion:
- Roster submission format and email (`eligibility-and-rosters.md:15`)
- Roster revision timestamp reference (`eligibility-and-rosters.md:41`)

**Action:** Schedule discussion with GPSA board/committee to finalize these operational details.

---

## Methodology Reminder

Our approach has been:

1. **Read legacy section** - Paste section text
2. **Read corresponding new rulebook sections** - Check what's covered
3. **Identify gaps** - What's missing, what's different
4. **Make decisions** - Add, skip, defer, or note for wiki
5. **Document rationale** - Why we made each decision

**Key Principles:**
- ✅ Rulebook = Rules (what must be done)
- ✅ Wiki = Operational guides (how to do it)
- ✅ Meet Invitations = Event-specific variations
- ✅ USA Swimming references = Don't duplicate
- ✅ Modern language > legacy language when equivalent
- ✅ Document all decisions for institutional memory

---

## How to Continue This Work

### Option 1: Continue Legacy Review (if more sections exist)

**Prompt to use:**
> "We're continuing our methodical section-by-section review of the legacy GPSA rulebook. I have the next section ready to review. [Paste next legacy section text here]"

### Option 2: Address DUTIES OF OFFICIALS Pending Items

**Prompt to use:**
> "Let's work through the pending items in `docs/rulebook/DUTIES-OF-OFFICIALS-TODO.md`. I'd like to start with the straightforward items first (B, C, D - hand signals, entry verification, postponement authority). Please read that document and let's add those three items to the rulebook."

### Option 3: Tackle Code of Conduct

**Prompt to use:**
> "Let's research and address the Code of Conduct enforcement items in `docs/rulebook/DUTIES-OF-OFFICIALS-TODO.md` Section 1.A. First, help me search the repository for any existing Code of Conduct document or references to understand what currently exists."

### Option 4: Create Wiki Content

**Prompt to use:**
> "Let's create wiki documentation for the operational guide items listed in `docs/rulebook/DUTIES-OF-OFFICIALS-TODO.md` Section 2. Start with the pre-meet conference procedures."

### Option 5: Resolve Deferred Roster Items

**Prompt to use:**
> "Let's finalize the roster submission details that we deferred. I need to provide specifics on: (1) roster submission format and email, and (2) roster revision timestamp reference method. Here's what I've decided: [your decisions]"

---

## Important Files & Locations

### Rulebook Files
- `docs/rulebook/index.qmd` - Main rulebook index
- `docs/rulebook/officials.md` - Official roles and duties
- `docs/rulebook/conduct-of-meets.md` - Meet procedures
- `docs/rulebook/eligibility-and-rosters.md` - Swimmer eligibility
- `docs/rulebook/order-of-events.md` - Event schedule
- `docs/rulebook/scoring.md` - Scoring rules
- `docs/rulebook/awards.md` - Awards and recognition
- `docs/rulebook/facilities.md` - Pool standards

### Reference Documents
- `docs/rulebook/DUTIES-OF-OFFICIALS-TODO.md` - **READ THIS FIRST**
- `docs/rulebook/LEGACY-DIFFERENCES-INTENTIONALLY-SKIPPED.md` - Historical decisions

### Legacy Rulebook
- `docs/rulebook/GPSA_Rulebook.pdf` - Original legacy rulebook
- `docs/rulebook/GoogleDocsRulebook.pdf` - Google Docs version

---

## Current Branch Status

```bash
git status
# Should show: On branch rulebook-development
# Should be clean (all changes committed)

git log --oneline -5
# Should show: 398144e Complete methodical legacy rulebook section-by-section review
```

---

## Continuation Checklist

Before starting work:
- [ ] Confirm on `rulebook-development` branch
- [ ] Pull latest changes: `git pull origin rulebook-development`
- [ ] Read `DUTIES-OF-OFFICIALS-TODO.md` to understand pending items
- [ ] Decide which action item (Options 1-5 above) to tackle
- [ ] Have legacy rulebook PDF accessible if needed

---

## Notes for AI Assistant

- **Rulebook focus:** Dual meets only (not Championship/invitational meets)
- **USA Swimming references:** Don't duplicate rules covered by USA Swimming
- **Wiki vs Rulebook:** Operational "how-to" goes to wiki, "must do" rules go to rulebook
- **Code of Conduct:** Major unresolved item - may need research/discussion
- **Philosophy:** The user prefers reorganizing content into logical sections rather than preserving legacy structure
- **Decision documentation:** Always explain why we skip/add/modify items

---

## Success Metrics

By the end of this project, we should have:
- ✅ Complete coverage of all legacy rulebook content
- ✅ Clear documentation of all decisions made
- ✅ Wiki content for operational procedures
- ✅ Clean, modern, well-organized rulebook
- ✅ Institutional memory for future GPSA boards

**Current Status:** ~90% complete. Main remaining work is DUTIES OF OFFICIALS section.
