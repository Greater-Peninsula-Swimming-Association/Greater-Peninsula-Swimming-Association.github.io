import argparse
import os
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime

# --- Configuration ---
# This section can be easily updated with new teams or division assignments.

# Maps team abbreviations to their assigned division.
DIVISION_ASSIGNMENTS = {
    'Red': ['COL', 'HW', 'MBKMT', 'POQ', 'RMMR', 'WPPIR'],
    'White': ['CV', 'GWRA', 'GG', 'WYCC', 'WW', 'WO'],
    'Blue': ['BLMAR', 'EL', 'JRCC', 'KCD', 'RRST']
}

# Maps the full team names found in result files to their official abbreviations.
# This map is crucial for linking results to the correct team for standings.
TEAM_NAME_MAP = {
    "Colony Cudas": "COL",
    "Hidenwood Tarpons": "HW",
    "Marlbank Mudtoads": "MBKMT",
    "Poquoson Barracudas": "POQ",
    "Running Man Manta Rays": "RMMR",
    "Windy Point Piranhas": "WPPIR",
    "Coventry Sailfish Swim Team": "CV",
    "George Wythe Wahoos": "GWRA",
    "Glendale Gators": "GG",
    "WYCC Sea Turtles": "WYCC",
    "Wendwood Wahoos": "WW",
    "Willow Oaks Stingrays": "WO",
    "Beaconsdale Blue Marlins": "BLMAR",
    "Elizabeth Lake Tideriders": "EL",
    "James River Country Club": "JRCC",
    "Kiln Creek Dolphins": "KCD",
    "Riverdale Rays": "RRST"
}

# Maps full team names to the shorter names used in the schedule table.
TEAM_SCHEDULE_NAME_MAP = {
    "Colony Cudas": "Colony",
    "Hidenwood Tarpons": "Hidenwood",
    "Marlbank Mudtoads": "Marlbank",
    "Poquoson Barracudas": "Poquoson",
    "Running Man Manta Rays": "Running Man",
    "Windy Point Piranhas": "Windy Point",
    "Coventry Sailfish Swim Team": "Coventry",
    "George Wythe Wahoos": "George Wythe",
    "Glendale Gators": "Glendale",
    "WYCC Sea Turtles": "Warwick Yacht",
    "Wendwood Wahoos": "Wendwood",
    "Willow Oaks Stingrays": "Willow Oaks",
    "Beaconsdale Blue Marlins": "Beaconsdale",
    "Elizabeth Lake Tideriders": "Elizabeth Lake",
    "James River Country Club": "James River",
    "Kiln Creek Dolphins": "Kiln Creek",
    "Riverdale Rays": "Riverdale"
}

# Maps truncated filename abbreviations to their official, full-length counterparts.
FILENAME_ABBR_MAP = {
    "MBKM": "MBKMT",
    "WPPI": "WPPIR",
    "BLMA": "BLMAR"
}


def parse_meet_file(file_path, team_name_map, schedule_name_map, filename_abbr_map):
    """Parses a single meet result file to extract teams and scores, using the filename to determine home/away."""
    try:
        # --- Extract Home/Away from filename (e.g., "YYYY-MM-DD_HOME_v_AWAY.html") ---
        basename = os.path.basename(file_path)
        parts = basename.replace('.html', '').split('_')
        
        if len(parts) < 4 or parts[2].lower() != 'v':
            print(f"Warning: Filename {basename} does not match 'DATE_HOME_v_AWAY.html' format. Skipping.")
            return None
        
        date_str = parts[0]
        # Get the official abbreviation from the filename, using the map as a translator
        home_abbr_from_file = filename_abbr_map.get(parts[1], parts[1])
        away_abbr_from_file = filename_abbr_map.get(parts[3], parts[3])
        
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find the team scores table
        scores_header = soup.find('h2', string='Team Scores')
        if not scores_header: return None
        scores_table = scores_header.find_next('table')
        if not scores_table: return None
        rows = scores_table.find('tbody').find_all('tr')
        if len(rows) < 2: return None

        # Extract team data from table
        teamA_name = rows[0].find_all('td')[0].text.strip()
        teamA_score = float(rows[0].find_all('td')[1].text.strip())
        teamB_name = rows[1].find_all('td')[0].text.strip()
        teamB_score = float(rows[1].find_all('td')[1].text.strip())
        
        teamA_abbr = team_name_map.get(teamA_name)
        teamB_abbr = team_name_map.get(teamB_name)

        if not teamA_abbr or not teamB_abbr:
            print(f"Warning: Could not map team names in {basename} to abbreviations. Skipping.")
            return None

        # --- Match table data to filename data to assign home/away correctly ---
        if teamA_abbr == home_abbr_from_file and teamB_abbr == away_abbr_from_file:
            home_name, home_score = teamA_name, teamA_score
            away_name, away_score = teamB_name, teamB_score
        elif teamB_abbr == home_abbr_from_file and teamA_abbr == away_abbr_from_file:
            home_name, home_score = teamB_name, teamB_score
            away_name, away_score = teamA_name, teamA_score
        else:
            print(f"Warning: Teams in filename {basename} do not match teams in score table. Skipping.")
            return None

        return {
            "date": datetime.strptime(date_str, '%Y-%m-%d'),
            "home_name": home_name,
            "home_abbr": home_abbr_from_file,
            "home_schedule_name": schedule_name_map.get(home_name, home_name),
            "home_score": home_score,
            "away_name": away_name,
            "away_abbr": away_abbr_from_file,
            "away_schedule_name": schedule_name_map.get(away_name, away_name),
            "away_score": away_score,
            "file_name": basename
        }
    except Exception as e:
        print(f"Warning: Could not process file {file_path}. Error: {e}")
        return None

def generate_html(meets_by_division, year):
    """Generates the final HTML output file from the processed meet data."""
    
    # --- Calculate Standings ---
    standings = defaultdict(lambda: {'wins': 0, 'losses': 0})
    for division in meets_by_division:
        for meet in meets_by_division[division]:
            # Determine winner and loser
            winner_abbr = meet['home_abbr'] if meet['home_score'] > meet['away_score'] else meet['away_abbr']
            loser_abbr = meet['away_abbr'] if meet['home_score'] > meet['away_score'] else meet['home_abbr']
            standings[winner_abbr]['wins'] += 1
            standings[loser_abbr]['losses'] += 1

    # --- Start HTML Generation ---
    html_output = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPSA {year} Season Archive</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="apple-touch-icon" sizes="180x180" href="https://publicity.gpsaswimming.org/assets/gpsa_logo.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://publicity.gpsaswimming.org/assets/gpsa_logo.png">
    <link rel="icon" type="image/png" sizes="16x16" href="https://publicity.gpsaswimming.org/assets/gpsa_logo.png">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{ sans: ['Inter', 'sans-serif'] }},
                    colors: {{ 'gpsa-blue': '#002366', 'gpsa-blue-light': '#0033a0', 'gpsa-red': '#d9242b' }}
                }}
            }}
        }}
    </script>
</head>
<body class="font-sans bg-gray-100 text-gray-800">
    <header id="top" class="bg-gpsa-blue text-white p-4 shadow-md flex items-center justify-center">
        <img src="https://publicity.gpsaswimming.org/assets/gpsa_logo.png" alt="GPSA Logo" class="h-20 w-20 mr-4 rounded-full" crossorigin="anonymous">
        <h1 class="text-3xl md:text-5xl font-bold">GPSA {year} Season Archive</h1>
    </header>
    <div class="container mx-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-5xl mx-auto bg-white rounded-xl shadow-lg p-4 mb-8 flex justify-around">
            <a href="#red" class="text-xl font-bold text-gpsa-red hover:text-gpsa-blue transition-colors duration-300">Red Division</a>
            <a href="#white" class="text-xl font-bold text-gpsa-red hover:text-gpsa-blue transition-colors duration-300">White Division</a>
            <a href="#blue" class="text-xl font-bold text-gpsa-red hover:text-gpsa-blue transition-colors duration-300">Blue Division</a>
        </div>
"""
    # --- Loop Through Divisions to Build Tables ---
    for division_name in ['Red', 'White', 'Blue']:
        division_id = division_name.lower()
        html_output += f'<div id="{division_id}" class="max-w-5xl mx-auto bg-white rounded-xl shadow-lg p-6 mb-8 overflow-x-auto">'
        html_output += f'<h2 class="text-2xl font-bold mb-6 text-gray-700">{division_name} Division</h2>'

        # --- Meet Schedule Table ---
        html_output += '<table class="w-full border-collapse min-w-full">'
        html_output += '<thead><tr class="border-b border-black"><th class="w-1/5 p-2 text-lg bg-gpsa-red text-white text-center align-middle">DATE</th><th class="w-1/5 p-2 text-lg bg-gpsa-red text-white text-center align-middle">HOME</th><th class="w-1/12 p-2 text-lg bg-gpsa-red text-white text-center align-middle">SCORE</th><th class="w-1/5 p-2 text-lg bg-gpsa-red text-white text-center align-middle">VISITOR</th><th class="w-1/12 p-2 text-lg bg-gpsa-red text-white text-center align-middle">SCORE</th><th class="w-1/5 p-2 text-lg bg-gpsa-red text-white text-center align-middle">BEST TIMES</th></tr></thead><tbody>'
        
        # Group meets by date
        meets_grouped_by_date = defaultdict(list)
        for meet in meets_by_division.get(division_name, []):
            meets_grouped_by_date[meet['date']].append(meet)

        for date, meets_on_date in sorted(meets_grouped_by_date.items()):
            date_cell = f'<td class="p-2 text-center align-middle" rowspan="{len(meets_on_date)}">{date.strftime("%A %B %d").upper()}</td>'
            for i, meet in enumerate(meets_on_date):
                html_output += '<tr class="border-b border-black">'
                if i == 0:
                    html_output += date_cell
                
                home_score_str = f"<strong>{meet['home_score']}</strong>" if meet['home_score'] > meet['away_score'] else str(meet['home_score'])
                visitor_score_str = f"<strong>{meet['away_score']}</strong>" if meet['away_score'] > meet['home_score'] else str(meet['away_score'])

                html_output += f"<td class='p-2 text-center align-middle'>{meet['home_schedule_name']}</td>"
                html_output += f"<td class='p-2 text-center align-middle'>{home_score_str}</td>"
                html_output += f"<td class='p-2 text-center align-middle'>{meet['away_schedule_name']}</td>"
                html_output += f"<td class='p-2 text-center align-middle'>{visitor_score_str}</td>"
                html_output += f"<td class='p-2 text-center align-middle'><a href='{meet['file_name']}' target='_blank' class='text-gpsa-blue-light underline font-medium hover:text-gpsa-red'>Results</a></td>"
                html_output += '</tr>'
        html_output += '</tbody></table><div class="my-8"></div>'

        # --- Standings Table ---
        html_output += '<table class="w-full border-collapse min-w-full">'
        html_output += '<thead><tr class="border-b border-black"><th class="p-2 text-lg bg-gpsa-red text-white text-center align-middle">Team</th><th class="p-2 text-lg bg-gpsa-red text-white text-center align-middle">Win</th><th class="p-2 text-lg bg-gpsa-red text-white text-center align-middle">Loss</th></tr></thead><tbody>'
        
        division_teams = DIVISION_ASSIGNMENTS.get(division_name, [])
        # Sort teams by wins (descending)
        sorted_teams = sorted(division_teams, key=lambda abbr: standings[abbr]['wins'], reverse=True)
        
        # Find the full name from the inverted map for display
        inverted_team_map = {v: k for k, v in TEAM_NAME_MAP.items()}

        for team_abbr in sorted_teams:
            team_full_name = inverted_team_map.get(team_abbr, team_abbr)
            win_loss = standings[team_abbr]
            html_output += f"<tr class='border-b border-black'><td class='p-2 text-left align-middle'>{team_abbr} &ndash; {team_full_name}</td><td class='p-2 text-center align-middle'>{win_loss['wins']}</td><td class='p-2 text-center align-middle'>{win_loss['losses']}</td></tr>"
        html_output += '</tbody></table>'
        html_output += '<div class="mt-6 flex justify-end"><a href="#top" class="text-gpsa-blue-light hover:text-gpsa-red font-medium">Back to Top &uarr;</a></div></div>'

    html_output += '</div></body></html>'
    return html_output

def main():
    """Main function to process a directory of meet files and generate an archive."""
    parser = argparse.ArgumentParser(description="Generate a GPSA season archive from a directory of meet result files.")
    parser.add_argument('input_dir', type=str, help='The path to the directory containing meet result HTML files.')
    parser.add_argument('year', type=int, help='The season year for the archive (e.g., 2024).')
    args = parser.parse_args()

    # Invert the division map for easy lookup
    team_to_division = {team: division for division, teams in DIVISION_ASSIGNMENTS.items() for team in teams}

    all_meets = []
    for filename in os.listdir(args.input_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(args.input_dir, filename)
            meet_data = parse_meet_file(file_path, TEAM_NAME_MAP, TEAM_SCHEDULE_NAME_MAP, FILENAME_ABBR_MAP)
            if meet_data:
                # Assign division based on the home team
                division = team_to_division.get(meet_data['home_abbr'])
                if division:
                    meet_data['division'] = division
                    all_meets.append(meet_data)

    # Group meets by division
    meets_by_division = defaultdict(list)
    for meet in all_meets:
        meets_by_division[meet['division']].append(meet)
    
    # Sort meets within each division by date
    for division in meets_by_division:
        meets_by_division[division].sort(key=lambda x: x['date'])

    # Generate and save the final HTML file
    final_html = generate_html(meets_by_division, args.year)
    output_filename = f"gpsa_{args.year}_season_archive.html"
    with open(output_filename, "w", encoding='utf-8') as file:
        file.write(final_html)
    
    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    main()
