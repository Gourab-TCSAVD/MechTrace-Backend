from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Part Models ---
class PartBase(BaseModel):
    name: str
    number: str
    description: Optional[str] = None

class PartResponse(PartBase):
    uuid: str
    linked_machine: str | None = None  # Add this line


# --- Machine Models ---
class MachineBase(BaseModel):
    name: str
    site: str
    description: Optional[str] = None

class MachineResponse(MachineBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)


# --- Combined Models ---
class MachineWithPartsResponse(MachineResponse):
    parts: List[PartResponse] = []