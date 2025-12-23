# Machine & Parts Management System API

This project is a FastAPI-based backend for managing machines and parts, using Neo4j as the database to store machines, parts, and their relationships. It supports PDF uploads for part drawings, machine–part linking, and inventory statistics.

---

## Tech Stack

- **FastAPI** – Backend framework
- **Neo4j** – Graph database
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server
- **Python Dotenv** – Environment variable management

---

## Prerequisites

- Python **3.8+**
- Neo4j
- Git

---
## Neo4j Database Setup

- Install Neo4j Desktop
- Create a new Instance
- Start the database
- Note the URI, username, and password
- Create a .env file in the project root:
**NEO4J_URI=bolt://localhost:7687**
**NEO4J_USER=neo4j**
**NEO4J_PASSWORD=password**

---
## Starting the application

**uvicorn app.main:app --reload**