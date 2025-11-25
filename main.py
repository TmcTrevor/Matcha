from contextlib import asynccontextmanager
from typing import Annotated
from asyncpg import Connection
from fastapi import Depends, FastAPI

from src.database.connection_db import connection

connection_dep = Annotated[Connection, Depends(connection.get_connection)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connection.init_connection()
    yield
    await connection.close_connection()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def say_hello():
    return {"message": "hello Matha"}
