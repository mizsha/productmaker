import requests
import pytest

SERVER = "http://localhost:5000/v1/"


def test_healthcheck():
    _response = requests.get(SERVER + 'system/healthcheck')
    assert _response.status_code == 200


def test_products():
    _response = requests.get(SERVER + 'products')
    assert _response.status_code == 200
