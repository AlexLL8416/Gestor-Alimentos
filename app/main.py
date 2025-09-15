from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "API Gestor de Alimentos funcionando 🚀"}

# ------------------
# ALIMENTOS
# ------------------

@app.post("/alimentos/", response_model=schemas.Alimento)
def crear_alimento(alimento: schemas.AlimentoCreate, db: Session = Depends(get_db)):
    return crud.crear_alimento(db=db, alimento=alimento)

@app.get("/alimentos/", response_model=list[schemas.Alimento])
def listar_alimentos(db:Session = Depends(get_db)):
    return crud.obtener_alimentos(db=db)

@app.get("/alimentos/{id}", response_model=schemas.Alimento)
def listar_alimentos_por_id(id:int,db:Session = Depends(get_db)):
    alimento = crud.obtener_alimento_por_id(db, id)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return alimento

@app.put("/alimentos/{id}", response_model=schemas.Alimento)
def actualiza_alimentos( id:int, alimento_actualizado:schemas.AlimentoUpdate, db:Session = Depends(get_db)):
    return crud.actualizar_alimento(db=db, id=id,alimento_datos=alimento_actualizado)

@app.delete("/alimentos/{id}", response_model=schemas.Alimento)
def actualiza_alimentos( id:int, db:Session = Depends(get_db)):
    return crud.eliminar_alimento(db=db, id=id)

# ------------------
# TIENDAS
# ------------------

@app.post("/tiendas/", response_model=schemas.Tienda)
def creat_tienda(tienda: schemas.TiendaCreate, db: Session = Depends(get_db)):
    return crud.crear_tienda(db=db, tienda=tienda)

@app.get("/tiendas/", response_model=list[schemas.Tienda])
def listar_tiendas(db:Session = Depends(get_db)):
    return crud.obtener_tiendas(db=db)

@app.get("/tiendas/{id}", response_model=schemas.Tienda)
def listar_tiendas_por_id(id:int,db:Session = Depends(get_db)):
    tienda = crud.obtener_tienda_por_id(db, id)
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return tienda

@app.put("/tiendas/{id}", response_model=schemas.Tienda)
def actualiza_tiendas( id:int, tienda_actualizada:schemas.TiendaUpdate, db:Session = Depends(get_db)):
    return crud.actualizar_tienda(db=db, id=id,tienda_datos=tienda_actualizada)

@app.delete("/tiendas/{id}", response_model=schemas.Tienda)
def eliminar_tienda( id:int, db:Session = Depends(get_db)):
    return crud.eliminar_tienda(db=db, id=id)

# ------------------
# RECETAS
# ------------------

@app.post("/recetas/", response_model=schemas.Receta)
def creat_receta(receta: schemas.RecetaCreate, db: Session = Depends(get_db)):
    return crud.crear_receta(db=db, receta=receta)

@app.get("/recetas/", response_model=list[schemas.Receta])
def listar_recetas(db:Session = Depends(get_db)):
    return crud.obtener_recetas(db=db)

@app.get("/recetas/{id}", response_model=schemas.Receta)
def listar_recetas_por_id(id:int,db:Session = Depends(get_db)):
    receta = crud.obtener_receta_por_id(db, id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

@app.put("/recetas/{id}", response_model=schemas.Receta)
def actualiza_recetas( id:int, receta_actualizada:schemas.RecetaUpdate, db:Session = Depends(get_db)):
    return crud.actualizar_receta(db=db, id=id,receta_datos=receta_actualizada)

@app.delete("/recetas/{id}", response_model=schemas.Receta)
def eliminar_receta( id:int, db:Session = Depends(get_db)):
    return crud.eliminar_receta(db=db, id=id)

# ------------------
# RELACIONES
# ------------------

@app.post("/alimentos/{id_alimento}/tiendas/{id_tienda}", response_model=schemas.Alimento)
def asociar_alimento_con_tienda(id_alimento: int, id_tienda: int, db: Session = Depends(get_db)):
    return crud.asociar_alimento_tienda(db, id_alimento, id_tienda)

@app.post("/alimentos/{id_alimento}/recetas/{id_receta}", response_model=schemas.Alimento)
def asociar_alimento_con_receta(id_alimento: int, id_receta: int, db: Session = Depends(get_db)):
    return crud.asociar_alimento_receta(db, id_alimento, id_receta)