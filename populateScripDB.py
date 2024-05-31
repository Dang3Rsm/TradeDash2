import csv
import sqlite3


def csv_to_sqlite(CSV_FILE, DB_NAME, TABLE_NAME):
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({', '.join(headers)})")
        for row in reader:
            cursor.execute(f"INSERT INTO {TABLE_NAME} VALUES ({', '.join('?' * len(row))})", row)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("=== Populating Scrip DB ===")
    DB_NAME = "scripDB.sqlite3"
    CSV_FILE = "api-scrip-master.csv"
    TABLE_NAME = "scrip_master_table"
    csv_to_sqlite(CSV_FILE, DB_NAME, TABLE_NAME)
    print("=== Successful: Populate Scrip DB ===")

