import pytest
from fastapi.testclient import TestClient
from main import app
import logging
from dotenv import load_dotenv
import os

load_dotenv('params.env')
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "default_token")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TestClient(app)


@pytest.fixture
def auth_header():
    return {"Authorization": f"Bearer {AUTH_TOKEN}"}


def test_get_all_nodes():
    response = client.get("/nodes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_node_and_relations():
    node_id = 44444444
    response = client.get(f"/nodes/{node_id}")
    assert response.status_code == 200


def test_insert_node_and_relationships(auth_header):
    test_data = {
        "node": {
            "uid": 7777777,
            "label": "User",
            "name": "Тестер",
            "screen_name": "tester",
            "sex": 1,
            "home_town": "Gorod"
        },
        "relationships": [
            {
                "type": "Follow",
                "target_id": 161123875
            }
        ]
    }

    response = client.post("/nodes", json=test_data, headers=auth_header)
    assert response.status_code == 200


def test_delete_node_and_relationships(auth_header):
    node_id = 44444444
    response = client.delete(f"/nodes/{node_id}", headers=auth_header)
    assert response.status_code == 200
