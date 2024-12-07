# Markdown Cover URL Updater

This repository provides two Python scripts, `fix.py` and `fix_without_download.py`, to manage and update cover URLs in markdown files. These scripts are specifically designed to work with a directory of markdown files used for tracking video games.

![](.img/playing.png)

## Files

### 1. `fix.py`  
**Purpose:**  
Validates existing cover URLs by checking their image dimensions, updates invalid or missing URLs, and marks files as manually set if skipped.

**Key Features:**
- Downloads images from provided cover URLs and verifies dimensions.
- Opens a search URL for the title on **SteamGridDB** if no valid cover URL is present.
- Allows the user to:
  - Input a new cover URL.
  - Skip the file (marks the file with `coverManuallySet: true`).
- Adds `coverManuallySet: true` to the metadata when a file is updated or skipped.

**Usage:**
```bash
python3 fix.py
```

---

### 2. `fix_without_download.py`  
**Purpose:**  
Updates or adds cover URLs without checking image dimensions. Marks skipped files as manually set.

**Key Features:**
- Opens a search URL for the title on **SteamGridDB** if no cover URL is present.
- Allows the user to:
  - Input a new cover URL.
  - Skip the file (marks the file with `coverManuallySet: true`).
- Adds `coverManuallySet: true` to the metadata when a file is updated or skipped.

**Usage:**
```bash
python3 fix_without_download.py
```

---

## Directory Structure
The scripts process markdown files under the directory:
```bash
~/obsidian/brain/03 - Resources/Video Games/Backlog
```

You can modify the `backlog_dir` variable in the scripts to point to a different directory.

---

## Metadata Format in Markdown Files
Each markdown file is expected to have a YAML metadata section at the top. Example:

```yaml
---
title: "Game Title"
coverUrl: "https://example.com/image.jpg"
coverManuallySet: true
---
```

- `title`: The name of the game.
- `coverUrl`: The URL for the cover image.
- `coverManuallySet`: Indicates that the cover URL was manually set or the file was skipped.

---

## Notes
- Both scripts rely on user interaction for setting new cover URLs.
- For skipping files, `coverManuallySet: true` is automatically added to prevent reprocessing.
- **`fix.py`** includes additional functionality to validate image dimensions, while **`fix_without_download.py`** only updates the metadata without validation.

