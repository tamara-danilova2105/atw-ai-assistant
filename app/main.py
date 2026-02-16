from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="ATW AI Assistant")
app.include_router(router)

