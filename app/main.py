from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.analytics import router as analytics_router
from app.core.config import settings

app = FastAPI(
    title="Analytics Service API",
    description="Aggregates analytics from MySQL and MongoDB",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "analytics-service"}

app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
