SHELL=/bin/bash

.PHONY: help, install, setup, develop, database, timesheets

help:  # Help
	@echo "Available options: help, install, setup, develop, database, timesheets"

install:  # Install Python requirements
	pip install -r requirements.in

setup: install  # One-time setup including creating folder directories
	mkdir -p vdj-export
	mkdir -p processed-files

develop: install setup  # Setup devlopment requirements
	pip install -r development.in

format: develop  # Format files
	black .

database:  # Unzip and extract database info from a VDJ backup
	python scripts/database.py

timesheets:  database # Create timestamps for the given filepath in second args
	python scripts/generate-timesheets.py "$(arg)"

# Extract the second argument
arg := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

# Allow additional arguments to be passed
%:
	@: