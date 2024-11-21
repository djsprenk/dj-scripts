# DJ Scripts

Scripts I use for DJ tasks / management.

## Quick Start

### Install Requirements

Set up and activate a virtual environment

```bash
virtualenv venv
source venv/bin/activate
```

Run install / setup scripts (install Python requirements, create required folders):

```bash
make setup
```

### Add Your Info

Create a new file called `.env` in the root of the project (or rename and edit the sample [.env-sample](./.env-sample) to `.env`), modifying values below to match your specific paths / values):

- `DJ_NAME`: your DJ name to add to processed files.
- `VDJ_DB_BACKUP_DIR`: Path to your VirtualDJ backup directory. On MacOS, usually `/Users/{USER}/Documents/VirtualDJ/Backup`, on Windows, usually `C:\users\{USER}\VirtualDJ\Backup`.

### Pulling data from VDJ

These scripts rely on having access to a Database Backup from VirtualDJ (VDJ). To get a database backup:

1. In the VDJ Browser view, click the dot for more commands.
2. Click Database > Create Database Backup
3. This should create a timestamped database backup ZIP in your `VirtualDJ > Backup` folder.

Next, run:

```bash
make extract_vdj_data
```

This will unzip and unpack the contents of your database export into `{dj-scripts}/vdj-export` and convert that data to JSON (`{processed-files}/database.json`) for easier reading by Python.

## Available Scripts

### Generate YouTube Chapters comment

Generate a YouTube comment containing chapters and timestamps for songs in a recorded set.

```bash
make youtube_chapters "{set file}"
```

This creates a new file in the `PROCESSED_FILES_DIR` called `{set file}.txt`.

### Generate a CUE file

Generate a CUE file containing chapters and timestamps for songs in a recorded set.

```bash
make cue_file "{set file}"
```

This creates a new file in the `PROCESSED_FILES_DIR` called `{set file}.txt`.

### Generate Timesheets

Generate all available timesheet formats for a given set.

```bash
make timesheets "{set file name}"
```

Outputs new files to the `PROCESSED_FILES_DIR` directory.

## Developing

Install development requirements with:

```bash
make develop
```

Format files(with `black`) by running:

```bash
make format
```
