import psycopg2
import csv
import os

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# CSV file paths
PATH = os.getenv("PATH")
TMP_TRANSACTION_CSV = PATH + 'tmp_data.csv'
TRANSACTION_CSV = PATH + 'data.csv'

# Text file to store the last transaction ID
LAST_TRANSACTION_ID_FILE = PATH + 'last_transaction_id.txt'

def fetch_new_transactions():
    # Fetch the last transaction ID from the text file
    try:
        with open(LAST_TRANSACTION_ID_FILE, 'r') as file:
            last_transaction_id = int(file.read())
    except (FileNotFoundError, ValueError):
        last_transaction_id = 0

    # Establish a connection to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()

    # Fetch new transactions from the database
    cur.execute("SELECT * FROM transactions WHERE id > %s", (last_transaction_id,))
    new_transactions = cur.fetchall()

    # Close the connection
    cur.close()
    conn.close()

    return new_transactions

def write_to_csv(transactions, filename):
    # Define the field names - already updated to match new schema
    fieldnames = ['id', 'client_id', 'client_account_id', 'transaction_type', 'amount', 'transaction_date', 'status']

    # Write transactions to the CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for transaction in transactions:
            writer.writerow({
                'id': transaction[0],
                'client_id': str(transaction[1]),  # Ensure UUID is converted to string
                'client_account_id': str(transaction[2]),  # Ensure UUID is converted to string
                'transaction_type': transaction[3],
                'amount': transaction[4],
                'transaction_date': transaction[5],
                'status': transaction[6]
            })

def update_last_transaction_id(transactions):
    if transactions:
        last_transaction_id = max(transaction[0] for transaction in transactions)
        with open(LAST_TRANSACTION_ID_FILE, 'w') as file:
            file.write(str(last_transaction_id))

def swap_csv_files(tmp_filename, final_filename):
    # Check if the final file exists
    if os.path.exists(final_filename):
        # Rename the final file to a backup
        os.rename(final_filename, f"{final_filename}.bak")

    # Rename the temporary file to the final filename
    os.rename(tmp_filename, final_filename)

if __name__ == '__main__':
    # Fetch new transactions from the database
    new_transactions = fetch_new_transactions()

    # Write new transactions to the temporary CSV file
    write_to_csv(new_transactions, TMP_TRANSACTION_CSV)

    # Update the last transaction ID in the text file
    update_last_transaction_id(new_transactions)

    # Swap the temporary CSV with the final CSV
    swap_csv_files(TMP_TRANSACTION_CSV, TRANSACTION_CSV)