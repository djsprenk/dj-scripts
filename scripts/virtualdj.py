"""
Scripts for dealing with VirtualDJ's database.
Running the script from the command line will convert XML database to JSON.
"""

import json
from os.path import basename

from config import JSON_DB_FILE, VDJ_DB_BACKUP_DIR, VDJ_DB_FILE, VDJ_EXPORT_DIR
from utils import get_latest_file_with_extension, read_from_xml, unzip_file


def cue_filter(elem):
    """Filter function for returning cue points"""
    return elem.get("@Type") == "cue"


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


def get_songs_from_database(database):
    """Get a list of all songs from the database"""
    return database["VirtualDJ_Database"]["Song"]


def find_song_from_database(database, file_name):
    """Find a matching song from the database by file name"""

    songs = get_songs_from_database(database)

    for song in songs:
        if basename(song.get("@FilePath")) == file_name:
            return song


if __name__ == "__main__":

    # Get the latest VDJ database backup from the VDJ_DB_BACKUP_DIR, unzip, and convert to JSON
    print(f"Fetching latest VDJ database export from {VDJ_DB_BACKUP_DIR}")
    vdj_database_backup_zip = get_latest_file_with_extension(VDJ_DB_BACKUP_DIR, "zip")
    print(f"Found backup: {vdj_database_backup_zip.name}")

    unzip_path = VDJ_EXPORT_DIR
    print(f"Unzipping file to: {unzip_path}")
    unzip_file(vdj_database_backup_zip, unzip_path)

    print("Converting VDJ database to JSON...")
    database_to_json()

    print("DONE")
