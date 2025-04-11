#!/bin/bash
# Database connection details
source .env

echo "$(date): Starting transaction ID tracking" >> $LOG_FILE

# Get the last transaction ID
LAST_ID=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COALESCE(MAX(id), 0) FROM transactions;")
LAST_ID=$(echo "$LAST_ID" | tr -d '[:space:]')

# Save to file
echo "$LAST_ID" > /tmp/last_transaction_id.txt

# Upload to SFTP server
sftp sftp_user@$SFTP_SERVER_IP << EOF
cd uploads
put /tmp/last_transaction_id.txt
exit
EOF