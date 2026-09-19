from app import app
from db import users_col

with app.app_context():
    # Database mein teacher ki email update kar rahay hain
    result = users_col.update_one(
        {"role": "teacher"},
        {"$set": {"email": "Teacher.ep9@gmail.com"}}
    )
    print(f"Updated {result.modified_count} teacher email to Teacher.ep9@gmail.com")