import models
from fastapi import FastAPI
from database import engine
from routers import blog, person, auth, visit

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(person.router)
app.include_router(visit.router)
