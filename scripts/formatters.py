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


def seconds_to_hours_minutes_and_seconds(seconds):
    """
    Convert seconds to formatted hh:mm:ss string or empty
    """
    if not seconds:
        return ""
    m, s = divmod(int(float(seconds)), 60)
    h, m = divmod(m, 60)

    return f"{h:d}:{m:02d}:{s:02d}"


def seconds_to_minutes_and_seconds(time):
    """Convert cue format ss.mm to MM:ss:mm format"""
    rounded_seconds = floor(float(time))
    minutes = floor(rounded_seconds / 60)
    seconds = rounded_seconds % 60

    return f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:00"
