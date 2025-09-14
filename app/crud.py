from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def crear_alimento(db: Session, alimento: schemas.AlimentoCreate):
    nuevo_alimento = models.Alimento(
        nombre=alimento.nombre,
        tienda=alimento.tienda,
        cantidad=alimento.cantidad,
        caducidad=alimento.caducidad
    )
    db.add(nuevo_alimento)
    db.commit()
    db.refresh(nuevo_alimento)
    return nuevo_alimento

def obtener_alimentos(db: Session):
    # db.query(models.Alimento) → selecciona todos los registros de la tabla Alimento
    # .all() → devuelve todos los resultados en forma de lista
    return db.query(models.Alimento).all()

def actualizar_alimento(db: Session, id:int, alimento_datos: schemas.AlimentoUpdate):
    alimento=db.query(models.Alimento).filter(models.Alimento.id==id).first()
    if not alimento:
        raise HTTPException(status_code=404,detail="Alimento no encontrado")
    for key, value in alimento_datos.dict(exclude_unset=True).items(): #.dict convierte al objeto de tipo Pydantic(los del PUT) y el exclude_unset quita los que no se hayan añadido en el UPDATE
        setattr(alimento,key,value)
    db.commit()
    db.refresh(alimento)
    return alimento

def eliminar_alimento(db:Session, id:int):
    alimento=db.query(models.Alimento).filter(models.Alimento.id==id).first()
    if not alimento:
        raise HTTPException(status_code=404,detail="Alimento no encontrado")
    db.delete(alimento)
    db.commit()
    return alimento
