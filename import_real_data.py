import pandas as pd
from datetime import datetime
import bcrypt
from app import app
from db import db, users_col, educational_records_col, predictions_col
from model import predict_risk

def import_real_data():
    print("Loading real dataset...")
    try:
        # Aapki CSV file ka naam (Agar file uploads folder mai hai toh 'uploads/dataset.csv' likhein)
        df = pd.read_csv('dataset.csv') 
        
        with app.app_context():
            # Purana blank data clear kar rahe hain
            educational_records_col.delete_many({})
            predictions_col.delete_many({})
            
            records_to_insert = []
            predictions_to_insert = []
            
            # Default password for real students
            hashed_pw = bcrypt.hashpw(b"student123", bcrypt.gensalt())
            
            print(f"Found {len(df)} records. Importing into database...")
            
            for index, row in df.iterrows():
                # Column names ko lowercase mai convert kar rahay hain taake match karne mai asani ho
                row_dict = {str(k).lower().strip(): v for k, v in row.items()}
                
                # Fetching values safely from your CSV
                s_name = str(row_dict.get('name', row_dict.get('student_name', f'Learner {index+1}')))
                att = float(row_dict.get('attendance', row_dict.get('att', 75.0)))
                marks = float(row_dict.get('marks', row_dict.get('score', row_dict.get('assignment_score', 70.0))))
                lms = float(row_dict.get('lms_activity', row_dict.get('lms', 65.0)))
                prev = float(row_dict.get('previous_performance', row_dict.get('study_hours', 70.0)))
                
                sid = str(1000 + index)
                
                # 1. Create Student User
                email = f"student{sid}@edupredict.com"
                if not users_col.find_one({"email": email}):
                    users_col.insert_one({
                        "id": sid, "name": s_name, "email": email,
                        "password": hashed_pw, "role": "student",
                        "created_at": datetime.now().isoformat(), "is_active": 1
                    })
                
                # 2. Add to Educational Records (For Analytics Dashboard)
                avg = (att + marks + lms + prev) / 4.0
                risk_label = "Low" if avg >= 75 else ("Medium" if avg >= 60 else "High")
                
                records_to_insert.append({
                    "student_id": sid,
                    "student_name": s_name,
                    "attendance": att,
                    "marks": marks,
                    "lms_activity": lms,
                    "previous_performance": prev,
                    "risk": risk_label,
                    "created_at": datetime.now().isoformat()
                })
                
                # 3. Add to Predictions Pipeline
                pred = predict_risk(att, marks, lms, prev)
                predictions_to_insert.append({
                    "student_id": sid,
                    "student_name": s_name,
                    "attendance": att,
                    "marks": marks,
                    "lms_activity": lms,
                    "previous_performance": prev,
                    "risk": pred["risk"],
                    "predicted_grade": pred.get("predicted_grade", "B"),
                    "confidence": round(float(pred.get("confidence", 0.85)), 4),
                    "predicted_at": datetime.now().isoformat()
                })
            
            if records_to_insert:
                educational_records_col.insert_many(records_to_insert)
            if predictions_to_insert:
                predictions_col.insert_many(predictions_to_insert)
                
            print(f"SUCCESS! {len(records_to_insert)} real records imported to dashboards.")
            print("You can now start your app.py!")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure 'dataset.csv' exists in your main folder.")

if __name__ == "__main__":
    import_real_data()