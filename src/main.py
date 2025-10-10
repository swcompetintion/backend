
from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from src.database.connection import initialize_database
from .routes.plans import plan_router
from .routes.auths import auth_router
from .routes.users import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await initialize_database()
    yield


app = FastAPI(
    lifespan=lifespan
)


origins = [
    "http://localhost:3002",
    "https://www.bed-rock.p-e.kr",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(plan_router)
app.include_router(auth_router)
app.include_router(user_router)
