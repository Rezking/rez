from fastapi import APIRouter
from routers.Text_detection.readText import Text_router

router = APIRouter()

router.include_router(Text_router)
