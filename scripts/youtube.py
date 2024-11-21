"""
Scripts and functions for YouTube.

Args: Set file name

Output a YouTube chapter text file of the format:

```
mm:ss   Artist Name - Song Name
```
"""

from os.path import splitext
from pathlib import Path
import sys

from config import PROCESSED_FILES_DIR, VDJ_DB_FILE, DJ_NAME
from formatters import seconds_to_minutes_and_seconds
from virtualdj import find_song_from_database, cue_filter
from utils import read_from_xml


def youtube_chapter_format(cue_points, set_metadata):
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
        timestamp = seconds_to_minutes_and_seconds(
            cue.get("@Pos", "0"), milliseconds=False
        )

        text_data += f"{timestamp}\t{performer} - {title}\n"

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

    # Write YouTube chapter format
    youtube_chapters_file_name = f"{Path(set_file).stem}.txt"
    print(f"Generating YouTube chapters:\t{youtube_chapters_file_name}")
    youtube_chapters_text = youtube_chapter_format(cue_points, set_metadata)

    # Write file to the processed_files directory
    output_file_path = Path(PROCESSED_FILES_DIR, youtube_chapters_file_name)
    with open(output_file_path, "w") as output_file:
        output_file.write(youtube_chapters_text)
        print(f"Wrote file:\t\t\t{output_file_path}")
