# Machine & Parts Management System API

This project is a **FastAPI-based backend** for managing machines and parts, using **Neo4j** as the database to store machines, parts, and their relationships.  
It supports:

- PDF uploads for part drawings
- Machine–part linking
- Inventory statistics

---

## **Tech Stack**

- **FastAPI** – Backend framework  
- **Neo4j** – Graph database  
- **Pydantic** – Data validation  
- **Uvicorn** – ASGI server  
- **python-dotenv** – Environment variable management  

---

## **Prerequisites**

- Python **3.8+**  
- Neo4j  
- Git  

---

## **Neo4j Database Setup**

1. Install **Neo4j Desktop**  
2. Create a new instance  
3. Start the database  
4. Note the **URI**, **username**, and **password**  
5. Create a `.env` file in the project root with the following variables:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

---

## **Starting the Application**

Run the following command:

```
uvicorn app.main:app --reload
```
