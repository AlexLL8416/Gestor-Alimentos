from sqlalchemy.orm import Session
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
