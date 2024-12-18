from pydantic import BaseModel


class Node(BaseModel):
    uid: int
    label: str
    name: str
    screen_name: str
    sex: int
    home_town: str


class Relationship(BaseModel):
    type: str
    target_id: int


class NodeCreate(BaseModel):
    node: Node = None
    relationships: list[Relationship] = []  # Example: [{"target_id": "node2", "type": "RELATES_TO"}]
