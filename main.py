from db import Base, engine
from fastapi import FastAPI
from api.users import user_router
from api.workers import worker_router
from api.post import worker_post_router

Base.metadata.create_all(engine)

app = FastAPI(docs_url="/")

app.include_router(user_router)
app.include_router(worker_post_router)
app.include_router(worker_router)

