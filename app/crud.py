# crud.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select, insert, update
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
    return db.query(models.Alimento).all()

def obtener_alimento_por_id(db: Session, id: int):
    return db.query(models.Alimento).filter(models.Alimento.id_alimento == id).first()

def obtener_alimento_por_nombre(db: Session, nombre: str):
    return db.query(models.Alimento).filter(models.Alimento.nombre_alimento == nombre).first()

def actualizar_alimento(db: Session, id: int, alimento_datos: schemas.AlimentoUpdate):
    alimento = db.query(models.Alimento).filter(models.Alimento.id_alimento == id).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    for key, value in alimento_datos.dict(exclude_unset=True).items():
        setattr(alimento, key, value)
    db.commit()
    db.refresh(alimento)
    return alimento

def eliminar_alimento(db: Session, id: int):
    alimento = db.query(models.Alimento).filter(models.Alimento.id_alimento == id).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    db.delete(alimento)
    db.commit()
    return alimento

def obtener_alimentos_sin_stock(db: Session):
    return db.query(models.Alimento).filter(models.Alimento.cantidad == 0).all()

def obtener_alimentos_con_stock(db: Session):
    return db.query(models.Alimento).filter(models.Alimento.cantidad > 0).all()

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
    return db.query(models.Tienda).all()

def obtener_tienda_por_id(db: Session, id: int):
    return db.query(models.Tienda).filter(models.Tienda.id_tienda == id).first()

def obtener_tienda_por_nombre(db: Session, nombre: str):
    return db.query(models.Tienda).filter(models.Tienda.nombre_tienda == nombre).first()

def actualizar_tienda(db: Session, id: int, tienda_datos: schemas.TiendaUpdate):
    tienda = db.query(models.Tienda).filter(models.Tienda.id_tienda == id).first()
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    for key, value in tienda_datos.dict(exclude_unset=True).items():
        setattr(tienda, key, value)
    db.commit()
    db.refresh(tienda)
    return tienda

def eliminar_tienda(db: Session, id: int):
    tienda = db.query(models.Tienda).filter(models.Tienda.id_tienda == id).first()
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
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
    return db.query(models.Receta).all()

def obtener_receta_por_id(db: Session, id: int):
    return db.query(models.Receta).filter(models.Receta.id_receta == id).first()

def obtener_receta_por_nombre(db: Session, nombre: str):
    return db.query(models.Receta).filter(models.Receta.nombre_receta == nombre).first()

def actualizar_receta(db: Session, id: int, receta_datos: schemas.RecetaUpdate):
    receta = db.query(models.Receta).filter(models.Receta.id_receta == id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    for key, value in receta_datos.dict(exclude_unset=True).items():
        setattr(receta, key, value)
    db.commit()
    db.refresh(receta)
    return receta

def eliminar_receta(db: Session, id: int):
    receta = db.query(models.Receta).filter(models.Receta.id_receta == id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    db.delete(receta)
    db.commit()
    return receta

# ------------------
# RELACIONES (por id)
# ------------------

def asociar_alimento_tienda(db: Session, id_alimento: int, id_tienda: int):
    alimento = db.query(models.Alimento).filter(models.Alimento.id_alimento == id_alimento).first()
    tienda = db.query(models.Tienda).filter(models.Tienda.id_tienda == id_tienda).first()

    if not alimento or not tienda:
        raise HTTPException(status_code=404, detail="Alimento o tienda no encontrados")

    # Evitar duplicados
    # chequeamos en la tabla puente
    sel = select(models.alimento_tienda).where(
        models.alimento_tienda.c.id_alimento == id_alimento,
        models.alimento_tienda.c.id_tienda == id_tienda
    )
    existing = db.execute(sel).first()
    if existing:
        raise HTTPException(status_code=400, detail="La relación ya existe")

    # Insertar en la tabla puente
    ins = insert(models.alimento_tienda).values(id_alimento=id_alimento, id_tienda=id_tienda)
    db.execute(ins)
    db.commit()
    db.refresh(alimento)
    return alimento

def asociar_alimento_receta(db: Session, id_alimento: int, id_receta: int, cantidad: int = 1):
    alimento = db.query(models.Alimento).filter(models.Alimento.id_alimento == id_alimento).first()
    receta = db.query(models.Receta).filter(models.Receta.id_receta == id_receta).first()

    if not alimento or not receta:
        raise HTTPException(status_code=404, detail="Alimento o receta no encontrados")

    # Evitar duplicados
    sel = select(models.alimento_receta).where(
        models.alimento_receta.c.id_alimento == id_alimento,
        models.alimento_receta.c.id_receta == id_receta
    )
    existing = db.execute(sel).first()
    if existing:
        raise HTTPException(status_code=400, detail="La relación ya existe")

    # Insertar en la tabla puente con cantidad
    ins = insert(models.alimento_receta).values(id_alimento=id_alimento, id_receta=id_receta, cantidad=cantidad)
    db.execute(ins)
    db.commit()
    db.refresh(alimento)
    return alimento

# -------------------
# EDITAR POR NOMBRE
# -------------------

def actualizar_alimento_por_nombre(db: Session, nombre_alimento: str, alimento_datos: schemas.AlimentoUpdate):
    alimento = db.query(models.Alimento).filter(models.Alimento.nombre_alimento == nombre_alimento).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    for key, value in alimento_datos.dict(exclude_unset=True).items():
        setattr(alimento, key, value)
    db.commit()
    db.refresh(alimento)
    return alimento

def actualizar_tienda_por_nombre(db: Session, nombre_tienda: str, tienda_datos: schemas.TiendaUpdate):
    tienda = db.query(models.Tienda).filter(models.Tienda.nombre_tienda == nombre_tienda).first()
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    for key, value in tienda_datos.dict(exclude_unset=True).items():
        setattr(tienda, key, value)
    db.commit()
    db.refresh(tienda)
    return tienda

def actualizar_receta_por_nombre(db: Session, nombre_receta: str, receta_datos: schemas.RecetaUpdate):
    receta = db.query(models.Receta).filter(models.Receta.nombre_receta == nombre_receta).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    for key, value in receta_datos.dict(exclude_unset=True).items():
        setattr(receta, key, value)
    db.commit()
    db.refresh(receta)
    return receta

def update_alimento_by_nombre_and_tienda(db: Session, alimento_nombre: str, tienda_nombre: str, alimento_update: schemas.AlimentoUpdate):
    tienda = db.query(models.Tienda).filter(models.Tienda.nombre_tienda == tienda_nombre).first()
    if not tienda:
        return None

    alimento = db.query(models.Alimento).filter(models.Alimento.nombre_alimento == alimento_nombre).first()
    if not alimento:
        return None

    # verificar que la relación exista entre alimento y tienda
    sel = select(models.alimento_tienda).where(
        models.alimento_tienda.c.id_alimento == alimento.id_alimento,
        models.alimento_tienda.c.id_tienda == tienda.id_tienda
    )
    exists = db.execute(sel).first()
    if not exists:
        return None

    # actualizar campos permitidos
    for key, value in alimento_update.dict(exclude_unset=True).items():
        setattr(alimento, key, value)
    db.commit()
    db.refresh(alimento)
    return alimento

def update_alimento_receta_cantidad(db: Session, alimento_nombre: str, receta_nombre: str, nueva_cantidad: int):
    alimento = db.query(models.Alimento).filter(models.Alimento.nombre_alimento == alimento_nombre).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    receta = db.query(models.Receta).filter(models.Receta.nombre_receta == receta_nombre).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    upd = update(models.alimento_receta).where(
        models.alimento_receta.c.id_alimento == alimento.id_alimento,
        models.alimento_receta.c.id_receta == receta.id_receta
    ).values(cantidad=nueva_cantidad)
    res = db.execute(upd)
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    db.commit()

    sel = select(models.alimento_receta).where(
        models.alimento_receta.c.id_alimento == alimento.id_alimento,
        models.alimento_receta.c.id_receta == receta.id_receta
    )
    row = db.execute(sel).first()
    return {"id_alimento": alimento.id_alimento, "id_receta": receta.id_receta, "cantidad": row.cantidad}

# -------------------
# RELACIONES POR NOMBRE
# -------------------

def asociar_alimento_tienda_por_nombre(db: Session, nombre_alimento: str, nombre_tienda: str):
    alimento = db.query(models.Alimento).filter(models.Alimento.nombre_alimento == nombre_alimento).first()
    tienda = db.query(models.Tienda).filter(models.Tienda.nombre_tienda == nombre_tienda).first()

    if not alimento or not tienda:
        raise HTTPException(status_code=404, detail="Alimento o Tienda no encontrados")

    sel = select(models.alimento_tienda).where(
        models.alimento_tienda.c.id_alimento == alimento.id_alimento,
        models.alimento_tienda.c.id_tienda == tienda.id_tienda
    )
    existing = db.execute(sel).first()
    if existing:
        raise HTTPException(status_code=400, detail="La relación ya existe")

    ins = insert(models.alimento_tienda).values(id_alimento=alimento.id_alimento, id_tienda=tienda.id_tienda)
    db.execute(ins)
    db.commit()
    db.refresh(alimento)
    return alimento

def asociar_alimento_receta_por_nombre(db: Session, nombre_alimento: str, nombre_receta: str, cantidad: int = 1):
    alimento = db.query(models.Alimento).filter(models.Alimento.nombre_alimento == nombre_alimento).first()
    receta = db.query(models.Receta).filter(models.Receta.nombre_receta == nombre_receta).first()

    if not alimento or not receta:
        raise HTTPException(status_code=404, detail="Alimento o Receta no encontrados")

    sel = select(models.alimento_receta).where(
        models.alimento_receta.c.id_alimento == alimento.id_alimento,
        models.alimento_receta.c.id_receta == receta.id_receta
    )
    existing = db.execute(sel).first()
    if existing:
        raise HTTPException(status_code=400, detail="La relación ya existe")

    ins = insert(models.alimento_receta).values(id_alimento=alimento.id_alimento, id_receta=receta.id_receta, cantidad=cantidad)
    db.execute(ins)
    db.commit()
    db.refresh(alimento)
    return alimento

# --------------------- FUNCION COMPLEJA ---------------------

def obtener_recetas_con_alimentos_disponibles(db: Session):
    """
    Devuelve todas las recetas que tienen al menos un alimento con cantidad > 0
    """
    return (
        db.query(models.Receta)
        .join(models.alimento_receta, models.Receta.id_receta == models.alimento_receta.c.id_receta)
        .join(models.Alimento, models.Alimento.id_alimento == models.alimento_receta.c.id_alimento)
        .filter(models.Alimento.cantidad > 0)
        .distinct()
        .all()
    )