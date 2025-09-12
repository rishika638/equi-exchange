from fastapi import FastAPI
from .routes import router
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EquiExchange Backend")

@app.get("/")
def root():
    return {"message": "EquiExchange API is running 🚀"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)



