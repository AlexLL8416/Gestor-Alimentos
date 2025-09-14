from pydantic import BaseModel
from datetime import date
from typing import Optional

class AlimentoCreate(BaseModel):
    nombre: str
    tienda: Optional[str] = None
    cantidad: int
    caducidad: Optional[date] = None

class AlimentoUpdate(BaseModel):
    nombre: Optional[str] = None
    tienda: Optional[str] = None
    cantidad: Optional[int] = None
    caducidad: Optional[date] = None