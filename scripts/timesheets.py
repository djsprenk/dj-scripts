"""
Generate timesheets for all available formats.

Args: Set file name

Outputs:
- CUE file
- YouTube chapter text file
"""

from os.path import splitext
import sys

from config import PROCESSED_FILES_DIR, VDJ_DB_FILE, DJ_NAME
from cuefile import cue_file_format
from youtube import youtube_chapter_format
from virtualdj import find_song_from_database, cue_filter
from utils import read_from_xml

AVAILABLE_FORMATS = ["cue", "youtube"]

if __name__ == "__main__":

    # If there is only only one arg, it should be the set title.
    # We will generate all available formats by default
    if len(sys.argv) < 2:
        print(f"Expected at least 1 arg: set file name")
        exit(1)
    if len(sys.argv) == 2:
        set_file = sys.argv[1]
        set_title = splitext(set_file)[0]
        output_formats = AVAILABLE_FORMATS

    # We can use flags to specify the output formats
    if len(sys.argv) > 2:
        set_file = sys.argv[-1]
        set_title = splitext(set_file)[0]

        flags = sys.argv[:-1]

        output_formats = []

        if "-a" in flags:
            output_formats = AVAILABLE_FORMATS
        else:
            if "-c" in flags:
                output_formats.append("cue")
            if "-y" in flags:
                output_formats.append("youtube")

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
        "set_title": set_title,
        "set_file": set_file,
    }

    # Find cue points for the set
    cue_points = [*filter(cue_filter, song_data["Poi"])]
    print(f"Found {len(cue_points)} POIs ...")

    files = []

    # Generate timesheets for each selected format
    if "cue" in output_formats:
        cue_file_name = f"{set_title}.cue"
        print(f"Generating CUE sheet:\t\t{cue_file_name}")
        cue_data = cue_file_format(cue_points, set_metadata)
        files.append({"file_name": cue_file_name, "file_data": cue_data})

    if "youtube" in output_formats:
        youtube_chapters_file_name = f"{set_title}.txt"
        print(f"Generating YouTube chapters:\t{youtube_chapters_file_name}")
        youtube_chapters_text = youtube_chapter_format(cue_points, set_metadata)
        files.append(
            {
                "file_name": youtube_chapters_file_name,
                "file_data": youtube_chapters_text,
            }
        )

    # Write files to the processed_files directory
    for file in files:
        output_file_path = f"{PROCESSED_FILES_DIR}/{file['file_name']}"

        with open(output_file_path, "w") as output_file:
            output_file.write(file["file_data"])
            print(f"Wrote file:\t\t\t{output_file_path}")
