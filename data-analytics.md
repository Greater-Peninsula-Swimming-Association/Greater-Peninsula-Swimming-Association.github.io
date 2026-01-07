# GPSA Swim Data Analytics

## Overview

This document outlines a recommended platform and approach for analyzing GPSA swim meet data from .sd3 (SDIF) format files. The goal is to enable analysis and visualization of swimmer performance across seasons, including comparisons against championship qualifying times.

---

## Recommended Platform

### SQLite + Python + Jupyter Notebooks

**Why this combination:**

1. **SQLite Database** (data storage)
   - Lightweight, file-based, no server needed
   - Perfect for structured swim data (swimmers, meets, events, times)
   - Easy to query for specific analyses
   - Portable - entire database in a single file

2. **Python** (data processing)
   - Already used in GPSA dev-tools infrastructure
   - Can extend existing SDIF parsing logic
   - Key libraries:
     - `sqlite3` - database operations
     - `pandas` - data analysis and manipulation
     - `matplotlib` / `plotly` - data visualization
     - `seaborn` - statistical visualizations

3. **Jupyter Notebooks** (analysis & exploration)
   - Interactive data exploration
   - Document analysis with visualizations
   - Easy to share insights with coaches/board members
   - Reproducible analysis workflows

4. **Optional: Web-based Dashboard** (public visualization)
   - Build GPSA-branded tool using existing template system
   - Interactive charts for parents/swimmers to track progress
   - Show qualifying time comparisons, improvement trends, etc.
   - Integrate with existing GPSA website

---

## Database Schema Design

### Core Tables

```sql
-- Swimmers
CREATE TABLE swimmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    swimmer_id TEXT UNIQUE NOT NULL,  -- From SDIF
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    team_code TEXT NOT NULL,
    gender TEXT NOT NULL,
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Meets
CREATE TABLE meets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meet_name TEXT NOT NULL,
    meet_date DATE NOT NULL,
    season INTEGER NOT NULL,  -- e.g., 2025
    division TEXT,  -- Division 1, 2, 3
    meet_type TEXT,  -- dual, invitational, championship
    home_team TEXT,
    away_team TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_code TEXT UNIQUE NOT NULL,
    stroke TEXT NOT NULL,  -- Free, Back, Breast, Fly, IM, Medley Relay, Free Relay
    distance INTEGER NOT NULL,  -- in meters (25, 50, 100, 200)
    age_group TEXT NOT NULL,  -- 8U, 9-10, 11-12, 13-14, 15-18
    gender TEXT NOT NULL,  -- M, F
    relay BOOLEAN DEFAULT 0
);

-- Times (race results)
CREATE TABLE times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    swimmer_id INTEGER NOT NULL,
    meet_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    time_seconds REAL NOT NULL,
    points INTEGER,
    place INTEGER,
    heat INTEGER,
    lane INTEGER,
    dq BOOLEAN DEFAULT 0,
    exhibition BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (swimmer_id) REFERENCES swimmers(id),
    FOREIGN KEY (meet_id) REFERENCES meets(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Qualifying Standards
CREATE TABLE qualifying_standards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    meet_type TEXT NOT NULL,  -- championship, invitational
    qualifying_time REAL NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Teams
CREATE TABLE teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_code TEXT UNIQUE NOT NULL,
    team_name TEXT NOT NULL,
    division TEXT,
    active BOOLEAN DEFAULT 1
);
```

### Indexes for Performance

```sql
CREATE INDEX idx_times_swimmer ON times(swimmer_id);
CREATE INDEX idx_times_meet ON times(meet_id);
CREATE INDEX idx_times_event ON times(event_id);
CREATE INDEX idx_meets_season ON meets(season);
CREATE INDEX idx_swimmers_team ON swimmers(team_code);
```

---

## Example Analyses

### 1. Time Drops Across Season
Track individual swimmer improvement throughout the season:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Get all swims for a specific swimmer in a specific event
query = """
SELECT m.meet_date, t.time_seconds, e.stroke, e.distance
FROM times t
JOIN meets m ON t.meet_id = m.id
JOIN events e ON t.event_id = e.id
JOIN swimmers s ON t.swimmer_id = s.id
WHERE s.swimmer_id = ? AND e.event_code = ?
ORDER BY m.meet_date
"""
df = pd.read_sql_query(query, conn, params=['swimmer_id', 'event_code'])

# Plot progression
plt.plot(df['meet_date'], df['time_seconds'])
plt.title('Swimmer Progression - 50m Freestyle')
plt.xlabel('Date')
plt.ylabel('Time (seconds)')
plt.show()
```

### 2. Qualifying Time Comparisons
Identify swimmers close to championship qualifying times:
```python
query = """
SELECT
    s.first_name, s.last_name, s.team_code,
    e.stroke, e.distance, e.age_group,
    MIN(t.time_seconds) as best_time,
    q.qualifying_time,
    (t.time_seconds - q.qualifying_time) as gap
FROM times t
JOIN swimmers s ON t.swimmer_id = s.id
JOIN events e ON t.event_id = e.id
JOIN meets m ON t.meet_id = m.id
JOIN qualifying_standards q ON e.id = q.event_id AND m.season = q.season
WHERE m.season = 2025 AND q.meet_type = 'championship'
GROUP BY s.id, e.id
HAVING best_time <= qualifying_time * 1.05  -- Within 5% of qualifying
ORDER BY gap DESC
```

### 3. Team Performance Trends
Compare team performance across seasons:
```python
query = """
SELECT
    m.season,
    s.team_code,
    COUNT(*) as total_swims,
    AVG(t.points) as avg_points,
    SUM(CASE WHEN t.place = 1 THEN 1 ELSE 0 END) as first_places
FROM times t
JOIN swimmers s ON t.swimmer_id = s.id
JOIN meets m ON t.meet_id = m.id
WHERE t.dq = 0 AND t.exhibition = 0
GROUP BY m.season, s.team_code
ORDER BY m.season, avg_points DESC
```

### 4. Event Participation Patterns
Identify which events have the most/least participation:
```python
query = """
SELECT
    e.stroke, e.distance, e.age_group,
    COUNT(DISTINCT t.swimmer_id) as unique_swimmers,
    COUNT(*) as total_swims,
    AVG(t.time_seconds) as avg_time
FROM times t
JOIN events e ON t.event_id = e.id
JOIN meets m ON t.meet_id = m.id
WHERE m.season = 2025
GROUP BY e.id
ORDER BY unique_swimmers DESC
```

### 5. Personal Records & Improvements
Track personal bests and improvement rates:
```python
query = """
WITH ranked_times AS (
    SELECT
        t.swimmer_id,
        t.event_id,
        t.time_seconds,
        m.meet_date,
        ROW_NUMBER() OVER (PARTITION BY t.swimmer_id, t.event_id ORDER BY t.time_seconds) as rank
    FROM times t
    JOIN meets m ON t.meet_id = m.id
    WHERE t.dq = 0
)
SELECT
    s.first_name, s.last_name,
    e.stroke, e.distance, e.age_group,
    rt.time_seconds as personal_best,
    rt.meet_date as pr_date
FROM ranked_times rt
JOIN swimmers s ON rt.swimmer_id = s.id
JOIN events e ON rt.event_id = e.id
WHERE rt.rank = 1
ORDER BY s.last_name, e.stroke, e.distance
```

### 6. Heat Sheet Predictions
Predict likely times based on season performance:
```python
query = """
SELECT
    s.swimmer_id,
    s.first_name,
    s.last_name,
    e.stroke,
    e.distance,
    AVG(t.time_seconds) as avg_time,
    MIN(t.time_seconds) as best_time,
    MAX(t.time_seconds) as worst_time,
    COUNT(*) as swim_count
FROM times t
JOIN swimmers s ON t.swimmer_id = s.id
JOIN events e ON t.event_id = e.id
JOIN meets m ON t.meet_id = m.id
WHERE m.season = 2025 AND t.dq = 0
GROUP BY s.id, e.id
HAVING swim_count >= 2
ORDER BY e.stroke, e.distance, avg_time
```

---

## Implementation Pathway

### Phase 1: SDIF Parser to SQLite
**Goal:** Convert .sd3 files into structured database

**Tasks:**
- Create Python script to parse SDIF files
- Extract swimmer, meet, event, and time data
- Handle team name mapping (similar to `build_archive.py`)
- Insert data into SQLite database
- Handle duplicates and updates

**Deliverable:** `sdif_to_sqlite.py` script

### Phase 2: Database Setup & Schema
**Goal:** Initialize database with proper structure

**Tasks:**
- Create SQLite database schema
- Add indexes for performance
- Populate events table with standard GPSA events
- Import qualifying standards for championship meets
- Populate teams table

**Deliverable:** `init_database.sql` and setup script

### Phase 3: Bulk Import Historical Data
**Goal:** Import 3 years of SDIF files

**Tasks:**
- Run parser on all .sd3 files from recent seasons
- Validate data integrity
- Generate import report (swimmers, meets, total swims)
- Handle edge cases (forfeits, DQs, exhibitions)

**Deliverable:** Populated database with historical data

### Phase 4: Analysis Notebooks
**Goal:** Create reusable Jupyter notebooks for common analyses

**Tasks:**
- Notebook: Swimmer progression tracking
- Notebook: Qualifying time analysis
- Notebook: Team performance comparison
- Notebook: Event participation trends
- Notebook: Personal records report

**Deliverable:** `/analysis/notebooks/` directory with examples

### Phase 5: Web-based Visualization (Optional)
**Goal:** Public-facing analytics tool

**Tasks:**
- Design GPSA-branded analytics page using tool template
- Interactive charts (time drops, qualifying times, PRs)
- Swimmer search and personal dashboards
- Team performance leaderboards
- Export capabilities (PDF reports, CSV data)

**Deliverable:** `tools/analytics.html` or separate analytics subdomain

---

## Data Sources

### Input: SDIF Files (.sd3)
- 3 years of dual meet results
- Invitational results
- Championship meet results

### Output: SQLite Database
- Structured, queryable data
- Portable single-file format
- Ready for analysis and visualization

### Reference: Qualifying Standards
- Championship qualifying times by event/age group
- Invitational qualifying times
- Historical standards for trend analysis

---

## Tools & Libraries

### Python Dependencies
```bash
pip install pandas matplotlib seaborn plotly jupyter sqlite3
```

### Optional Visualization Libraries
```bash
pip install dash streamlit  # For interactive web dashboards
```

### Jupyter Setup
```bash
jupyter notebook  # Launch notebook server
```

---

## Next Steps

1. **Decide scope:** Start with Phase 1-3 (database + import) or include Phase 4-5 (analysis + web)?
2. **Create SDIF parser:** Build on existing SDIF parsing logic from `publicity.html`
3. **Design database schema:** Finalize table structure and relationships
4. **Import historical data:** Process 3 years of .sd3 files
5. **Build analysis notebooks:** Create reusable templates for common queries
6. **(Optional) Build web dashboard:** Public-facing analytics tool

---

## Questions to Consider

- **Access control:** Should analytics be public or restricted?
- **Update frequency:** Real-time during season or batch import after meets?
- **User audience:** Coaches only, or parents/swimmers too?
- **Export formats:** PDF reports, CSV downloads, or just web interface?
- **Historical data:** How far back to import? (Currently: 3 years)
- **Privacy:** Any PII considerations for swimmer data?

---

## References

- Existing GPSA tools: `tools/publicity.html`, `dev-tools/build_archive.py`
- SDIF format documentation: [SDIF Standard](https://www.usaswimming.org/docs/default-source/timesdocuments/sd3-file-format.pdf)
- GPSA tool template: `templates/tool-template.html`
- GPSA documentation: `DOCUMENTATION.md`, `MAINTENANCE.md`
