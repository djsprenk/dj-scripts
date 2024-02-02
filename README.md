# DJ Scripts

Scripts I use for DJ tasks / management

## Quickstart

### Install Requirements

Set up and activate a virtual environment

```
virtualenv venv
source venv/bin/activate
```

Install Python requirements into your virtual environment:

```
pip install -r requirements.in
```

### Add Your Info

In `scripts/constants.py` modify `DJ_NAME` to be the DJ name you want used in CUE files, etc.

### Export Virtual DJ Database

These scripts rely on having access to a Database Backup from VirtualDJ (VDJ). To get a database backup:

1. In the VDJ Browser view, click the dot for more commands.
2. Click Database > Create Database Backup
3. This should create a timestamped database backup ZIP in your `VirtualDJ > Backup` folder.

Next, unzip and unpack the contents of your database export into a folder in this project called `vdj-export`. The scripts expect a `database.xml` file as an immediate child to this export directory.

## Available Scripts

### CUE File

Given a set recorded with VirtualDJ having cues in the default VirtualDJ cue format (`Artist - Song Title`), create a CUE file with those songs and timestamps.

```bash
python scripts/cue-file.py "{set file name}"
```

Outputs a new file, `{set file name}.cue`, to `processed-files` directory.

## Developing

Install development requirements:

```
pip install -r development.in
```

Python files are formatted with `black`.
