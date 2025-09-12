from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.database import engine
from .app import models
from .app.routers import auth, books, loans

# TODO: Create database tables
# models.Base.metadata.create_all(bind=engine)

# TODO: Create FastAPI app instance
app = FastAPI(
    title="Library Management API",
    description="A REST API for managing an online library system",
    version="1.0.0"
)

# TODO: Configure CORS middleware
# app.add_middleware(...)

# TODO: Include routers
# app.include_router(auth.router)
# app.include_router(books.router)
# app.include_router(loans.router)

@app.get("/")
def read_root():
    """Root endpoint"""
    # TODO: Return welcome message
    pass

@app.get("/health")
def health_check():
    """Health check endpoint"""
    # TODO: Return health status
    pass

if __name__ == "__main__":
    # TODO: Configure uvicorn server
    pass