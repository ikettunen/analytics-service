from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.mysql import get_mysql_session
from app.db.mongo import get_mongo_db

router = APIRouter()

@router.get("/patients/summary")
async def patients_summary(db: Session = Depends(get_mysql_session)):
    # Get patient count by status from MySQL
    result = db.execute("SELECT status, COUNT(*) as count FROM patients GROUP BY status")
    rows = [{"status": r[0], "count": int(r[1])} for r in result]
    return {"data": rows}

@router.get("/visits/summary")
async def visits_summary(db: Session = Depends(get_mysql_session)):
    # Get visits summary from MySQL visits table
    result = db.execute("SELECT status, COUNT(*) as count FROM visits GROUP BY status")
    rows = [{"status": r[0], "count": int(r[1])} for r in result]
    return {"data": rows}

@router.get("/patients/critical")
async def patients_critical(db: Session = Depends(get_mysql_session)):
    # Get count of patients with critical status
    result = db.execute("SELECT COUNT(*) as count FROM patients WHERE status = 'Critical'")
    count = result.scalar() or 0
    return {"data": {"critical_patients": int(count)}}

@router.get("/performance")
async def performance(db: Session = Depends(get_mysql_session)):
    # Get comprehensive stats from MySQL
    patient_total = db.execute("SELECT COUNT(*) FROM patients").scalar() or 0
    visit_total = db.execute("SELECT COUNT(*) FROM visits").scalar() or 0
    
    # Get today's visits
    today_visits = db.execute("""
        SELECT COUNT(*) FROM visits 
        WHERE DATE(scheduled_time) = CURDATE()
    """).scalar() or 0
    
    # Get critical patients
    critical_patients = db.execute("""
        SELECT COUNT(*) FROM patients 
        WHERE status = 'Critical'
    """).scalar() or 0
    
    return {"data": {
        "patients": int(patient_total),
        "visits": int(visit_total),
        "today_visits": int(today_visits),
        "critical_patients": int(critical_patients)
    }}

@router.get("/dashboard/stats")
async def dashboard_stats(db: Session = Depends(get_mysql_session)):
    # Get all dashboard statistics in one call
    try:
        # Total patients
        total_patients = db.execute("SELECT COUNT(*) FROM patients").scalar() or 0
        
        # Total visits
        total_visits = db.execute("SELECT COUNT(*) FROM visits").scalar() or 0
        
        # Today's visits
        today_visits = db.execute("""
            SELECT COUNT(*) FROM visits 
            WHERE DATE(scheduled_time) = CURDATE()
        """).scalar() or 0
        
        # Critical patients
        critical_patients = db.execute("""
            SELECT COUNT(*) FROM patients 
            WHERE status = 'Critical'
        """).scalar() or 0
        
        # Patients by status
        patients_by_status = db.execute("""
            SELECT status, COUNT(*) as count 
            FROM patients 
            GROUP BY status
        """)
        patient_status_data = [{"status": r[0], "count": int(r[1])} for r in patients_by_status]
        
        # Visits by status
        visits_by_status = db.execute("""
            SELECT status, COUNT(*) as count 
            FROM visits 
            GROUP BY status
        """)
        visit_status_data = [{"status": r[0], "count": int(r[1])} for r in visits_by_status]
        
        return {"data": {
            "overview": {
                "total_patients": int(total_patients),
                "total_visits": int(total_visits),
                "today_visits": int(today_visits),
                "critical_patients": int(critical_patients)
            },
            "patients_by_status": patient_status_data,
            "visits_by_status": visit_status_data
        }}
        
    except Exception as e:
        return {"error": str(e), "data": None}

@router.get("/staff/{staff_id}/tasks/today")
async def staff_tasks_today(staff_id: str, mongo_db = Depends(get_mongo_db)):
    # Get staff tasks for today from MongoDB visit_data collection
    try:
        from datetime import datetime, timedelta
        
        # Get today's date range
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Query MongoDB for visits assigned to this staff member today
        visits_collection = mongo_db.visit_data
        
        # Find all visits for this staff member today
        visits = list(visits_collection.find({
            "assignedStaffId": staff_id,
            "scheduledTime": {
                "$gte": today_start,
                "$lt": today_end
            }
        }))
        
        # Calculate task statistics
        total_tasks = 0
        completed_tasks = 0
        pending_tasks = 0
        high_priority_pending = 0
        total_visits = len(visits)
        
        for visit in visits:
            tasks = visit.get("tasks", [])
            total_tasks += len(tasks)
            
            for task in tasks:
                if task.get("status") == "completed":
                    completed_tasks += 1
                else:
                    pending_tasks += 1
                    if task.get("priority") == "high":
                        high_priority_pending += 1
        
        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {"data": {
            "totalTasks": total_tasks,
            "completedTasks": completed_tasks,
            "pendingTasks": pending_tasks,
            "highPriorityPending": high_priority_pending,
            "totalVisits": total_visits,
            "completionRate": round(completion_rate, 1)
        }}
        
    except Exception as e:
        return {"error": str(e), "data": None}
