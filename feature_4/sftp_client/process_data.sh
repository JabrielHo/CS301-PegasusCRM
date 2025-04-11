#!/bin/bash
# Script to pull data from SFTP and populate database

source .env
echo "$(date): Starting data processing" >> $LOG_FILE

# Pull data from SFTP server
echo "$(date): Pulling data from SFTP server" >> $LOG_FILE
python3 /home/ec2-user/scripts/pull_data.py
if [ $? -ne 0 ]; then
    echo "$(date): Failed to pull data from SFTP server" >> $LOG_FILE
    exit 1
fi

# Populate database
echo "$(date): Populating database" >> $LOG_FILE
python3 /home/ec2-user/scripts/populate_db.py
if [ $? -ne 0 ]; then
    echo "$(date): Failed to populate database" >> $LOG_FILE
    exit 1
fi