from app import app
from db import users_col, db

with app.app_context():
    # Saare users delete karke naye seed kar rahe hain taake koi purani ghalit email na rahe
    users_col.delete_many({})
    db["counters"].delete_many({})
    
    from analytics_data import init_database
    init_database()
    print("Database re-initialized with correct emails!")