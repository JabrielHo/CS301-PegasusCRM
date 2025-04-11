#!/usr/bin/env python3
import paramiko
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/tmp/sftp_pull.log'
)
logger = logging.getLogger('sftp_pull')

# SFTP Server details
SFTP_HOST = os.getenv("SFTP_HOST")  # Replace with actual IP
SFTP_USER = os.getenv("SFTP_USER")
SFTP_PASS = os.getenv("SFTP_PASS")  # Replace with actual password
REMOTE_PATH = os.getenv("REMOTE_PATH")
LOCAL_DIR = os.getenv("LOCAL_DIR")
LOCAL_PATH = os.path.join(LOCAL_DIR, 'data.csv')

def pull_data_from_sftp():
    try:
        # Connect to SFTP server
        transport = paramiko.Transport((SFTP_HOST, 22))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Check if file exists
        try:
            sftp.stat(REMOTE_PATH)
        except FileNotFoundError:
            logger.error(f"Remote file {REMOTE_PATH} not found")
            sftp.close()
            transport.close()
            return False

        # Download file
        sftp.get(REMOTE_PATH, LOCAL_PATH)
        logger.info(f"Successfully downloaded {REMOTE_PATH} to {LOCAL_PATH}")

        # Close connection
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        logger.error(f"Error pulling data from SFTP: {str(e)}")
        return False

if __name__ == "__main__":
    pull_data_from_sftp()