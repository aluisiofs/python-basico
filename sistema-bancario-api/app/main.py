from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.v1.router import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Sistema Bancário Corporativo NTT DATA",
    description="API assíncrona de microsserviço financeiro desenvolvida na Trilha Back-End Júnior.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["Infraestrutura"])
async def health_check():
    return {"status": "operacional", "servico": "sistema-bancario-api"}