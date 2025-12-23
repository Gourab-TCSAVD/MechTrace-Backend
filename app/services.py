import uuid
import shutil
from pathlib import Path
from fastapi import HTTPException, UploadFile
from .db import neo4j_connection
from .models import PartBase, PartResponse, MachineBase, MachineResponse

# Storage Configuration
UPLOAD_DIR = Path("static/part")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ---------- 1. Create Part with File Upload ----------
def create_part(part: PartBase, file: UploadFile) -> PartResponse:
    # Step 1: Manually generate UUID
    part_uuid = str(uuid.uuid4())

    if not file.filename.lower().endswith(".pdf"):  # type: ignore
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Step 2: Save to Neo4j
    query = """
    CREATE (p:Part {
        uuid: $uuid, 
        name: $name, 
        number: $number, 
        description: $description
    })
    RETURN p
    """
    params = {
        "uuid": part_uuid,
        "name": part.name,
        "number": part.number,
        "description": part.description,
    }

    with neo4j_connection.get_session() as session:
        result = session.run(query, params)
        record = result.single()
        if not record:
            raise HTTPException(
                status_code=500, detail="Failed to create part in database"
            )

        node = record["p"]

        # Step 3: Handle File Storage using UUID
        file_path = UPLOAD_DIR / f"{part_uuid}.pdf"
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Could not save file: {str(e)}"
            )

        return PartResponse(
            uuid=node["uuid"],
            name=node["name"],
            number=node["number"],
            description=node["description"],
        )


# ---------- 2. Create Machine ----------
def create_machine(machine: MachineBase) -> MachineResponse:
    machine_uuid = str(uuid.uuid4())
    query = """
    CREATE (m:Machine {
        uuid: $uuid, 
        name: $name, 
        site: $site, 
        description: $description
    })
    RETURN m
    """
    params = {
        "uuid": machine_uuid,
        "name": machine.name,
        "site": machine.site,
        "description": machine.description,
    }

    with neo4j_connection.get_session() as session:
        result = session.run(query, params)
        record = result.single()
        node = record["m"]  # type: ignore

        return MachineResponse(
            uuid=node["uuid"],
            name=node["name"],
            site=node["site"],
            description=node["description"],
        )


# ---------- 3. Associate Machine with Part ----------
def associate_machine_with_part(machine_name: str, part_number: str):
    # Using MERGE for the relationship to avoid duplicates
    query = """
    MATCH (m:Machine {name: $m_name})
    MATCH (p:Part {number: $p_num})
    MERGE (p)-[r:BELONGS_TO]->(m)
    RETURN m, p
    """
    params = {"m_name": machine_name, "p_num": part_number}

    with neo4j_connection.get_session() as session:
        result = session.run(query, params)
        record = result.single()

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Machine or Part not found. Ensure Machine name and Part number are correct.",
            )

    return {
        "message": f"Part '{part_number}' successfully linked to Machine '{machine_name}'."
    }


# ---------- 4. Get Part by Part Number ----------
def get_part_by_number(part_number: str) -> PartResponse:
    query = """
    MATCH (p:Part {number: $number})
    RETURN p
    """
    with neo4j_connection.get_session() as session:
        result = session.run(query, number=part_number)
        record = result.single()

        if not record:
            raise HTTPException(status_code=404, detail="Part not found")

        node = record["p"]
        return PartResponse(
            uuid=node["uuid"],
            name=node["name"],
            number=node["number"],
            description=node["description"],
        )


# ---------- 5. Get Inventory Stats ----------
def get_inventory_stats():
    query = """
    CALL {
        MATCH (m:Machine) RETURN count(m) as machineCount
    }
    CALL {
        MATCH (p:Part) RETURN count(p) as partCount
    }
    CALL {
        MATCH (p:Part) WHERE NOT (p)-[:BELONGS_TO]->() RETURN count(p) as unlinkedCount
    }
    RETURN machineCount, partCount, unlinkedCount
    """
    with neo4j_connection.get_session() as session:
        result = session.run(query)
        record = result.single()
        return {
            "total_machines": record["machineCount"], # type: ignore
            "total_parts": record["partCount"], # type: ignore
            "unlinked_parts": record["unlinkedCount"], # type: ignore
        }

# ---------- 6. Get Parts based on machine and site ----------
def get_machine_with_parts(name: str, site: str):
    # This query finds the machine and collects all related parts into a list
    query = """
    MATCH (m:Machine {name: $name, site: $site})
    OPTIONAL MATCH (p:Part)-[:BELONGS_TO]->(m)
    RETURN m, collect(p) as parts
    """
    params = {"name": name, "site": site}

    with neo4j_connection.get_session() as session:
        result = session.run(query, params)
        record = result.single()

        if not record or not record["m"]:
            return None

        machine_node = record["m"]
        parts_nodes = record["parts"]

        return {
            "uuid": machine_node["uuid"],
            "name": machine_node["name"],
            "site": machine_node["site"],
            "description": machine_node.get("description", ""),
            "parts": [
                {
                    "uuid": p["uuid"],
                    "name": p["name"],
                    "number": p["number"],
                    "description": p.get("description", "")
                }
                for p in parts_nodes if p is not None
            ]
        }
