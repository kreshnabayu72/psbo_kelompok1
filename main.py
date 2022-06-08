import models
from fastapi import FastAPI
from database import engine
from routers import appointment, person, auth, visit, request

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(appointment.router)
app.include_router(person.router)
app.include_router(visit.router)
app.include_router(request.router)
