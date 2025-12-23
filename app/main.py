from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app import models, services
import os


app = FastAPI(title="Machine & Parts Management System")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])



# ---------- 1. Part Endpoints ----------
@app.post("/parts/", response_model=models.PartResponse, tags=["Parts"])
async def create_part(
    name: str = Form(...),
    number: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a new part with a PDF drawing.
    The UUID is generated and used as the filename.
    """
    part_data = models.PartBase(name=name, number=number, description=description)
    return services.create_part(part_data, file)


@app.get("/parts/{part_number}", response_model=models.PartResponse, tags=["Parts"])
async def get_part(part_number: str):
    """Retrieve part details using the unique part number."""
    return services.get_part_by_number(part_number)


@app.get("/parts/{part_uuid}/drawing", tags=["Parts"])
async def get_part_drawing(part_uuid: str):
    """
    Retrieve the PDF drawing for a specific part by its UUID.
    """
    file_path = f"static/part/{part_uuid}.pdf"

    # Check if the file actually exists on the disk
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Drawing not found on server")

    # Return the file as a PDF
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{part_uuid}.pdf",
        headers={"Content-Disposition": "inline"}, #remove if we want the file to directly download
    )


# ---------- 2. Machine Endpoints ----------
@app.post("/machines/", response_model=models.MachineResponse, tags=["Machines"])
async def create_machine(machine: models.MachineBase):
    """Create a new machine record."""
    return services.create_machine(machine)


# ---------- 3. Relationship Endpoints ----------
@app.post("/machines/associate", tags=["Relationships"])
async def associate_part_with_machine(machine_name: str, part_number: str):
    """
    Link an existing part to an existing machine.
    Logic: (Part)-[:BELONGS_TO]->(Machine)
    """
    return services.associate_machine_with_part(machine_name, part_number)


# ---------- 4. Health Check ----------
@app.get("/", tags=["System"])
async def root():
    return {"message": "Neo4j Machine-Parts API is running"}

# ---------- 5. Inventory Stats ----------
@app.get("/inventory/stats", tags=["System"])
async def get_stats():
    return services.get_inventory_stats()

