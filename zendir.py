#!/usr/bin/env python3
"""
ZenDir - Automated File Organizer
"""

import os
import sys
import json
import shutil
import zipfile
import logging
import argparse
from pathlib import Path

# Setup professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ZenDir")

CONFIG_FILENAME = 'config.json'
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50 MB

DEFAULT_CONFIG = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".md"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rs", ".php", ".sh", ".bat", ".json", ".xml", ".yaml", ".yml", ".sql"],
    "Media": [".mp3", ".wav", ".ogg", ".flac", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm"],
    "Others": []
}

def load_or_create_config() -> dict:
    """
    Reads the config.json file next to the script.
    If it doesn't exist, automatically generates a default one.
    """
    config_path = Path(__file__).parent / CONFIG_FILENAME
    
    if not config_path.exists():
        logger.info(f"Configuration file not found. Generating default {CONFIG_FILENAME}.")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to create default configuration file: {e}")
            return DEFAULT_CONFIG
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read {CONFIG_FILENAME}. Using default configuration. Error: {e}")
        return DEFAULT_CONFIG

def get_category(extension: str, config: dict) -> str:
    """Determine the category folder for a given extension."""
    extension = extension.lower()
    for category, extensions in config.items():
        if extension in extensions:
            return category
    return "Others"

def organize_directory(target_path: Path, config: dict):
    """
    Scans the target directory, compresses large files, 
    and sorts files into subfolders based on the config.
    """
    if not target_path.exists() or not target_path.is_dir():
        logger.error(f"The path '{target_path}' is invalid or not a directory.")
        return

    logger.info(f"Starting organization of '{target_path}'")

    for file_path in target_path.iterdir():
        # Only process files
        if not file_path.is_file():
            continue
            
        # Do not process the config file if organizing the script directory
        if file_path.name == CONFIG_FILENAME:
            continue
            
        try:
            category = get_category(file_path.suffix, config)
            file_size = file_path.stat().st_size
            is_large = file_size > LARGE_FILE_THRESHOLD
            is_archive = category == "Archives"

            # 1. Compress Large Files
            if is_large and not is_archive:
                zip_filename = file_path.with_suffix(file_path.suffix + '.zip').name
                zip_path = file_path.parent / zip_filename
                
                try:
                    logger.info(f"Compressing large file: {file_path.name} ({file_size / 1024 / 1024:.2f} MB)")
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(file_path, arcname=file_path.name)
                    
                    if zip_path.exists():
                        file_path.unlink() # Safely delete the original file
                        logger.info(f"Successfully compressed and deleted original: {file_path.name}")
                        
                        # Update references so the zip file is pushed to Archives
                        file_path = zip_path
                        category = "Archives"
                    else:
                        raise FileNotFoundError("Zip file was not created successfully.")
                except Exception as e:
                    logger.error(f"Failed to compress file {file_path.name}: {e}")
                    # Cleanup partial zip file if compression failed
                    if zip_path.exists():
                        try:
                            zip_path.unlink()
                        except:
                            pass
            
            # 2. Moving the file
            category_dir = target_path / category
            if not category_dir.exists():
                category_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created category folder: {category}")

            destination = category_dir / file_path.name
            
            # Handle name collisions by adding a counter
            counter = 1
            while destination.exists():
                destination = category_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1

            shutil.move(str(file_path), str(destination))
            logger.info(f"Moved: {file_path.name} -> {category}/")

        except PermissionError:
            logger.error(f"Permission denied: {file_path.name} (File might be in use)")
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")

    logger.info("Organization complete.")

def main():
    parser = argparse.ArgumentParser(description="ZenDir - Lightweight Automated File Organizer")
    parser.add_argument(
        '-p', '--path', 
        type=str, 
        required=True, 
        help="Target directory to organize"
    )
    
    args = parser.parse_args()
    target_path = Path(args.path).resolve()
    
    config = load_or_create_config()
    organize_directory(target_path, config)

if __name__ == "__main__":
    main()
