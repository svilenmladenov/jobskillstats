import mysql.connector
from datetime import datetime

# Database connection config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySvilen',
    'database': 'project'
}

grid = []
rows = 0


try:
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    row = [None] * 4

    # Data to insert (without id)
    row[0] = "Auto-incremented insert"
    row[1] = datetime.now().date()
    row[2] = "https://dev.bg/company/jobads/yamasoft-site-reliability-engineer-senior-devops-engineer/"
    row[3] = "Test2"

    grid.append(row)

    # Insert query
    insert_query = "INSERT INTO test (text, date, link, text2) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (grid[0][0], grid[0][1], grid[0][2], grid[0][3], ))

    # Commit changes
    conn.commit()

    print(f"Inserted with ID: {cursor.lastrowid}")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
