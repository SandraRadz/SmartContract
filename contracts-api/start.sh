#!/bin/bash

# Local .env
if [ -f .env ]; then
  # Load Environment Variables
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
  # For instance, will be example_kaggle_key
  echo "CHOSEN SERVICE LOCATION: $SERVICE_DIRECTORY"
else
  echo "Cannot load .env file"
  exit 1
fi

cd $SERVICE_DIRECTORY

# Activating virtual environment
source venv/bin/activate

# Starting service
python main.py
