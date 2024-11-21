SHELL=/bin/bash

.PHONY: help, install, setup, develop, database, timesheets

help:  # Help
	@echo "Available options: help, install, setup, develop, database, timesheets"

install:  # Install Python requirements
	pip install -r requirements/requirements.in

setup: install  # One-time setup including creating folder directories
	mkdir -p vdj-export
	mkdir -p processed-files

develop: install setup  # Setup devlopment requirements
	pip install -r requirements/development.in

format: develop  # Format files
	black .

extract_vdj_data:  # Unzip and extract database info from a VDJ backup
	python scripts/virtualdj.py

youtube_chapters:  extract_vdj_data  # Create YouTube chapter format file with song timestamps
	python scripts/youtube.py "$(arg)"

cue_file:  extract_vdj_data  # Create CUE file with song timestamps
	python scripts/cuefile.py "$(arg)"

timesheets:  extract_vdj_data youtube_chapters cue_file  # Add any timesheets make targets here to run together

# Extract the second argument
arg := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

# Allow additional arguments to be passed
%:
	@: