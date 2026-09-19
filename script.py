import sqlite3

conn = sqlite3.connect('edupredict.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE assignment_submissions ADD COLUMN file_path TEXT")
    conn.commit()
    print("Column added successfully!")
except sqlite3.OperationalError:
    print("Column already exists.")

conn.close()