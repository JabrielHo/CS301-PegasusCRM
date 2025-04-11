import psycopg2
import random
import uuid
import os
from datetime import date, timedelta

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def generate_transactions():
    # List of specific UUIDs to choose from
    client_uuids = [
        '3afca589-d05a-41ac-b30c-f5a645f1976b',
        '4c3d2a88-e05d-4182-9d4c-7f12857603c3',
        'a56459cf-f66a-410d-93e1-51bba05fd2b0',
        'b173a3a1-3a8a-474d-8c9f-2af6a690f49d',
        'c13671a7-6abb-4034-be7f-80d223705a89',
        'c327296c-86eb-47a5-a138-90f1b81be180',
        'ce139e65-be8a-4506-8c5a-bf45fd58d41f',
        'cef4af91-503d-4356-9ffe-f5621a444f2b',
        'd2f366af-ca3f-4975-a855-7528b3eaba55',
        'd58f86c2-af37-4307-a114-33c51153c594',
        'd7f1905b-ca99-4866-8483-7b59f5ec4a58'
    ]

    # List of specific account UUIDs
    account_uuids = [
        'a085421b-a41f-494b-8d30-82d16d5dded4',
        'dd1e2c34-e088-4796-95ea-5e83f4e8b974',
        '890f85e5-da4f-4a94-8a4e-31617d1c84fa',
        '2b5d7cba-c14d-4ddb-9ba6-55af8ceefffa',
        '7b68e96d-6d69-46e2-a2e7-87f521f21a72',
        '09c723b5-5d61-4e7a-978b-6866c0688a2d',
        'd7aeb242-d4a0-4058-8cdc-6ec495afe354',
        '3281e874-a047-4335-a82c-76d0f3a5a354',
        '44dcc1c4-0e2f-4bf9-877f-ae526165ae37',
        '636398cb-cd07-4f87-b6b9-24b5565187d0',
        '60dd1af3-6e89-419d-8b7d-074805202461'
    ]

    # Create a dictionary to associate client IDs with account IDs
    client_account_mapping = dict(zip(client_uuids, account_uuids))

    # Establish a connection to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()

    # Generate random transactions
    for _ in range(10):  # Generate 10 transactions at a time
        client_id = random.choice(client_uuids)  # Randomly select a UUID from the list
        client_account_id = client_account_mapping[client_id]  # Get the associated account ID
        transaction_type = 'W' if random.random() < 0.5 else 'D'  # Random transaction type
        amount = round(random.uniform(100.0, 5000.0), 2)  # Random amount between 100 and 5000
        transaction_date = date.today() - timedelta(days=random.randint(0, 30))  # Random date within the last month
        status = random.choice(['Completed', 'Pending', 'Failed'])  # Random status

        # Insert transaction into the database
        cur.execute("""
        INSERT INTO transactions (
            client_id,
            client_account_id,
            transaction_type,
            amount,
            transaction_date,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (client_id, client_account_id, transaction_type, amount, transaction_date, status))

    # Commit changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    generate_transactions()