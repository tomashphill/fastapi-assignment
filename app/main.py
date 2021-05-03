from fastapi import FastAPI

from .dependencies import get_logger
from .routers import tags


app = FastAPI()

app.include_router(tags.router)
