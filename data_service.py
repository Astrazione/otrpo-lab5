from neomodel import db
from fastapi import HTTPException
from model import *


class DataService:
    @staticmethod
    def get_all_nodes():
        query = "MATCH (n) RETURN id(n) AS id, labels(n)[0] AS label"
        results, _ = db.cypher_query(query)
        nodes = [{"id": node, "label": label} for (node, label) in results]
        return nodes

    @staticmethod
    def get_node_with_relationships(node_id):
        query = f"MATCH (n {{id: {node_id}}}) OPTIONAL MATCH (n)-[r]->(m) RETURN n, collect(r), collect(m)"

        results, _ = db.cypher_query(query, {"node_id": node_id})
        if not results:
            raise HTTPException(status_code=404, detail='Node not found')

        node, relationships, related_nodes = results[0]
        relationships = [relationship.type for relationship in relationships]
        return {
            "node": node,
            "relationships": relationships,
            "related_nodes": related_nodes,
        }

    @staticmethod
    def add_node_and_relationships(node_data: NodeCreate):
        node = node_data.node

        create_node_query = """
            CREATE (n:{label} {{
                id: $id, name: $name, screen_name: $screen_name,
                sex: $sex, home_town: $home_town
            }})
        """

        db.cypher_query(create_node_query.format(label=node.label), {
            "id": node.uid,
            "name": node.name,
            "screen_name": node.screen_name,
            "sex": node.sex,
            "home_town": node.home_town
        })

        try:
            if not node_data.relationships:
                return

            for rel in node_data.relationships:
                rel_query = ('MATCH (n {id: $id}), (m {id: $target_id})\n' +
                             f'CREATE (n)-[r: {rel.type}]->(m)')

                db.cypher_query(rel_query, {
                    "id": node.uid,
                    "target_id": rel.target_id,
                })
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def delete_node(node_id):
        query = """
        MATCH (n1)-[r]-(n2)
        WHERE id(n1) = $id
        DELETE r, n1
        """
        db.cypher_query(query, {"id": node_id})
