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


def test_get_all_request():
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


def test_get_all_visit():
    response = client.get("/visit/")

    assert response.status_code == 200

def test_post_visit():
    response = client.post("/visit/",json={
                                            "time": "2022-06-18T04:09:23.846Z",
                                            "doctor_db_id": 2,
                                            "patient_id": 2,
                                            "diagnosis": "string",
                                            "medicine": {
                                                "name": "paracetamol"
                                            }
                                        })

    assert response.status_code == 201
    assert response.json()["doctor_db_id"] == 2
    assert response.json()["patient_id"] == 2
    assert response.json()["diagnosis"] == "string"


def test_post_visit_error():
    response = client.post("/visit/",json={
                                            "time": "2022-06-18T04:09:23.846Z",
                                        })

    assert response.status_code == 422




def test_get_all_request():
    response = client.get("/request/")

    assert response.status_code == 200

def test_post_request():
    response = client.post("/request/",json={
                                            "time": "2022-06-18T05:18:52.734Z",
                                            "doctor_db_id": 1,
                                            "patient_id": 1,
                                            "status": "PENDING",
                                            "note": "string"
                                            })

    assert response.status_code == 201
    assert response.json()["doctor_db_id"] == 1
    assert response.json()["patient_id"] == 1
    assert response.json()["status"] == "PENDING"


def test_post_request_error():
    response = client.post("/request/",json={
                                            "time": "2022-06-18T04:09:23.846Z",
                                        })

    assert response.status_code == 422
