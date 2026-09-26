"""
ERP Platform — Main API Router

Routes must remain thin.
"""

from fastapi import APIRouter

from app.api.health import router as health_router

api_router = APIRouter()

# Include health check routes
api_router.include_router(health_router)

# Future: include domain routers here
# api_router.include_router(users_router, prefix="/users", tags=["users"])
# api_router.include_router(products_router, prefix="/products", tags=["products"])
