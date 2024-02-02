"""
Given a set name, generate a cue file.

Args: Set file name

Outputs: {set file name}.cue file with cue points to processed-files dir
"""

from os.path import basename, splitext
import sys

from constants import PROCESSED_FILES_DIR, VDJ_DB_FILE, DJ_NAME
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


def generate_cue_text_from_cues(song_data):
    """Find cues in the song data and generate text in CUE file format"""
    text_data = ""

    # Write Header
    text_data += f'PERFORMER "{DJ_NAME}"\n'
    text_data += f'TITLE "{set_title}"\n'
    text_data += f'FILE "{set_file}"\n'

    cue_points = filter(cue_filter, song_data["Poi"])

    for cue in cue_points:
        cue_number = cue.get("@Num", "0").zfill(2)

        if len(cue.get("@Name", "").split(" - ")) == 2:
            performer, title = cue.get("@Name", " - ").split(" - ")
        else:
            print(f"Bad cue point found at [{cue_number}]: f{cue.get('@Name')}")
            title = cue.get("@Name", "Unknown")
            performer = "Unknown"
        timestamp = seconds_to_minutes_and_seconds(cue.get("@Pos", "0"))

        text_data += f"  TRACK {cue_number} AUDIO\n"
        text_data += f'    TITLE "{title}"\n'
        text_data += f'    PERFORMER "{performer}"\n'
        text_data += f"    INDEX 01 {timestamp}\n"

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

    print(f"Generating CUE file text for {len(song_data)} cue points ...")
    cue_text = generate_cue_text_from_cues(song_data)

    # Write a CUE file, named after the original recorded file.
    output_file = f"{PROCESSED_FILES_DIR}/{set_title}.cue"

    with open(output_file, "w") as cue_file:
        cue_file.write(cue_text)
        print(f"Wrote CUE file to {output_file}")
