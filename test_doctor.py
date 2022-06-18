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

#Doctor
def test_get_all_doctor():
    response = client.get("/doctor/")
    assert response.status_code == 200

def test_post_doctor():
    response = client.post("/doctor/", json={
                                                "name": "Sugeng",
                                                "birthdate": "1970-06-12",
                                                "gender": "Male",
                                                "address": "Jakarta",
                                                "telephone": "0218861234",
                                                "id_kki": "123",
                                                "specialist": "Jantung"
                                            })

    assert response.status_code == 200
    assert type(response.json()["id"]) == type(14) #integer
    assert response.json()["name"] == "Sugeng"
    assert response.json()["birthdate"] == "1970-06-12"
    assert response.json()["gender"] == "Male"
    assert response.json()["address"] == "Jakarta"
    assert response.json()["telephone"] == "0218861234"
    assert response.json()["id_kki"] == "123"
    assert response.json()["specialist"] == "Jantung"


def test_post_doctor_error():
    response = client.post("/doctor/", json={"name": "Sugeng",
                                            "birthdate": "1970-06-12"})

    assert response.status_code == 422

def test_get_one_doctor():
    response = client.get("/doctor/3")

    assert response.status_code == 200
    assert response.json()["id"] is 3

def test_get_one_doctor_error():
    response = client.get("/doctor/1945")

    assert response.status_code == 404

def test_put_one_doctor():
    response = client.put("/doctor/update/2", json={
                                        "name": "put",
                                        "birthdate": "2000-06-18",
                                        "gender": "string",
                                        "address": "string",
                                        "telephone": "string",
                                        "id_kki": "string",
                                        "specialist": "string"
                                        })

    assert response.status_code == 200
    assert type(response.json()["id"]) == type(14) #integer
    assert response.json()["name"] == "put"
    assert response.json()["birthdate"] == "2000-06-18"
    assert response.json()["gender"] == "string"
    assert response.json()["address"] == "string"
    assert response.json()["telephone"] == "string"
    assert response.json()["id_kki"] == "string"
    assert response.json()["specialist"] == "string"

