#!/bin/bash

PYTHON_SCRIPT="listener.py"
PYTHON_PATH="/usr/bin/python3"

#  it will start at 00:15 every day from Monday to Friday
CRON_SCHEDULE="15 0 * * 1-5"

CRON_COMMAND="$PYTHON_PATH $PYTHON_SCRIPT"
CRON_EXISTS=$(crontab -l | grep -F "$CRON_COMMAND")

# If cron job does not exist, add it to the crontab
if [ -z "$CRON_EXISTS" ]; then
    # Add the cron job to the user's crontab
    (crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $CRON_COMMAND") | crontab -
    echo "Cron job added: $CRON_SCHEDULE $CRON_COMMAND"
else
    echo "Cron job already exists: $CRON_COMMAND"
fi
