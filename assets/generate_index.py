import os
import sys
import argparse
import html

# --- Configuration ---
# The name of the output HTML file.
OUTPUT_FILE = "index.html"
# The title for the generated HTML page.
PAGE_TITLE = "Directory Listing"
# The absolute URL for the centralized stylesheet.
STYLESHEET_URL = "https://publicity.gpsaswimming.org/assets/directory.css"
# List of directory names to exclude from indexing.
EXCLUDE_DIRS = ['.git', 'scripts']

def generate_index_for_single_directory(current_path, subdirs, files):
    """
    Generates an index.html file for a single directory.

    Args:
        current_path (str): The path to the directory where the index file will be created.
        subdirs (list): A list of visible subdirectory names in current_path.
        files (list): A list of visible file names in current_path.
    """
    try:
        # Get the directory name for the page heading
        dir_name = os.path.basename(os.path.abspath(current_path))
        
        # Combine subdirectories and files, then sort alphabetically
        all_items = sorted(subdirs + files, key=str.lower)

        # Filter out the index.html file itself from the list
        all_items = [item for item in all_items if item != OUTPUT_FILE]

        # Start building the HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(PAGE_TITLE)} - {html.escape(dir_name)}</title>
  <link rel="stylesheet" href="{STYLESHEET_URL}">
</head>
<body>
  <div class="container">
    <h1><span class="logo">🏊</span>{html.escape(PAGE_TITLE)}: {html.escape(dir_name)}</h1>
    <ul>
"""
        # Generate list items for each file/directory
        if not all_items:
            html_content += "      <li>No other files found in this directory.</li>\n"
        else:
            for item_name in all_items:
                escaped_item = html.escape(item_name)
                
                # Check if the item is a directory (it will be in the subdirs list)
                if item_name in subdirs:
                    icon = "📁"
                    link_target = f"{escaped_item}/"
                else:
                    icon = "📄"
                    link_target = escaped_item
                
                html_content += f"      <li><a href='{link_target}'><span class='icon'>{icon}</span>{escaped_item}</a></li>\n"

        # Finish the HTML content
        html_content += """    </ul>
  </div>
</body>
</html>"""

        # Write the content to the HTML file in the current directory
        output_file_path = os.path.join(current_path, OUTPUT_FILE)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Index generated for: '{output_file_path}'")

    except Exception as e:
        print(f"❌ An error occurred while processing {current_path}: {e}")

def crawl_and_index(root_path):
    """
    Recursively walks through a directory tree and generates an index file in each subdirectory.

    Args:
        root_path (str): The root directory to start crawling from.
    """
    if not os.path.isdir(root_path):
        print(f"❌ Error: The specified root path '{root_path}' is not a valid directory.")
        sys.exit(1)

    print(f"🚀 Starting crawl from '{os.path.abspath(root_path)}'...")

    for current_path, dir_names, file_names in os.walk(root_path, topdown=True):
        # Modify dir_names in-place to prevent os.walk from traversing into excluded or hidden directories
        dir_names[:] = [d for d in dir_names if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        # Filter out hidden files from the file_names list
        visible_files = [f for f in file_names if not f.startswith('.')]
        
        generate_index_for_single_directory(current_path, dir_names, visible_files)
    
    print("\n✨ Crawl complete!")

def main():
    """
    Main function to parse command-line arguments and run the indexer.
    """
    parser = argparse.ArgumentParser(
        description="A script to recursively generate an index.html file for a directory and its subdirectories.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "folder_path",
        help="The root path of the folder to crawl and index."
    )
    
    args = parser.parse_args()
    crawl_and_index(args.folder_path)

if __name__ == "__main__":
    main()
