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


def test_get_all_medicine():
    response = client.get("/medicine/")
    assert response.status_code == 200

def test_post_medicine():
    response = client.post("/medicine/", json={
                                                "name": "string",
                                                "efficacy": "string",
                                                "side_effect": "string"
                                                })

    assert response.status_code == 200
    assert type(response.json()["id"]) == type(14) #integer
    assert response.json()["name"] == "string"
    assert response.json()["efficacy"] == "string"
    assert response.json()["side_effect"] == "string" 

def test_get_one_medicine():
    response = client.get("/medicine/1")
    assert response.status_code == 200
    assert response.json()["id"] is 1

def test_put_one_medicine():
    response = client.put("/medicine/update/10", json={
  "name": "paracetamol",
  "efficacy": "string",
  "side_effect": "string"
})

    assert response.status_code == 200
    assert type(response.json()["id"]) == type(14) #integer
    assert response.json()["name"] == "paracetamol"
    assert response.json()["efficacy"] == "string"
    assert response.json()["side_effect"] == "string"

def test_delete_one_medicine():
    response = client.delete("/medicine/delete/15")

    assert response.status_code == 200