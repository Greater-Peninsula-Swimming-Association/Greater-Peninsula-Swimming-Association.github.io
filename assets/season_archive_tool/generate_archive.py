import argparse
from bs4 import BeautifulSoup

def get_soup_from_file(file_path):
    """Reads an HTML file from the local disk and returns a BeautifulSoup object."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return BeautifulSoup(f, 'html.parser')
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def main():
    """Main function to parse a local HTML file and generate the archive."""
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Parse a local GPSA HTML file and generate an archive.")
    parser.add_argument('input_file', type=str, help='The path to the input HTML file.')
    parser.add_argument('year', type=int, help='The season year for the archive (e.g., 2025).')
    args = parser.parse_args()
    
    year = args.year
    input_file = args.input_file

    soup = get_soup_from_file(input_file)

    if not soup:
        return

    # Start building the HTML output using the provided year
    html_output = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPSA {year} Season Archive</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="apple-touch-icon" sizes="180x180" href="https://d1nmxxg9d5tdo.cloudfront.net/875/files/apple-touch-icon.png?1651502524">
    <link rel="icon" type="image/png" sizes="32x32" href="https://d1nmxxg9d5tdo.cloudfront.net/875/files/favicon-32x32.png?1651502547">
    <link rel="icon" type="image/png" sizes="16x16" href="https://d1nmxxg9d5tdo.cloudfront.net/875/files/favicon-16x16.png?1651502535">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'sans-serif'],
                    }},
                    colors: {{
                        'gpsa-blue': '#002366',
                        'gpsa-blue-light': '#0033a0',
                        'gpsa-red': '#d9242b',
                    }}
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

    # A more robust way to find and process division data.
    # First, find all the h3 tags that act as division titles.
    division_headers = soup.find_all('h3')

    for header in division_headers:
        division_name = header.text.strip()
        
        # Process only if it's a division header
        if "Division" not in division_name:
            continue

        # Find the parent container for the meet schedule
        meet_schedule_div = header.find_parent('div', class_='html_snippet')
        if not meet_schedule_div:
            continue

        # The standings div is typically the next sibling div
        standings_div = meet_schedule_div.find_next_sibling('div')
        if not standings_div:
            continue

        division_id = division_name.lower().replace(" division", "")

        html_output += f'<div id="{division_id}" class="max-w-5xl mx-auto bg-white rounded-xl shadow-lg p-6 mb-8 overflow-x-auto">'
        html_output += f'<h2 class="text-2xl font-bold mb-6 text-gray-700">{division_name}</h2>'

        # Process meet schedule table
        meet_table = meet_schedule_div.find('table')
        if meet_table:
            html_output += '<table class="w-full border-collapse min-w-full">'
            for row in meet_table.find_all('tr'):
                html_output += '<tr class="border-b border-black">'
                for th in row.find_all('th'):
                    html_output += '<th class="w-1/5 p-2 text-lg bg-gpsa-red text-white text-center align-middle">{}</th>'.format(th.text.strip())
                for td in row.find_all('td'):
                    rowspan = td.get('rowspan')
                    content = ""
                    if td.find('a'):
                        link = td.find('a')
                        # Ensure href exists to prevent errors
                        href = link.get('href', '#')
                        content = f'<a href="{href}" target="_blank" class="text-gpsa-blue-light underline font-medium hover:text-gpsa-red">{link.text.strip()}</a>'
                    elif td.find('strong'):
                        content = f'<strong>{td.find("strong").text.strip()}</strong>'
                    else:
                        content = td.text.strip()
                    
                    if rowspan:
                        html_output += f'<td class="p-2 text-center align-middle" rowspan="{rowspan}">{content}</td>'
                    else:
                        html_output += f'<td class="p-2 text-center align-middle">{content}</td>'
                html_output += '</tr>'
            html_output += '</table>'
            html_output += '<div class="my-8"></div>'

        # Process standings table
        standings_table = standings_div.find('table')
        if standings_table:
            html_output += '<table class="w-full border-collapse min-w-full">'
            for row in standings_table.find_all('tr'):
                html_output += '<tr class="border-b border-black">'
                for th in row.find_all('th'):
                    html_output += '<th class="p-2 text-lg bg-gpsa-red text-white text-center align-middle">{}</th>'.format(th.text.strip())
                for i, td in enumerate(row.find_all('td')):
                    if i == 0: # Team name column
                        html_output += f'<td class="p-2 text-left align-middle">{td.text.strip()}</td>'
                    else: # Win/Loss columns
                        html_output += f'<td class="p-2 text-center align-middle">{td.text.strip()}</td>'

                html_output += '</tr>'
            html_output += '</table>'
        
        html_output += '<div class="mt-6 flex justify-end"><a href="#top" class="text-gpsa-blue-light hover:text-gpsa-red font-medium">Back to Top &uarr;</a></div>'
        html_output += '</div>'


    html_output += """
    </div>
</body>
</html>
"""

    # Save the generated HTML to a file with the dynamic year
    filename = f"gpsa_{year}_season_archive.html"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(html_output)

    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    main()
