from fastapi import FastAPI

from .telegram.adapter import router as telegram_router
from .whatsapp.adapter import router as whatsapp_router

app = FastAPI(title="Ankara Bots", version="0.1.0")
app.include_router(whatsapp_router)
app.include_router(telegram_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
