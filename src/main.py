
from fastapi import FastAPI
from contextlib import asynccontextmanager
# CORS 미들웨어를 임포트합니다.
from fastapi.middleware.cors import CORSMiddleware

from src.database.connection import initialize_database
from .routes.plans import plan_router
from .routes.auths import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 데이터베이스 초기화는 애플리케이션 시작 시 한 번만 수행됩니다.
    await initialize_database()
    yield
    # 애플리케이션 종료 시 필요한 정리 작업이 있다면 여기에 추가합니다.


app = FastAPI(
    lifespan=lifespan
)


origins = [
    "http://127.0.0.1:8000",
    "http://localhost:3002",
    "http://13.223.42.90:3000",
    "http://13.223.42.90:8000",
    "https://13.223.42.90:3000",
    "https://13.223.42.90:8000"
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
