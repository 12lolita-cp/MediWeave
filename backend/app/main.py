from fastapi import FastAPI
from app.api.v1.routers.pharmacies import router as pharmacies_router

app = FastAPI(
    title="MediWeave",
    description="Pharmacy Inventory Interoperability and Intelligence Platform",
    version="1.0.0"
)

app.include_router(
    pharmacies_router,
    prefix="/api/v1"
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "MediWeave"
    }