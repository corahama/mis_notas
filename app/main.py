from fastapi import FastAPI

from .database import engine
from . import models
from .routers import note, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(note.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API!!!"}
