from pymongo import MongoClient
from collections import defaultdict

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client['edupredict']  # Apna DB name check karein
alerts_col = db['alerts']

all_alerts = list(alerts_col.find())
print(f"Total alerts before cleanup: {len(all_alerts)}")

# Group by (student_id + alert_type)
seen = defaultdict(list)
for alert in all_alerts:
    key = (
        str(alert.get('student_id', 'unknown')),
        alert.get('alert_type', 'unknown')
    )
    seen[key].append(alert)

deleted_count = 0
for key, alerts in seen.items():
    if len(alerts) > 1:
        # Latest wala rakhein
        alerts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        for dup in alerts[1:]:
            alerts_col.delete_one({"_id": dup["_id"]})
            deleted_count += 1

print(f"\n✅ Total {deleted_count} duplicate alerts deleted!")
print(f"📊 Remaining unique alerts: {alerts_col.count_documents({})}")

# Har student ke liye kitne alerts hain, woh bhi dikhayein
print("\n📋 Breakdown by student:")
by_student = defaultdict(int)
for alert in alerts_col.find():
    by_student[alert.get('student_name', 'Unknown')] += 1
for name, count in sorted(by_student.items(), key=lambda x: -x[1])[:10]:
    print(f"  {name}: {count} alerts")