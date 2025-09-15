from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# ------------------
# ALIMENTOS
# ------------------

def crear_alimento(db: Session, alimento: schemas.AlimentoCreate):
    nuevo_alimento = models.Alimento(
        nombre_alimento=alimento.nombre_alimento,
        cantidad=alimento.cantidad,
        caducidad=alimento.caducidad,
        congelado=alimento.congelado
    )
    db.add(nuevo_alimento)
    db.commit()
    db.refresh(nuevo_alimento)
    return nuevo_alimento

def obtener_alimentos(db: Session):
    # db.query(models.Alimento) → selecciona todos los registros de la tabla Alimento
    # .all() → devuelve todos los resultados en forma de lista
    return db.query(models.Alimento).all()

def obtener_alimento_por_id(db: Session, id:int):
    # db.query(models.Alimento) → selecciona todos los registros de la tabla Alimento
    # .all() → devuelve todos los resultados en forma de lista
    return db.query(models.Alimento).filter(models.Alimento.id_alimento==id).first()

def actualizar_alimento(db: Session, id:int, alimento_datos: schemas.AlimentoUpdate):
    alimento=db.query(models.Alimento).filter(models.Alimento.id_alimento==id).first()
    if not alimento:
        raise HTTPException(status_code=404,detail="Alimento no encontrado")
    for key, value in alimento_datos.dict(exclude_unset=True).items(): #.dict convierte al objeto de tipo Pydantic(los del PUT) y el exclude_unset quita los que no se hayan añadido en el UPDATE
        setattr(alimento,key,value)
    db.commit()
    db.refresh(alimento)
    return alimento

def eliminar_alimento(db:Session, id:int):
    alimento=db.query(models.Alimento).filter(models.Alimento.id_alimento==id).first()
    if not alimento:
        raise HTTPException(status_code=404,detail="Alimento no encontrado")
    db.delete(alimento)
    db.commit()
    return alimento

# ------------------
# TIENDAS
# ------------------

def crear_tienda(db: Session, tienda: schemas.TiendaCreate):
    nueva_tienda = models.Tienda(
        nombre_tienda=tienda.nombre_tienda,
        pagina_web=tienda.pagina_web,
        lugar=tienda.lugar
    )
    db.add(nueva_tienda)
    db.commit()
    db.refresh(nueva_tienda)
    return nueva_tienda

def obtener_tiendas(db: Session):
    # db.query(models.Alimento) → selecciona todos los registros de la tabla Alimento
    # .all() → devuelve todos los resultados en forma de lista
    return db.query(models.Tienda).all()

def obtener_tienda_por_id(db: Session, id:int):
    # db.query(models.Alimento) → selecciona todos los registros de la tabla Alimento
    # .all() → devuelve todos los resultados en forma de lista
    return db.query(models.Tienda).filter(models.Tienda.id_tienda==id).first()

def actualizar_tienda(db: Session, id:int, tienda_datos: schemas.TiendaUpdate):
    tienda=db.query(models.Tienda).filter(models.Tienda.id_tienda==id).first()
    if not tienda:
        raise HTTPException(status_code=404,detail="Tienda no encontrada")
    for key, value in tienda_datos.dict(exclude_unset=True).items(): #.dict convierte al objeto de tipo Pydantic(los del PUT) y el exclude_unset quita los que no se hayan añadido en el UPDATE
        setattr(tienda,key,value)
    db.commit()
    db.refresh(tienda)
    return tienda

def eliminar_tienda(db:Session, id:int):
    tienda=db.query(models.Tienda).filter(models.Tienda.id_tienda==id).first()
    if not tienda:
        raise HTTPException(status_code=404,detail="Tienda no encontrada")
    db.delete(tienda)
    db.commit()
    return tienda

# ------------------
# RECETAS
# ------------------

def crear_receta(db: Session, receta: schemas.RecetaCreate):
    nueva_receta = models.Receta(
        nombre_receta=receta.nombre_receta,
        autor=receta.autor,
        url=receta.url
    )
    db.add(nueva_receta)
    db.commit()
    db.refresh(nueva_receta)
    return nueva_receta

def obtener_recetas(db: Session):
    # db.query(models.Alimento) → selecciona todos los registros de la tabla Alimento
    # .all() → devuelve todos los resultados en forma de lista
    return db.query(models.Receta).all()

def obtener_receta_por_id(db: Session, id:int):
    # db.query(models.Alimento) → selecciona todos los registros de la tabla Alimento
    # .all() → devuelve todos los resultados en forma de lista
    return db.query(models.Receta).filter(models.Receta.id_receta==id).first()

def actualizar_receta(db: Session, id:int, receta_datos: schemas.RecetaUpdate):
    receta=db.query(models.Receta).filter(models.Receta.id_receta==id).first()
    if not receta:
        raise HTTPException(status_code=404,detail="Receta no encontrada")
    for key, value in receta_datos.dict(exclude_unset=True).items(): #.dict convierte al objeto de tipo Pydantic(los del PUT) y el exclude_unset quita los que no se hayan añadido en el UPDATE
        setattr(receta,key,value)
    db.commit()
    db.refresh(receta)
    return receta

def eliminar_receta(db:Session, id:int):
    receta=db.query(models.Receta).filter(models.Receta.id_receta==id).first()
    if not receta:
        raise HTTPException(status_code=404,detail="Receta no encontrada")
    db.delete(receta)
    db.commit()
    return receta

# ------------------
# RELACIONES
# ------------------

def asociar_alimento_tienda(db: Session, id_alimento: int, id_tienda: int):
    alimento = db.query(models.Alimento).filter(models.Alimento.id_alimento == id_alimento).first()
    tienda = db.query(models.Tienda).filter(models.Tienda.id_tienda == id_tienda).first()

    if not alimento or not tienda:
        raise HTTPException(status_code=404, detail="Alimento o tienda no encontrados")

    # Evitar duplicados
    if tienda in alimento.tiendas:
        raise HTTPException(status_code=400, detail="La relación ya existe")

    alimento.tiendas.append(tienda)  # relación many-to-many
    db.commit()
    db.refresh(alimento)
    return alimento

def asociar_alimento_receta(db: Session, id_alimento: int, id_receta: int):
    alimento = db.query(models.Alimento).filter(models.Alimento.id_alimento == id_alimento).first()
    receta = db.query(models.Receta).filter(models.Receta.id_receta == id_receta).first()

    if not alimento or not receta:
        raise HTTPException(status_code=404, detail="Alimento o receta no encontrados")

    # Evitar duplicados
    if receta in alimento.recetas:
        raise HTTPException(status_code=400, detail="La relación ya existe")

    alimento.recetas.append(receta)  # relación many-to-many
    db.commit()
    db.refresh(alimento)
    return alimento