import mysql.connector
from datetime import datetime

# Database connection config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySvilen',
    'database': 'project'
}

try:
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Data to insert (without id)
    text_value = "Auto-incremented insert"
    date_value = datetime.now().date()
    link_value = "https://dev.bg/company/jobads/yamasoft-site-reliability-engineer-senior-devops-engineer/"
    text2_value = "Test2"

    # Insert query
    insert_query = "INSERT INTO test (text, date, link, text2) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (text_value, date_value, link_value, text2_value, ))

    # Commit changes
    conn.commit()

    print(f"Inserted with ID: {cursor.lastrowid}")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
