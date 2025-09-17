# schemas.py
from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional, List

# ------------------
# ALIMENTOS
# ------------------
class AlimentoBase(BaseModel):
    nombre_alimento: str
    cantidad: int = Field(ge=0, description="Cantidad debe ser >= 0")
    caducidad: Optional[date] = None
    congelado: bool

    @validator("caducidad")
    def caducidad_futura(cls, v):
        if v is not None and v <= date.today():
            raise ValueError("La fecha de caducidad debe ser futura")
        return v

class AlimentoCreate(AlimentoBase):
    pass

class AlimentoUpdate(BaseModel):
    nombre_alimento: Optional[str] = None
    cantidad: Optional[int] = None
    caducidad: Optional[date] = None
    congelado: Optional[bool] = None

class TiendaBrief(BaseModel):
    id_tienda: int
    nombre_tienda: str

    class Config:
        from_attributes = True

class RecetaBrief(BaseModel):
    id_receta: int
    nombre_receta: str

    class Config:
        from_attributes = True

class Alimento(AlimentoBase):
    id_alimento: int
    tiendas: Optional[List[TiendaBrief]] = None
    recetas: Optional[List[RecetaBrief]] = None

    class Config:
        from_attributes = True

# ------------------
# TIENDAS
# ------------------
class TiendaBase(BaseModel):
    nombre_tienda: str
    pagina_web: Optional[str] = None
    lugar: Optional[str] = None

class TiendaCreate(TiendaBase):
    pass

class TiendaUpdate(BaseModel):
    nombre_tienda: Optional[str] = None
    pagina_web: Optional[str] = None
    lugar: Optional[str] = None

class Tienda(TiendaBase):
    id_tienda: int
    alimentos: Optional[List[Alimento]] = None

    class Config:
        from_attributes = True

# ------------------
# RECETAS
# ------------------
class RecetaBase(BaseModel):
    nombre_receta: str
    autor: Optional[str] = None
    url: Optional[str] = None

class RecetaCreate(RecetaBase):
    pass

class RecetaUpdate(BaseModel):
    nombre_receta: Optional[str] = None
    autor: Optional[str] = None
    url: Optional[str] = None

class Receta(RecetaBase):
    id_receta: int
    alimentos: Optional[List[Alimento]] = None

    class Config:
        from_attributes = True