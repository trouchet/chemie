#!/bin/bash
clear

# Define the omitted paths
OMIT_PATHS="tests/*,/usr,backend/app/main.py,backend/app/core/config.py"

while true; do
  coverage run --rcfile=.coveragerc -m pytest
  coverage report --omit="$OMIT_PATHS" --show-missing

  sleep 5  # Adjust delay between test runs if needed
  clear
done
