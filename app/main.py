from fastapi import FastAPI
from app.routers import (
    system,
    recipes as recipes_router,
    recommendations,
)
app = FastAPI()


app.include_router(system.router)
app.include_router(recipes_router.router)
app.include_router(recommendations.router)
