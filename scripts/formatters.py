"""Different formatters for time, BPM, etc."""

from math import floor


def bpm_formatter(database):
    for song in database["VirtualDJ_Database"]["Song"]:
        bpm = song.get("Tags", {}).get("@Bpm")
        yield song


def bpm_format(spb):
    """
    Beats per minute (BPM) is actually saved as a seconds per beat (SPB) float.
    Convert to the more standard BPM with one decimal precision or empty string.
    """
    if not spb:
        return ""

    return round(60 / float(spb), 1)


def seconds_to_hours_minutes_and_seconds(seconds, leading_hour=False):
    """
    Convert seconds to formatted hh:mm:ss string or empty
    """
    if not seconds:
        return ""
    m, s = divmod(int(float(seconds)), 60)
    h, m = divmod(m, 60)

    return f"{h:d}:{m:02d}:{s:02d}"


def seconds_to_minutes_and_seconds(time, milliseconds=True):
    """Convert cue format ss.mm to MM:ss:mm format"""
    rounded_seconds = floor(float(time))
    minutes = floor(rounded_seconds / 60)
    seconds = rounded_seconds % 60

    return f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}{':00' if milliseconds else ''}"


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
