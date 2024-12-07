import os
import re
import subprocess
import requests
from PIL import Image
from io import BytesIO

def download_and_check_image(url):
    """Download an image and check its dimensions."""
    try:
        print(f"Downloading and checking image: {url}")
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img.size  # Returns (width, height)
    except Exception as e:
        print(f"Error downloading or processing image: {e}")
        return None

def update_cover_urls(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                title = None
                cover_url_exists = False
                cover_manually_set = False
                cover_url = None
                
                for line in lines:
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("coverUrl:"):
                        cover_url_exists = True
                        cover_url = line.split(":", 1)[1].strip().strip('"')
                        if cover_url == "N/A":
                            cover_url_exists = False
                    elif line.startswith("coverManuallySet: true"):
                        cover_manually_set = True

                if cover_manually_set:
                    print(f"Skipping file {file} as 'coverManuallySet: true' is present.")
                    continue

                if cover_url_exists and cover_url:
                    print(f"Checking image dimensions for cover URL in {file}...")
                    dimensions = download_and_check_image(cover_url)
                    if dimensions and dimensions in [(460, 215), (920, 430)]:
                        print(f"Image dimensions are valid ({dimensions[0]}×{dimensions[1]}) for {file}.")
                        continue  # Skip updating this file
                    else:
                        print(f"Image dimensions invalid or not acceptable for {file}.")
                        cover_url_exists = False  # Trigger update process

                if not cover_url_exists:
                    if title:
                        print(f"Processing file: {file}")
                        print(f"Title found: {title}")
                        search_url = f"https://www.steamgriddb.com/search/grids?term={title.replace(' ', '+')}"
                        subprocess.run(["xdg-open", search_url])

                        new_cover_url = input("Enter new cover URL (or type 'q' to quit, 's' to skip): ").strip()
                        if new_cover_url.lower() == 'q':
                            print("Quitting program.")
                            return
                        elif new_cover_url.lower() == 's':
                            print(f"Skipping file: {file}")
                            # Add 'coverManuallySet: true' to the file
                            new_lines = []
                            cover_manually_set_line = "coverManuallySet: true\n"
                            added_cover_manually_set = False

                            for i, line in enumerate(lines):
                                new_lines.append(line)
                                if line.strip() == "---" and not added_cover_manually_set and i > 0:
                                    # Add 'coverManuallySet: true' before the second "---"
                                    new_lines.insert(i, cover_manually_set_line)
                                    added_cover_manually_set = True
                                    break

                            if not added_cover_manually_set:
                                # If somehow no second "---" found, append it at the end of metadata
                                new_lines.append(cover_manually_set_line)

                            # Write the updated content back to the file
                            with open(file_path, 'w') as f:
                                f.writelines(new_lines)

                            print(f"Marked 'coverManuallySet: true' in {file}")
                            continue
                        
                        if new_cover_url:
                            new_lines = []
                            cover_url_line = f'coverUrl: "{new_cover_url}"\n'
                            cover_manually_set_line = "coverManuallySet: true\n"
                            added_cover_url = False

                            for i, line in enumerate(lines):
                                new_lines.append(line)
                                if line.strip() == "---" and not added_cover_url and i > 0:
                                    # Add coverUrl and coverManuallySet before the second "---"
                                    new_lines.insert(i, cover_url_line)
                                    new_lines.insert(i + 1, cover_manually_set_line)
                                    added_cover_url = True
                                    break
                            
                            if not added_cover_url:
                                # If somehow no second "---" found, append it at the end of metadata
                                new_lines.append(cover_url_line)
                                new_lines.append(cover_manually_set_line)

                            # Write the updated content back to the file
                            with open(file_path, 'w') as f:
                                f.writelines(new_lines)
                            
                            print(f"Updated cover URL and added 'coverManuallySet: true' in {file}")
                        else:
                            print("No URL entered, skipping update.")
                    else:
                        print(f"No title found in {file}, skipping.")
    print("Completed processing all files.")

# Define the directory to scan
backlog_dir = os.path.expanduser("~/obsidian/brain/03 - Resources/Video Games/Backlog")
update_cover_urls(backlog_dir)

