from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "API Gestor de Alimentos funcionando 🚀"}

@app.post("/alimentos/")
def crear_alimento(alimento: schemas.AlimentoCreate, db: Session = Depends(get_db)):
    return crud.crear_alimento(db=db, alimento=alimento)

@app.get("/alimentos/")
def listar_alimentos(db:Session = Depends(get_db)):
    return crud.obtener_alimentos(db=db)

@app.put("/alimentos/{id}")
def actualiza_alimentos( id:int, alimento_actualizado:schemas.AlimentoUpdate, db:Session = Depends(get_db)):
    return crud.actualizar_alimento(db=db, id=id,alimento_datos=alimento_actualizado)

@app.delete("/alimentos/{id}")
def actualiza_alimentos( id:int, db:Session = Depends(get_db)):
    return crud.eliminar_alimento(db=db, id=id)