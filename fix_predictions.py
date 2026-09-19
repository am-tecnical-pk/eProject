import sqlite3
import os

# Find the database
DATABASE = "edupredict.db"
if not os.path.exists(DATABASE):
    DATABASE = "data/edupredict.db"
if not os.path.exists(DATABASE):
    # Try to find it
    for root, dirs, files in os.walk("."):
        if "edupredict.db" in files:
            DATABASE = os.path.join(root, "edupredict.db")
            break

print(f"Using database: {DATABASE}")

def fix_predictions_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if predictions table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='predictions'")
    if cursor.fetchone():
        # Get existing columns
        cursor.execute("PRAGMA table_info(predictions)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Existing columns: {columns}")
        
        # Add missing columns
        missing_columns = []
        
        if 'predicted_at' not in columns:
            missing_columns.append('predicted_at')
            try:
                cursor.execute("ALTER TABLE predictions ADD COLUMN predicted_at TEXT")
                print("✅ Added predicted_at column")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not add predicted_at: {e}")
        
        if 'student_name' not in columns:
            missing_columns.append('student_name')
            try:
                cursor.execute("ALTER TABLE predictions ADD COLUMN student_name TEXT")
                print("✅ Added student_name column")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not add student_name: {e}")
        
        if 'student_id' not in columns:
            missing_columns.append('student_id')
            try:
                cursor.execute("ALTER TABLE predictions ADD COLUMN student_id TEXT")
                print("✅ Added student_id column")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not add student_id: {e}")
        
        if 'confidence' not in columns:
            missing_columns.append('confidence')
            try:
                cursor.execute("ALTER TABLE predictions ADD COLUMN confidence REAL")
                print("✅ Added confidence column")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not add confidence: {e}")
        
        conn.commit()
        
        # Show final columns
        cursor.execute("PRAGMA table_info(predictions)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Final columns: {columns}")
        
        print("✅ Database fix complete!")
    else:
        print("Predictions table doesn't exist. Creating it...")
        cursor.execute("""
            CREATE TABLE predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                student_name TEXT,
                attendance REAL,
                marks REAL,
                lms_activity REAL,
                previous_performance REAL,
                risk TEXT,
                confidence REAL,
                predicted_at TEXT
            )
        """)
        conn.commit()
        print("✅ Predictions table created!")
    
    conn.close()

if __name__ == "__main__":
    fix_predictions_table()