from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy import create_engine, text
import pymongo
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database connections
MYSQL_DSN = os.getenv('MYSQL_DSN', 'mysql+pymysql://root:password@localhost:3306/nursing_home_db')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'nursing_home_visits')

# MySQL connection
mysql_engine = create_engine(MYSQL_DSN, pool_pre_ping=True)

# MongoDB connection
try:
    mongo_client = pymongo.MongoClient(MONGODB_URI)
    mongo_db = mongo_client[MONGODB_DB]
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    mongo_client = None
    mongo_db = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "analytics-service"})

@app.route('/api/analytics/patients/summary', methods=['GET'])
def patients_summary():
    try:
        with mysql_engine.connect() as conn:
            result = conn.execute(text("SELECT status, COUNT(*) as count FROM patients GROUP BY status"))
            rows = [{"status": r[0], "count": int(r[1])} for r in result]
            return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e), "data": []}), 500

@app.route('/api/analytics/visits/summary', methods=['GET'])
def visits_summary():
    try:
        with mysql_engine.connect() as conn:
            result = conn.execute(text("SELECT status, COUNT(*) as count FROM visits GROUP BY status"))
            rows = [{"status": r[0], "count": int(r[1])} for r in result]
            return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e), "data": []}), 500

@app.route('/api/analytics/performance', methods=['GET'])
def performance():
    try:
        with mysql_engine.connect() as conn:
            patient_total = conn.execute(text("SELECT COUNT(*) FROM patients")).scalar() or 0
            visit_total = conn.execute(text("SELECT COUNT(*) FROM visits")).scalar() or 0
            
            # Get today's visits
            today_visits = conn.execute(text("""
                SELECT COUNT(*) FROM visits 
                WHERE DATE(scheduled_time) = CURDATE()
            """)).scalar() or 0
            
            # Get critical patients
            critical_patients = conn.execute(text("""
                SELECT COUNT(*) FROM patients 
                WHERE status = 'Critical'
            """)).scalar() or 0
            
            return jsonify({"data": {
                "patients": int(patient_total),
                "visits": int(visit_total),
                "today_visits": int(today_visits),
                "critical_patients": int(critical_patients)
            }})
    except Exception as e:
        return jsonify({"error": str(e), "data": None}), 500

@app.route('/api/analytics/dashboard/stats', methods=['GET'])
def dashboard_stats():
    try:
        with mysql_engine.connect() as conn:
            # Total patients
            total_patients = conn.execute(text("SELECT COUNT(*) FROM patients")).scalar() or 0
            
            # Total visits
            total_visits = conn.execute(text("SELECT COUNT(*) FROM visits")).scalar() or 0
            
            # Today's visits
            today_visits = conn.execute(text("""
                SELECT COUNT(*) FROM visits 
                WHERE DATE(scheduled_time) = CURDATE()
            """)).scalar() or 0
            
            # Critical patients
            critical_patients = conn.execute(text("""
                SELECT COUNT(*) FROM patients 
                WHERE status = 'Critical'
            """)).scalar() or 0
            
            # Patients by status
            patients_by_status = conn.execute(text("""
                SELECT status, COUNT(*) as count 
                FROM patients 
                GROUP BY status
            """))
            patient_status_data = [{"status": r[0], "count": int(r[1])} for r in patients_by_status]
            
            # Visits by status
            visits_by_status = conn.execute(text("""
                SELECT status, COUNT(*) as count 
                FROM visits 
                GROUP BY status
            """))
            visit_status_data = [{"status": r[0], "count": int(r[1])} for r in visits_by_status]
            
            return jsonify({"data": {
                "overview": {
                    "total_patients": int(total_patients),
                    "total_visits": int(total_visits),
                    "today_visits": int(today_visits),
                    "critical_patients": int(critical_patients)
                },
                "patients_by_status": patient_status_data,
                "visits_by_status": visit_status_data
            }})
            
    except Exception as e:
        return jsonify({"error": str(e), "data": None}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)