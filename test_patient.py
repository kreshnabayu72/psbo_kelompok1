from fastapi.testclient import TestClient 
import models
from fastapi import FastAPI
from database import engine
from routers import medicine, visit, request, patient, doctor
from schemas import Settings
from fastapi_jwt_auth import AuthJWT
import json
from .main import app

client = TestClient(app)

#Patient
def test_get_all_patient():
    response = client.get("/patient/")
    assert response.status_code == 200

def test_post_patient():
    response = client.post("/patient/", json={"name": "Sutrisno",
                                            "birthdate": "1960-06-18",
                                            "gender": "Male",
                                            "address": "Jalan Apel",
                                            "telephone": "081311112234",
                                            "email": "Sut@gmail.com",
                                            "insurance": "BPJS",
                                            "password": "string"})

    assert response.status_code == 200
    assert type(response.json()["id"]) == type(14) #integer
    assert response.json()["name"] == "Sutrisno"
    assert response.json()["birthdate"] == "1960-06-18"
    assert response.json()["gender"] == "Male"
    assert response.json()["address"] == "Jalan Apel"
    assert response.json()["telephone"] == "081311112234"
    assert response.json()["email"] == "Sut@gmail.com"
    assert response.json()["insurance"] == "BPJS"

def test_post_patient_error():
    response = client.post("/patient/", json={"name": "string",
                                            "password": "string"})

    assert response.status_code == 422

def test_get_visit_patient():
    response = client.get("/patient/visit-list-auth/")

    assert response.status_code == 401

