Added a FastAPI-based analytics microservice at backend_cursor/analytics-service with Docker support.
What you have:
App entry: app/main.py with /health and /api/analytics routes
Config: app/core/config.py using .env for DB URIs
DB connectors:
MySQL via SQLAlchemy: app/db/mysql.py
MongoDB via Motor: app/db/mongo.py
Routers: app/routers/analytics.py
GET /api/analytics/patients/summary: counts patients by status (MySQL)
GET /api/analytics/visits/summary: counts visits by status (MongoDB)
GET /api/analytics/performance: combined totals (MySQL+Mongo)
Containerization:
Dockerfile
requirements.txt
README.md with env and run instructions
Build and run:
Create backend_cursor/analytics-service/.env:
MYSQL_DSN=mysql://user:password@mysql:3306/nursing_home
MONGODB_URI=mongodb://mongo:27017
MONGODB_DB=analytics
DEBUG=false
Local:
pip install -r requirements.txt
uvicorn app.main:app --port 3005
Docker:
docker build -t analytics-service:latest .
docker run -p 3005:3005 --env-file .env analytics-service:latest
Endpoints to test:
GET http://localhost:3005/health
GET http://localhost:3005/api/analytics/patients/summary
GET http://localhost:3005/api/analytics/visits/summary
GET http://localhost:3005/api/analytics/performance