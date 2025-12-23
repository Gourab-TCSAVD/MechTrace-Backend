# Machine & Parts Management System API

This project provides a **FastAPI-based backend** for managing machines and parts, utilizing **Neo4j** as the database to store machines, parts, and their relationships. The system supports:

* Uploading PDF drawings for parts
* Linking parts to machines
* Inventory statistics and reporting

## **Tech Stack**

* **FastAPI**: Backend framework
* **Neo4j**: Graph database
* **Pydantic**: Data validation
* **Uvicorn**: ASGI server
* **python-dotenv**: Environment variable management

## **Prerequisites**

* Python **3.8+**
* Neo4j (installed locally or on a remote server)
* Git (for version control)

## **Setting Up Neo4j Database**

1. Install **Neo4j Desktop**.
2. Create a new instance.
3. Start the Neo4j database instance.
4. Retrieve the **URI**, **username**, and **password**.
5. Create a `.env` file in the project root directory with the following variables:

   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=password
   ```

## **Installation**

1. Clone this repository.
2. Install dependencies from `requirements.txt`:

   ```
   pip install -r requirements.txt
   ```

## **Starting the Application**

Start the application using Uvicorn:

```
uvicorn main:app --reload
```

The application will run on `http://localhost:8000` by default.

## **API Endpoints**

### **Part Endpoints**

* **Create a Part**: `POST /parts/`

  * Upload part details with a PDF file.
* **Get Part by Number**: `GET /parts/{part_number}`

  * Retrieve details of a part by its unique number.
* **Get Part Drawing**: `GET /parts/{part_uuid}/drawing`

  * Retrieve the PDF drawing for a part.
* **List All Parts**: `GET /parts/`

  * List all parts with optional filters (linked or unlinked to machines).

### **Machine Endpoints**

* **Create a Machine**: `POST /machines/`

  * Add a new machine record.
* **Get Machine Details**: `GET /machines/details`

  * Retrieve machine and its associated parts using name and site.
* **List All Machines**: `GET /machines/`

  * List all machines with their part counts.

### **Relationship Endpoints**

* **Associate a Part with a Machine**: `POST /machines/associate`

  * Link an existing part to an existing machine.

### **Health Check**

* **System Health**: `GET /`

  * Check if the API is running.

### **Inventory Statistics**

* **Get Inventory Stats**: `GET /inventory/stats`

  * View statistics about the machines and parts, including linked/unlinked parts.

## **File Storage**

* PDF files for parts are stored under the `static/part` directory.
* Each part's file is saved with its UUID as the filename.

## **Database Queries**

The application uses **Neo4j** to store and manage the relationships between machines and parts. Key queries include:

* Creating parts and machines.
* Linking parts to machines.
* Retrieving machine details with associated parts.
* Generating inventory statistics, including linked and unlinked parts.
