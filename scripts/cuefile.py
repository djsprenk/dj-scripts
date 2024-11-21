"""
Given a set name, generate timesheets in selected formats

Args: Set file name

Outputs:
- CUE file
- YouTube chapter text file
"""

from os.path import basename, splitext
from pathlib import Path
import sys

from config import PROCESSED_FILES_DIR, VDJ_DB_FILE, DJ_NAME
from virtualdj import cue_filter, find_song_from_database
from utils import read_from_xml
from formatters import seconds_to_minutes_and_seconds


def cue_file_format(cue_points, set_metadata):
    """Create CUE file output for a list of cue points"""
    text_data = ""

    # Write Header
    text_data += f'PERFORMER "{set_metadata["dj_name"]}"\n'
    text_data += f'TITLE "{set_metadata["set_title"]}"\n'
    text_data += f'FILE "{set_metadata["set_file"]}"\n'

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
    # We expect 1 argument (after script name), the set file name
    if len(sys.argv) < 2:
        print(f"Expected 1 argument: set file name")
        exit(1)
    set_file = sys.argv[-1]

    # Convert XML database dump to JSON
    print(f"Reading data from {VDJ_DB_FILE} ...")
    database = read_from_xml(VDJ_DB_FILE)

    # Find sets from database dump
    print(f"Searching for entry for {set_file} ...")
    song_data = find_song_from_database(database, set_file)
    if song_data is None:
        print(f"No set found in database for file {set_file}")
        exit(1)

    # Package relevant metadata about the set
    set_metadata = {
        "dj_name": DJ_NAME,
        "set_title": song_data.get("Tags", {}).get("@Title", Path(set_file).stem),
        "set_file": set_file,
    }

    # Find cue points for the set
    cue_points = [*filter(cue_filter, song_data["Poi"])]
    print(f"Found {len(cue_points)} POIs ...")

    # Write CUE file format
    cue_file_name = f"{Path(set_file).stem}.cue"
    print(f"Generating CUE sheet:\t\t{cue_file_name}")
    cue_file_data = cue_file_format(cue_points, set_metadata)

    # Write file to the processed_files directory
    output_file_path = Path(PROCESSED_FILES_DIR, cue_file_name)
    with open(output_file_path, "w") as output_file:
        output_file.write(cue_file_data)
        print(f"Wrote file:\t\t\t{output_file_path}")
