from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.review import router as review_router
from app.api.routes.repository import (
    router as repository_router
)
from app.repository.db import Base
from app.repository.db import engine

from app.repository import models


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_router)
app.include_router(repository_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}