import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from neomodel import config
import os
from dotenv import load_dotenv
from model import *
from data_service import DataService

load_dotenv('params.env')

config.DATABASE_URL = os.getenv("NEO4J_CONNECTION_STRING", "bolt://neo4j:password@localhost:7687")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
APP_HOST = os.getenv("APP_HOST", "localhost")

app = FastAPI()

bearer_scheme = HTTPBearer()
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "default_token")


def authorize(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/nodes")
def get_all_nodes():
    return DataService.get_all_nodes()


@app.get("/nodes/{node_id}")
def get_node_with_relationships(node_id: str):
    return DataService.get_node_with_relationships(node_id)


@app.post("/nodes", dependencies=[Depends(authorize)], response_model=None)
def add_node_and_relationships(node_data: NodeCreate):
    try:
        DataService.add_node_and_relationships(node_data)
        return {"message": "Node and relationships added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/nodes/{node_id}", dependencies=[Depends(authorize)])
def delete_segment(node_id):
    try:
        DataService.delete_node(node_id)
        return {"message": "Nodes and relationships deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=APP_HOST,
        port=APP_PORT
    )

# Deployment Instructions
# 1. Install dependencies: `pip install fastapi uvicorn neomodel`.
# 2. Set up Neo4j and ensure the database is running.
# 3. Set the `NEO4J_DATABASE_URL` and `AUTH_TOKEN` environment variables.
# 4. Start the application: `uvicorn app:app --host 0.0.0.0 --port 8000`.

# Running Tests
# 1. Install pytest: `pip install pytest`.
# 2. Write tests in a `tests` folder (example below).
# 3. Run tests: `pytest tests`.
