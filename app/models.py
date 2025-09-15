from sqlalchemy import Column, Integer, String, Float, Date, Table, MetaData, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from .database import Base

alimento_tienda = Table(
    "alimento_tienda",
    Base.metadata,
    Column("id_alimento_tienda",Integer,primary_key=True,autoincrement=True),
    Column("id_tienda",Integer,ForeignKey("tiendas.id_tienda"),nullable=False),
    Column("id_alimento",Integer,ForeignKey("alimentos.id_alimento"),nullable=False),
    UniqueConstraint("id_alimento", "id_tienda", name="uq_alimento_tienda")
)

alimento_receta = Table(
    "alimento_receta",
    Base.metadata,
    Column("id_alimento_receta",Integer,primary_key=True,autoincrement=True),
    Column("cantidad",Integer,nullable=True),
    Column("id_receta",Integer,ForeignKey("recetas.id_receta"),nullable=False),
    Column("id_alimento",Integer,ForeignKey("alimentos.id_alimento"),nullable=False),
    UniqueConstraint("id_alimento", "id_receta", name="uq_alimento_receta")
)

class Alimento(Base):
    __tablename__ = "alimentos"

    id_alimento = Column(Integer, primary_key=True, index=True)
    nombre_alimento = Column(String, nullable=False)
    cantidad = Column(Float)
    caducidad = Column(Date,nullable=True)
    congelado = Column(Boolean)

    tiendas = relationship("Tienda",secondary=alimento_tienda, back_populates="alimentos")
    recetas = relationship("Receta",secondary=alimento_receta, back_populates="alimentos")

class Tienda(Base):
    __tablename__ = "tiendas"

    id_tienda = Column(Integer, primary_key=True, index=True)
    nombre_tienda = Column(String)
    pagina_web = Column(String, nullable=True)
    lugar = Column(String, nullable=True)

    alimentos = relationship("Alimento", secondary=alimento_tienda, back_populates="tiendas")

class Receta(Base):
    __tablename__ = "recetas"

    id_receta = Column(Integer, primary_key=True, index=True)
    nombre_receta = Column(String)
    autor = Column(String, nullable=True)
    url = Column(String, nullable=True)

    alimentos = relationship("Alimento", secondary=alimento_receta, back_populates="recetas")


