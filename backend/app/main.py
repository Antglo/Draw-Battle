# backend/app/main.py

from fastapi import FastAPI
from app.api.routes import router as api_router

# Create FastAPI instance
app = FastAPI(title="Drawing Battle Game", version="1.0.0")

# Include API routes
app.include_router(api_router)

# Start point for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
