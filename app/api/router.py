"""
ERP Platform — Main API Router

Routes must remain thin.
"""

from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.sales import router as sales_router

api_router = APIRouter()

# Include health check routes
api_router.include_router(health_router)

# Include authentication routes
api_router.include_router(auth_router)

# Include domain routers
api_router.include_router(sales_router)

# Future: include domain routers here
# api_router.include_router(users_router, prefix="/users", tags=["users"])
# api_router.include_router(products_router, prefix="/products", tags=["products"])
