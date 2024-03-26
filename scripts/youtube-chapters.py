"""
Given a set name, generate a cue file.

Args: Set file name

Outputs: {set file name}.cue file with cue points to processed-files dir
"""

from os.path import basename, splitext
import sys

from constants import PROCESSED_FILES_DIR, VDJ_DB_FILE
from utils import read_from_xml
from formatters import seconds_to_minutes_and_seconds


def cue_filter(elem):
    """Filter function for returning cue points"""
    return elem.get("@Type") == "cue"


def get_songs_from_database(database):
    """Get a list of all songs from the database"""
    return database["VirtualDJ_Database"]["Song"]


def find_song_from_database(database, file_name):
    """Find a matching song from the database by file name"""

    songs = get_songs_from_database(database)

    for song in songs:
        if basename(song.get("@FilePath")) == file_name:
            return song


def generate_chapters_from_song_data(cue_points):
    """Create YouTube chapter list output for a list of cue points"""
    text_data = ""

    # Write Header
    text_data += "Songs:\n"

    for cue in cue_points:
        cue_number = cue.get("@Num", "0").zfill(2)

        if len(cue.get("@Name", "").split(" - ")) == 2:
            performer, title = cue.get("@Name", " - ").split(" - ")
        else:
            print(f"Bad cue point found at [{cue_number}]: f{cue.get('@Name')}")
            title = cue.get("@Name", "Unknown")
            performer = "Unknown"
        timestamp = seconds_to_minutes_and_seconds(cue.get("@Pos", "0"), milliseconds=False)

        text_data += f"{timestamp}\t{performer} - {title}\n"

    return text_data


if __name__ == "__main__":

    # Get set from args
    if len(sys.argv) == 2:
        set_file = sys.argv[1]
        set_title = splitext(set_file)[0]
    else:
        print(f"Expected 1 arg: set file name")
        exit(1)

    # Convert XML database dump to JSON
    print(f"Reading data from {VDJ_DB_FILE} ...")
    database = read_from_xml(VDJ_DB_FILE)

    # Find sets from database dump
    print(f"Searching for entry for {set_file} ...")
    song_data = find_song_from_database(database, set_file)

    if song_data is None:
        print(f"No set found in database for file {set_file}")
        exit(1)

    # Find cue points for the set
    cue_points = filter(cue_filter, song_data["Poi"])

    # Generate timesheet in YouTube chapter format
    print(f"Generating chapters for {len(song_data)} cue points ...")
    chapters = generate_chapters_from_song_data(cue_points)

    # Write a CUE file, named after the original recorded file.
    output_file = f"{PROCESSED_FILES_DIR}/{set_title}.txt"

    with open(output_file, "w") as text_file:
        text_file.write(chapters)
        print(f"Wrote chapters to {output_file}")
