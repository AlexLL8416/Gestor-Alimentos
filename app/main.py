from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, join
from . import models, schemas, crud
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Permitir peticiones desde el frontend (ej: localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta absoluta a la carpeta frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

# Montar la carpeta "frontend" como archivos estáticos
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# ------------------
# ALIMENTOS
# ------------------

@app.post("/alimentos/", response_model=schemas.Alimento)
def crear_alimento(alimento: schemas.AlimentoCreate, db: Session = Depends(get_db)):
    return crud.crear_alimento(db=db, alimento=alimento)

@app.get("/alimentos/", response_model=list[schemas.Alimento])
def listar_alimentos(db: Session = Depends(get_db)):
    return crud.obtener_alimentos(db=db)

@app.get("/alimentos/{id}", response_model=schemas.Alimento)
def obtener_alimento_por_id(id: int, db: Session = Depends(get_db)):
    alimento = crud.obtener_alimento_por_id(db, id)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento

@app.put("/alimentos/{id}", response_model=schemas.Alimento)
def actualizar_alimento(id: int, alimento_actualizado: schemas.AlimentoUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_alimento(db=db, id=id, alimento_datos=alimento_actualizado)

@app.delete("/alimentos/{nombre}", response_model=schemas.Alimento)
def eliminar_alimento(nombre: str, db: Session = Depends(get_db)):
    return crud.eliminar_alimento(db=db, nombre=nombre)

# ------------------
# TIENDAS
# ------------------

@app.post("/tiendas/", response_model=schemas.Tienda)
def crear_tienda(tienda: schemas.TiendaCreate, db: Session = Depends(get_db)):
    return crud.crear_tienda(db=db, tienda=tienda)

@app.get("/tiendas/", response_model=list[schemas.Tienda])
def listar_tiendas(db: Session = Depends(get_db)):
    return crud.obtener_tiendas(db=db)

@app.get("/tiendas/{id}", response_model=schemas.Tienda)
def obtener_tienda_por_id(id: int, db: Session = Depends(get_db)):
    tienda = crud.obtener_tienda_por_id(db, id)
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return tienda

@app.put("/tiendas/{id}", response_model=schemas.Tienda)
def actualizar_tienda(id: int, tienda_actualizada: schemas.TiendaUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_tienda(db=db, id=id, tienda_datos=tienda_actualizada)

@app.delete("/tiendas/{nombre}", response_model=schemas.Tienda)
def eliminar_tienda(nombre: str, db: Session = Depends(get_db)):
    return crud.eliminar_tienda(db=db, nombre=nombre)

# ------------------
# RECETAS
# ------------------

@app.post("/recetas/", response_model=schemas.Receta)
def crear_receta(receta: schemas.RecetaCreate, db: Session = Depends(get_db)):
    return crud.crear_receta(db=db, receta=receta)

@app.get("/recetas/", response_model=list[schemas.Receta])
def listar_recetas(db: Session = Depends(get_db)):
    return crud.obtener_recetas(db=db)

@app.get("/recetas/{id}", response_model=schemas.Receta)
def obtener_receta_por_id(id: int, db: Session = Depends(get_db)):
    receta = crud.obtener_receta_por_id(db, id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

@app.put("/recetas/{id}", response_model=schemas.Receta)
def actualizar_receta(id: int, receta_actualizada: schemas.RecetaUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_receta(db=db, id=id, receta_datos=receta_actualizada)

@app.delete("/recetas/{nombre}", response_model=schemas.Receta)
def eliminar_receta(nombre: str, db: Session = Depends(get_db)):
    return crud.eliminar_receta(db=db, nombre=nombre)

# ------------------
# RELACIONES (por id)
# ------------------
'''
@app.post("/alimentos/{id_alimento}/tiendas/{id_tienda}", response_model=schemas.Alimento)
def asociar_alimento_con_tienda(id_alimento: int, id_tienda: int, db: Session = Depends(get_db)):
    return crud.asociar_alimento_tienda(db, id_alimento, id_tienda)

@app.post("/alimentos/{id_alimento}/recetas/{id_receta}", response_model=schemas.Alimento)
def asociar_alimento_con_receta(id_alimento: int, id_receta: int, db: Session = Depends(get_db)):
    # por defecto cantidad = 1
    return crud.asociar_alimento_receta(db, id_alimento, id_receta, cantidad=1)
'''
# -------------------
# EDITAR POR NOMBRE
# -------------------

@app.put("/alimentos/nombre/{nombre}")
def actualizar_alimento_nombre(nombre: str, alimento: schemas.AlimentoUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_alimento_por_nombre(db, nombre, alimento)

@app.put("/tiendas/nombre/{nombre}")
def actualizar_tienda_nombre(nombre: str, tienda: schemas.TiendaUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_tienda_por_nombre(db, nombre, tienda)

@app.put("/recetas/nombre/{nombre}")
def actualizar_receta_nombre(nombre: str, receta: schemas.RecetaUpdate, db: Session = Depends(get_db)):
    return crud.actualizar_receta_por_nombre(db, nombre, receta)

@app.put("/alimentos/{alimento_nombre}/tienda/{tienda_nombre}", response_model=schemas.Alimento)
def update_alimento(alimento_nombre: str, tienda_nombre: str, alimento_update: schemas.AlimentoUpdate, db: Session = Depends(get_db)):
    alimento = crud.update_alimento_by_nombre_and_tienda(db, alimento_nombre, tienda_nombre, alimento_update)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado en esa tienda")
    return alimento

# -------------------
# RELACIONES POR NOMBRE (y cantidad para receta)
# -------------------

@app.post("/alimentos/{nombre_alimento}/tiendas/{nombre_tienda}")
def asociar_alimento_tienda_nombre(nombre_alimento: str, nombre_tienda: str, db: Session = Depends(get_db)):
    return crud.asociar_alimento_tienda_por_nombre(db, nombre_alimento, nombre_tienda)

@app.post("/alimentos/{nombre_alimento}/recetas/{nombre_receta}")
def asociar_alimento_receta_nombre(nombre_alimento: str, nombre_receta: str, cantidad: int = 1, db: Session = Depends(get_db)):
    return crud.asociar_alimento_receta_por_nombre(db, nombre_alimento, nombre_receta, cantidad)

# -------------------
# FILTRO: ALIMENTOS CON/SIN STOCK
# -------------------

@app.get("/alimentos/sin_stock/", response_model=list[schemas.Alimento])
def listar_alimentos_sin_stock(db: Session = Depends(get_db)):
    return crud.obtener_alimentos_sin_stock(db)

@app.get("/alimentos/con_stock/", response_model=list[schemas.Alimento])
def listar_alimentos_con_stock(db: Session = Depends(get_db)):
    return crud.obtener_alimentos_con_stock(db)

# -------------------
# GET POR NOMBRE
# -------------------

@app.get("/alimentos/nombre/{nombre}", response_model=schemas.Alimento)
def obtener_alimento_por_nombre(nombre: str, db: Session = Depends(get_db)):
    alimento = crud.obtener_alimento_por_nombre(db, nombre)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento

@app.get("/tiendas/nombre/{nombre}", response_model=schemas.Tienda)
def obtener_tienda_por_nombre(nombre: str, db: Session = Depends(get_db)):
    tienda = crud.obtener_tienda_por_nombre(db, nombre)
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return tienda

@app.get("/recetas/nombre/{nombre}", response_model=schemas.Receta)
def obtener_receta_por_nombre(nombre: str, db: Session = Depends(get_db)):
    receta = crud.obtener_receta_por_nombre(db, nombre)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

# --------------------- GET RELACIONES ---------------------

# Listar todas las relaciones alimento-receta
@app.get("/alimentos-recetas/")
def listar_alimentos_recetas(db: Session = Depends(get_db)):
    j = join(models.alimento_receta, models.Alimento, models.alimento_receta.c.id_alimento == models.Alimento.id_alimento)\
        .join(models.Receta, models.alimento_receta.c.id_receta == models.Receta.id_receta)
    sel = select(models.Alimento.nombre_alimento, models.Receta.nombre_receta, models.alimento_receta.c.cantidad).select_from(j)
    rows = db.execute(sel).all()

    return [{"alimento": r.nombre_alimento, "receta": r.nombre_receta, "cantidad": r.cantidad} for r in rows]


# Listar todas las relaciones alimento-tienda
@app.get("/alimentos-tiendas/")
def listar_alimentos_tiendas(db: Session = Depends(get_db)):
    return crud.obtener_alimentos_tiendas(db)

# --------------------- FUNCION COMPLEJA ---------------------

@app.get("/recetas/con_alimentos_disponibles/", response_model=list[schemas.Receta])
def listar_recetas_con_alimentos_disponibles(db: Session = Depends(get_db)):
    return crud.obtener_recetas_con_alimentos_disponibles(db)