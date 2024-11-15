"""
Scripts for dealing with VirtualDJ's database.
Running the script from the command line will convert XML database to JSON.
"""

import json
import zipfile

from config import JSON_DB_FILE, VDJ_DB_BACKUP_DIR, VDJ_DB_FILE, VDJ_EXPORT_DIR
from utils import read_from_xml


def database_to_json():
    """Convert XML database to JSON database."""

    # Read database from XML
    data_dict = read_from_xml(VDJ_DB_FILE)

    # generate the object using json.dumps() corresponding to json data
    json_data = json.dumps(data_dict)

    # Write data to JSON file
    with open(JSON_DB_FILE, "w", encoding="utf-8") as json_file:
        print(f"Writing data to {JSON_DB_FILE}")
        json_file.write(json_data)
        json_file.close()


def get_latest_file_with_extension(dir_path, extension):
    """Get most recent file from directory."""
    files = list(dir_path.glob(f"*.{extension}"))

    if not files:
        raise FileNotFoundError(f"No {extension} files found in the directory.")

    # Find the most recent zip file
    most_recent_file = max(files, key=lambda p: p.stat().st_mtime)
    return most_recent_file


def unzip_file(zip_path, extract_to):
    # Unzip the file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


if __name__ == "__main__":
    print(f"Fetching latest VDJ database export from {VDJ_DB_BACKUP_DIR}")

    vdj_database_backup_zip = get_latest_file_with_extension(VDJ_DB_BACKUP_DIR, "zip")

    print(f"Found backup: {vdj_database_backup_zip.name}")

    unzip_path = VDJ_EXPORT_DIR
    print(f"Unzipping file to: {unzip_path}")
    unzip_file(vdj_database_backup_zip, unzip_path)

    print("Converting VDJ database to JSON...")
    database_to_json()

    print("DONE")
