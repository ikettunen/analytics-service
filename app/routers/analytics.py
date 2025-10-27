from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.mysql import get_mysql_session
from app.db.mongo import get_mongo_db

router = APIRouter()

@router.get("/patients/summary")
async def patients_summary(db: Session = Depends(get_mysql_session)):
    # Example: count patients by status from MySQL
    result = db.execute("SELECT status, COUNT(*) as count FROM patients GROUP BY status")
    rows = [{"status": r[0], "count": int(r[1])} for r in result]
    return {"data": rows}

@router.get("/visits/summary")
async def visits_summary(mongo = Depends(get_mongo_db)):
    # Example: count visits by status from MongoDB 'visits' collection
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        {"$project": {"status": "$_id", "count": 1, "_id": 0}},
    ]
    cursor = mongo["visits"].aggregate(pipeline)
    rows = [doc async for doc in cursor]
    return {"data": rows}

@router.get("/performance")
async def performance(db: Session = Depends(get_mysql_session), mongo = Depends(get_mongo_db)):
    # Basic combined stats for example purposes
    patient_total = db.execute("SELECT COUNT(*) FROM patients").scalar() or 0
    visit_total = await mongo["visits"].count_documents({})
    return {"data": {"patients": int(patient_total), "visits": int(visit_total)}}
