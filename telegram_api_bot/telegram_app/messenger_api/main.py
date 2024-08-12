from fastapi import FastAPI
from api.routers import router as Telegram

app = FastAPI()
app.include_router(router=Telegram, prefix='')
