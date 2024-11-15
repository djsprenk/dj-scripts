"""
Config used across multiple files.
Overwrite by
"""

import os
from pathlib import Path

# Load any private settings from .env file
from dotenv import load_dotenv

load_dotenv()

# Constants with defaults
OS_USERNAME = os.getenv("USER")
DJ_NAME = os.getenv("DJ_NAME", "Unknown")

# Directories with defaults
VDJ_DB_BACKUP_DIR = Path(
    os.getenv(
        "VDJ_DB_BACKUP_DIR", Path("/Users", OS_USERNAME, "Documents/VirtualDJ/Backup")
    )
)
VDJ_EXPORT_DIR = os.getenv("VDJ_EXPORT_DIR", "vdj-export")
PROCESSED_FILES_DIR = os.getenv("PROCESSED_FILES_DIR", "processed-files")

# Files with default
VDJ_DB_FILE = os.getenv("VDJ_DB_FILE", f"{VDJ_EXPORT_DIR}/database.xml")
JSON_DB_FILE = os.getenv("JSON_DB_FILE", f"{PROCESSED_FILES_DIR}/database.json")
