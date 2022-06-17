import models
from fastapi import FastAPI
from database import engine
from routers import medicine, visit, request, patient, doctor
from schemas import Settings
from fastapi_jwt_auth import AuthJWT

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(visit.router)
app.include_router(request.router)
app.include_router(medicine.router)
