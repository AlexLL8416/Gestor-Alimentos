from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# ------------------
# ALIMENTOS
# ------------------
class AlimentoBase(BaseModel):
    nombre_alimento: str
    cantidad: int
    caducidad: Optional[date] = None
    congelado: bool

class AlimentoCreate(AlimentoBase):
    pass

class AlimentoUpdate(BaseModel):
    nombre_alimento: Optional[str] = None
    cantidad: Optional[int] = None
    caducidad: Optional[date] = None
    congelado: Optional[bool] = None

class Alimento(AlimentoBase):
    id_alimento: int

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

    class Config:
        from_attributes = True
