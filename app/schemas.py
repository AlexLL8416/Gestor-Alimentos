from pydantic import BaseModel
from datetime import date
from typing import Optional

class AlimentoCreate(BaseModel):
    nombre: str
    tienda: Optional[str] = None
    cantidad: int
    caducidad: Optional[date] = None
