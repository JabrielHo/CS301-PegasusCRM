#!/usr/bin/env python3
import pandas as pd
import logging
from sqlalchemy import create_engine, text
import os
from io import StringIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/tmp/db_populate.log'
)
logger = logging.getLogger('db_populate')

# Database connection details
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# CSV file path
CSV_FILE = os.getenv("CSV_FILE")

def populate_database():
    try:
        # Check if CSV file exists
        if not os.path.exists(CSV_FILE):
            logger.error(f"CSV file {CSV_FILE} not found")
            return False

        # Create SQLAlchemy engine
        engine = create_engine(DB_URL)

        # Read CSV file
        df = pd.read_csv(CSV_FILE)

        # Convert date strings to datetime objects
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        # Use the more efficient COPY command for bulk inserts
        conn = engine.raw_connection()
        cursor = conn.cursor()

        # Create a buffer from the dataframe
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        # Use COPY command for bulk insert
        cursor.copy_from(
            buffer,
            'transactions',
            sep=',',
            columns=('id', 'client_id', 'client_account_id', 'transaction_type', 'amount', 'transaction_date', 'status')
        )

        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Successfully populated database with {len(df)} records from {CSV_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error populating database: {str(e)}")
        return False

if __name__ == "__main__":
    populate_database()