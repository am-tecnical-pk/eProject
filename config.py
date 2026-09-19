import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://localhost:27017/EduPredict"

# ============================================================
# APPLICATION & SECURITY CONFIGURATION
# ============================================================

APP_NAME = "EduPredict"
APP_VERSION = "2.4.0"
DEBUG_MODE = True
SECRET_KEY = Config.SECRET_KEY

# ============================================================
# DATABASE CONFIGURATION (MONGODB & HDFS STORAGE PARITY)
# ============================================================

MONGO_URI = Config.MONGO_URI
DB_NAME = os.environ.get("DB_NAME", "EduPredict")
DATABASE_PATH = "edupredict.db"  # SQLite fallback reference if needed

# ============================================================
# AUTOMATED SMTP ALERT & NOTIFICATION SERVICE
# ============================================================

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USER = os.environ.get("EMAIL_USER", "attamuhammad7587@gmail.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "fjmvfyvfbvqqjszy")

# NAYA ARCHITECTURE: Desired Mails for Direct Routing
ROLE_EMAILS = {
    "administrator": "Admin.ep9@gmail.com",
    "analyst": "Analyst.ep9@gmail.com",
    "teacher": "Teacher.ep9@gmail.com"
}
ADMIN_EMAIL = ROLE_EMAILS["administrator"]

# ============================================================
# DATA INGESTION & HDFS PARTITION STORAGE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORTS_FOLDER = os.path.join(BASE_DIR, "static", "reports")
SUBMISSIONS_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "submissions")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backups")

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {'.csv', '.json', '.parquet'}

# Ensure required storage directories exist
for folder in [UPLOAD_FOLDER, REPORTS_FOLDER, SUBMISSIONS_FOLDER, BACKUP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ============================================================
# MACHINE LEARNING & MAPREDUCE ANOMALY THRESHOLDS
# ============================================================

MODEL_FILE = os.path.join(BASE_DIR, "risk_model.pkl")
SCALER_FILE = os.path.join(BASE_DIR, "scaler.pkl")
COURSE_DEMAND_MODEL_FILE = os.path.join(BASE_DIR, "demand_model.pkl")

MODEL_FEATURES = ['attendance', 'marks', 'lms_activity', 'previous_performance']
RISK_LEVELS = ['Low', 'Medium', 'High']

# MapReduce Threshold Screening Parameters
ANOMALY_ATTENDANCE_CRITICAL = 50.0
ANOMALY_ATTENDANCE_WARNING = 75.0
ANOMALY_MARKS_CRITICAL = 40.0
ANOMALY_MARKS_WARNING = 50.0
ANOMALY_LMS_WARNING = 40.0