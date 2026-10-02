from fastapi import APIRouter
from wasteos_api.api.v1 import (
    health, auth, waste, pickups, scanning, passports,
    marketplace, reports, hotspots, municipality, rewards,
    forecasting, routes, e_waste, medical_waste, food_waste, advisory,
    facilities, vehicles, wards, waste_types, users, organizations,
    citizens, notifications, analytics, classification, assistant, purchases,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(waste.router, prefix="/waste", tags=["waste"])
api_router.include_router(pickups.router, prefix="/pickups", tags=["pickups"])
api_router.include_router(scanning.router, prefix="/scanning", tags=["scanning"])
api_router.include_router(passports.router, prefix="/passports", tags=["passports"])
api_router.include_router(marketplace.router, prefix="/marketplace", tags=["marketplace"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(hotspots.router, prefix="/hotspots", tags=["hotspots"])
api_router.include_router(municipality.router, prefix="/municipality", tags=["municipality"])
api_router.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
api_router.include_router(forecasting.router, prefix="/forecasting", tags=["forecasting"])
api_router.include_router(routes.router, prefix="/routes", tags=["routes"])
api_router.include_router(e_waste.router, prefix="/e-waste", tags=["special-waste"])
api_router.include_router(medical_waste.router, prefix="/medical-waste", tags=["special-waste"])
api_router.include_router(food_waste.router, prefix="/food-waste", tags=["special-waste"])
api_router.include_router(advisory.router, prefix="/advisory", tags=["ai"])
api_router.include_router(facilities.router, prefix="/facilities", tags=["facilities"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["municipality"])
api_router.include_router(wards.router, prefix="/wards", tags=["municipality"])
api_router.include_router(waste_types.router, prefix="/waste-types", tags=["admin"])
api_router.include_router(users.router, prefix="/admin/users", tags=["admin"])
api_router.include_router(organizations.router, prefix="/admin/organizations", tags=["admin"])
api_router.include_router(citizens.router, prefix="/citizens", tags=["citizens"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(classification.router, prefix="/classification", tags=["ai"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["ai"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["marketplace"])
