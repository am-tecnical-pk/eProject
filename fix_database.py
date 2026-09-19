import bcrypt
from datetime import datetime
from db import (
    db, users_col, predictions_col, batches_col,
    student_batches_col, assignments_col, student_marks_col,
    datasets_col, dataset_mappings_col, reports_col,
    educational_records_col, alerts_col, system_logs_col
)


def fix_database():
    print("Starting MongoDB database fix...")

    collections = {
        "users": users_col,
        "predictions": predictions_col,
        "batches": batches_col,
        "student_batches": student_batches_col,
        "assignments": assignments_col,
        "student_marks": student_marks_col,
        "datasets": datasets_col,
        "dataset_mappings": dataset_mappings_col,
        "reports": reports_col,
        "educational_records": educational_records_col,
        "alerts": alerts_col,
        "system_logs": system_logs_col,
    }

    for name, col in collections.items():
        count = col.count_documents({})
        print(f"  Collection '{name}': {count} documents")

    print("\nCreating default users...")
    default_users = {
        "admin@gmail.com": {"password": "admin123", "name": "Admin User", "role": "administrator"},
        "teacher@edupredict.com": {"password": "teacher123", "name": "Teacher User", "role": "teacher"},
        "student@edupredict.com": {"password": "student123", "name": "Student User", "role": "student"},
        "analyst@edupredict.com": {"password": "analyst123", "name": "Data Analyst", "role": "analyst"}
    }

    for email, data in default_users.items():
        if not users_col.find_one({"email": email}):
            hashed = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
            users_col.insert_one({
                "email": email,
                "password": hashed,
                "name": data["name"],
                "role": data["role"],
                "created_at": datetime.now().isoformat(),
                "is_active": 1
            })
            print(f"  Created user: {email} ({data['role']})")
        else:
            print(f"  User already exists: {email}")

    print("\nDatabase fix complete!")
    print("\nDefault Login Credentials:")
    print("   Admin:    admin@gmail.com / admin123")
    print("   Teacher:  teacher@edupredict.com / teacher123")
    print("   Student:  student@edupredict.com / student123")
    print("   Analyst:  analyst@edupredict.com / analyst123")


if __name__ == "__main__":
    fix_database()
