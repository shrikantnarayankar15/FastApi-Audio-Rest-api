
from fastapi import FastAPI
from database import models
from database import connection
from routers import audios

app = FastAPI()

models.Base.metadata.create_all(connection.engine)

app.include_router(audios.router)
