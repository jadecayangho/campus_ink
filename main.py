from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as orders_router
from pricing import get_all_prices

app = FastAPI(
    title="Campus Printing Management System",
    description="A system to manage printing orders and costs for a campus printing shop",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router)


@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Campus Printing Management System",
        "version": "1.0.0",
        "endpoints": {
            "orders": "/api/orders",
            "pricing": "/pricing",
            "docs": "/docs"
        }
    }


@app.get("/pricing")
def get_pricing():
    """Get all printing prices"""
    return get_all_prices()


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Campus Printing Management System"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
