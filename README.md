# Analytics Service

FastAPI microservice aggregating analytics from MySQL and MongoDB.

## Environment Variables

Create `.env`:

```
MYSQL_DSN=mysql://user:password@mysql:3306/nursing_home
MONGODB_URI=mongodb://mongo:27017
MONGODB_DB=analytics
DEBUG=false
```

## Run locally

```
pip install -r requirements.txt
pip install -r requirements.txt
uvicorn app.main:app --reload --port 3005
```

Docs: http://localhost:3005/api-docs

## Docker

```
docker build -t analytics-service:latest .
docker run -p 3005:3005 --env-file .env analytics-service:latest
```
