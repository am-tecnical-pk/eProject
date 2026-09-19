"""
EduPredict - Database Seeder
Creates realistic student data, batches, assignments, predictions, and educational records.
"""
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import bcrypt

client = MongoClient('mongodb://localhost:27017')
db = client['EduPredict']

print("Clearing old data...")
for col in db.list_collection_names():
    if col == 'counters':
        continue
    db[col].drop()

# ========== USERS ==========
print("Seeding users...")
users_col = db['users']

teachers = [
    {"email": "teacher@edupredict.com", "name": "Dr. Ayesha Khan", "role": "teacher"},
    {"email": "prof.ali@edupredict.com", "name": "Prof. Ali Raza", "role": "teacher"},
    {"email": "dr.sara@edupredict.com", "name": "Dr. Sara Malik", "role": "teacher"},
]

analysts = [
    {"email": "analyst@edupredict.com", "name": "Hamza Tariq", "role": "analyst"},
]

student_data = [
    ("Ahmed Khan", "ahmed@student.com"),
    ("Fatima Ali", "fatima@student.com"),
    ("Hassan Raza", "hassan@student.com"),
    ("Zainab Malik", "zainab@student.com"),
    ("Omar Farooq", "omar@student.com"),
    ("Amina Siddiqui", "amina@student.com"),
    ("Bilal Ahmed", "bilal@student.com"),
    ("Noor Hassan", "noor@student.com"),
    ("Ali Hamza", "ali@student.com"),
    ("Sana Bibi", "sana@student.com"),
    ("Usman Ghani", "usman@student.com"),
    ("Maryam Noor", "maryam@student.com"),
    ("Kamran Shah", "kamran@student.com"),
    ("Hira Khan", "hira@student.com"),
    ("Talha Mehmood", "talha@student.com"),
    ("Rabia Aslam", "rabia@student.com"),
    ("Faisal Qureshi", "faisal@student.com"),
    ("Mehwish Sheikh", "mehwish@student.com"),
    ("Saad Ali", "saad@student.com"),
    ("Iqra Javed", "iqra@student.com"),
    ("Danish Rehman", "danish@student.com"),
    ("Ayesha Siddiqa", "ayesha@student.com"),
    ("Imran Khan", "imran@student.com"),
    ("Nadia Parveen", "nadia@student.com"),
    ("Shahid Afridi", "shahid@student.com"),
    ("Rukhsana Bibi", "ukhsana@student.com"),
    ("Waqas Ahmed", "waqas@student.com"),
    ("Sobia Malik", "sobia@student.com"),
    ("Adnan Khan", "adnan@student.com"),
    ("Bushra Bibi", "bushra@student.com"),
    ("Kashif Raza", "kashif@student.com"),
    ("Saima Akhtar", "saima@student.com"),
    ("Tariq Mahmood", "tariq@student.com"),
    ("Zara Hussain", "zara@student.com"),
    ("Naeem Shah", "naeem@student.com"),
    ("Farah Naz", "farah@student.com"),
    ("Asif Javed", "asif@student.com"),
    ("Samina Bibi", "samina@student.com"),
    ("Rashid Minhas", "rashid@student.com"),
    ("Nasreen Akhter", "nasreen@student.com"),
]

user_ids = {}
hashed = bcrypt.hashpw("student123".encode('utf-8'), bcrypt.gensalt())

# Insert admin
users_col.insert_one({"id": 1, "email": "admin@gmail.com", "password": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()), "name": "Admin User", "role": "administrator", "created_at": "2026-01-01", "is_active": 1})
user_ids["admin@gmail.com"] = 1

# Insert teachers
for i, t in enumerate(teachers):
    uid = i + 2
    users_col.insert_one({"id": uid, "email": t["email"], "password": hashed, "name": t["name"], "role": "teacher", "created_at": "2026-01-15", "is_active": 1})
    user_ids[t["email"]] = uid

# Insert analyst
uid = len(teachers) + 2
users_col.insert_one({"id": uid, "email": "analyst@edupredict.com", "password": hashed, "name": "Hamza Tariq", "role": "analyst", "created_at": "2026-02-01", "is_active": 1})
user_ids["analyst@edupredict.com"] = uid

# Insert students
student_ids = []
start_id = len(teachers) + len(analysts) + 2
for i, (name, email) in enumerate(student_data):
    uid = start_id + i
    users_col.insert_one({"id": uid, "email": email, "password": hashed, "name": name, "role": "student", "created_at": "2026-02-10", "is_active": 1})
    user_ids[email] = uid
    student_ids.append(uid)

print(f"  Inserted {len(student_ids)} students, {len(teachers)} teachers, 1 analyst, 1 admin")

# ========== BATCHES ==========
print("Seeding batches...")
batches_col = db['batches']
batch_data = [
    {"id": 1, "name": "Computer Science - Section A", "teacher_id": user_ids["teacher@edupredict.com"], "created_at": "2026-01-20"},
    {"id": 2, "name": "Computer Science - Section B", "teacher_id": user_ids["prof.ali@edupredict.com"], "created_at": "2026-01-20"},
    {"id": 3, "name": "Data Science - Section A", "teacher_id": user_ids["dr.sara@edupredict.com"], "created_at": "2026-02-01"},
]
batches_col.insert_many(batch_data)
print(f"  Inserted {len(batch_data)} batches")

# ========== STUDENT_BATCHES ==========
print("Assigning students to batches...")
student_batches_col = db['student_batches']
assignments_list = []
for i, sid in enumerate(student_ids):
    batch_id = (i % 3) + 1
    assignments_list.append({"student_id": sid, "batch_id": batch_id})
student_batches_col.insert_many(assignments_list)
print(f"  Assigned {len(assignments_list)} students to batches")

# ========== ASSIGNMENTS ==========
print("Seeding assignments...")
assignments_col = db['assignments']
assignment_data = [
    {"id": 1, "batch_id": 1, "teacher_id": user_ids["teacher@edupredict.com"], "title": "Midterm Exam", "subject": "Data Structures", "total_marks": 100, "due_date": "2026-03-15", "created_at": "2026-03-01"},
    {"id": 2, "batch_id": 1, "teacher_id": user_ids["teacher@edupredict.com"], "title": "Assignment 1 - Arrays", "subject": "Data Structures", "total_marks": 50, "due_date": "2026-03-20", "created_at": "2026-03-05"},
    {"id": 3, "batch_id": 2, "teacher_id": user_ids["prof.ali@edupredict.com"], "title": "Quiz 1 - Python Basics", "subject": "Programming", "total_marks": 30, "due_date": "2026-03-10", "created_at": "2026-03-02"},
    {"id": 4, "batch_id": 2, "teacher_id": user_ids["prof.ali@edupredict.com"], "title": "Final Project", "subject": "Programming", "total_marks": 200, "due_date": "2026-04-30", "created_at": "2026-03-10"},
    {"id": 5, "batch_id": 3, "teacher_id": user_ids["dr.sara@edupredict.com"], "title": "ML Model Evaluation", "subject": "Machine Learning", "total_marks": 100, "due_date": "2026-04-01", "created_at": "2026-03-15"},
    {"id": 6, "batch_id": 3, "teacher_id": user_ids["dr.sara@edupredict.com"], "title": "Data Cleaning Lab", "subject": "Data Science", "total_marks": 75, "due_date": "2026-03-25", "created_at": "2026-03-12"},
]
assignments_col.insert_many(assignment_data)
print(f"  Inserted {len(assignment_data)} assignments")

# ========== STUDENT_MARKS ==========
print("Seeding student marks...")
student_marks_col = db['student_marks']
marks_data = []
mark_id = 1
for aid in [1, 2, 3, 5, 6]:
    assignment = [a for a in assignment_data if a["id"] == aid][0]
    batch_students = [s for s in assignments_list if s["batch_id"] == assignment["batch_id"]]
    for sa in batch_students[:12]:
        obtained = random.randint(int(assignment["total_marks"] * 0.3), assignment["total_marks"])
        marks_data.append({
            "student_id": sa["student_id"],
            "assignment_id": aid,
            "obtained_marks": obtained,
            "graded_at": datetime(2026, 3, random.randint(15, 28)).isoformat()
        })
        mark_id += 1
student_marks_col.insert_many(marks_data)
print(f"  Inserted {len(marks_data)} marks records")

# ========== EDUCATIONAL RECORDS ==========
print("Seeding educational records...")
edu_records_col = db['educational_records']
records = []
for sid in student_ids:
    attendance = random.gauss(72, 18)
    marks = random.gauss(68, 20)
    lms = random.gauss(60, 22)
    prev = random.gauss(70, 16)
    attendance = max(20, min(100, round(attendance, 1)))
    marks = max(15, min(100, round(marks, 1)))
    lms = max(10, min(100, round(lms, 1)))
    prev = max(20, min(100, round(prev, 1)))
    
    avg = (attendance + marks + lms + prev) / 4
    if avg >= 75: risk = "Low"
    elif avg >= 55: risk = "Medium"
    else: risk = "High"
    
    name = [n for n, e in student_data if users_col.find_one({"id": sid}) and users_col.find_one({"id": sid})["name"] == n]
    student_name = name[0] if name else "Student"
    
    records.append({
        "student_id": str(sid),
        "student_name": student_name,
        "attendance": attendance,
        "marks": marks,
        "lms_activity": lms,
        "previous_performance": prev,
        "risk": risk,
        "created_at": datetime(2026, random.randint(1, 6), random.randint(1, 28)).isoformat()
    })
edu_records_col.insert_many(records)
print(f"  Inserted {len(records)} educational records")

# ========== PREDICTIONS ==========
print("Seeding predictions...")
predictions_col = db['predictions']
preds = []
for rec in records:
    preds.append({
        "student_id": rec["student_id"],
        "student_name": rec["student_name"],
        "attendance": rec["attendance"],
        "marks": rec["marks"],
        "lms_activity": rec["lms_activity"],
        "previous_performance": rec["previous_performance"],
        "risk": rec["risk"],
        "confidence": round(random.uniform(0.65, 0.98), 2),
        "predicted_at": rec["created_at"]
    })
predictions_col.insert_many(preds)
print(f"  Inserted {len(preds)} predictions")

# ========== ALERTS ==========
print("Seeding alerts...")
alerts_col = db['alerts']
high_risk = [r for r in records if r["risk"] == "High"]
alerts = []
for r in high_risk:
    alerts.append({
        "student_id": r["student_id"],
        "alert_type": "Academic Risk",
        "message": f"High-risk student detected: {r['student_name']}",
        "severity": "High",
        "created_at": r["created_at"],
        "status": "New"
    })
if alerts:
    alerts_col.insert_many(alerts)
print(f"  Inserted {len(alerts)} alerts")

# ========== SYSTEM LOGS ==========
print("Seeding system logs...")
logs_col = db['system_logs']
logs = [
    {"event": "System Start", "details": "EduPredict system started", "created_at": datetime(2026, 1, 1).isoformat()},
    {"event": "Data Import", "details": "Imported 40 student records", "created_at": datetime(2026, 2, 1).isoformat()},
    {"event": "Model Training", "details": "ML model retrained with 3000 samples", "created_at": datetime(2026, 3, 1).isoformat()},
    {"event": "Batch Created", "details": "Created 3 batches", "created_at": datetime(2026, 1, 20).isoformat()},
]
logs_col.insert_many(logs)
print(f"  Inserted {len(logs)} system logs")

# ========== COUNTERS ==========
print("Setting up ID counters...")
counters_col = db['counters']
counters_col.drop()
counters_col.insert_many([
    {"_id": "users", "seq": start_id + len(student_data)},
    {"_id": "batches", "seq": 3},
    {"_id": "assignments", "seq": 6},
    {"_id": "datasets", "seq": 0},
    {"_id": "reports", "seq": 0},
])

print("\n=== Database seeded successfully! ===")
print(f"  Users: {users_col.count_documents({})}")
print(f"  Students: {len(student_ids)}")
print(f"  Batches: {batches_col.count_documents({})}")
print(f"  Assignments: {assignments_col.count_documents({})}")
print(f"  Marks: {student_marks_col.count_documents({})}")
print(f"  Records: {edu_records_col.count_documents({})}")
print(f"  Predictions: {predictions_col.count_documents({})}")
print(f"  Alerts: {alerts_col.count_documents({})}")
