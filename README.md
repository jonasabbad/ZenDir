# ZenDir

ZenDir is a lightweight, automated file organizer that scans a target directory, categorizes files based on their extensions, moves them into appropriate subfolders, and automatically compresses extremely large files to save space.

<div align="center">
  <a href="https://www.buymeacoffee.com/jonasabbad" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</div>

## Features
- **Dynamic Extension Mapping:** Sorts files into intuitive folders like Images, Documents, Archives, Code, Media, and Others based on extensions.
- **External Configuration:** Uses an easily editable `config.json` file to manage categorizations. The tool auto-generates a default config on its first run if it doesn't exist.
- **Large File Compression:** Automatically detects files larger than 50MB (that aren't already archives), compresses them into `.zip` format using built-in Python `zipfile`, and safely deletes the original file before moving it to the Archives folder.
- **Professional Logging:** Outputs clear, timestamped logs using Python's `logging` module indicating every move, compression, and any errors encountered via CLI interface.
- **Robust Error Handling:** Employs `try-except` blocks around file operations to smoothly skip files that are in use or inaccessible, ensuring the script runs without crashing.

## Installation

1. Clone this repository (or download the source code):
   ```bash
   git clone https://github.com/yourusername/zendir.git
   ```
2. Navigate to the project directory:
   ```bash
   cd zendir
   ```
3. *Optional*: ZenDir relies strictly on Python standard libraries, meaning no additional `pip install` commands are required! Ensure you have **Python 3.6+** installed.

## Usage

Use the command-line interface to organize a target directory. Provide the path using the `-p` or `--path` argument.

```bash
python zendir.py -p /path/to/your/messy/folder
```

On Windows, you can use:
```bash
python zendir.py -p "C:\Users\username\Downloads"
```

### Configuration

On its first run (or if manually configured), ZenDir looks for a `config.json` file in the same directory as the script. You can edit this file to add new extensions or customize folder names. The default structure looks like this:

```json
{
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".md"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rs", ".php", ".sh", ".bat", ".json", ".xml", ".yaml", ".yml", ".sql"],
    "Media": [".mp3", ".wav", ".ogg", ".flac", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm"],
    "Others": []
}
```

## How It Works
1. **Scanning:** ZenDir looks at every file directly inside the target directory. Subdirectories are ignored.
2. **Compression:** If a file is over 50MB and not in the Archives category, it is automatically zipped inplace. The original file is removed.
3. **Categorizing:** The `config.json` is assessed for the file's matching extension folder. If the file was just compressed into a zip, it gets cataloged dynamically as an Archive.
4. **Moving:** The file (or its compressed `.zip` version) is moved to the corresponding category folder. If a file with the same name already exists in the destination folder, the tool appends a counter to prevent overwriting existing data.
