from sqlalchemy import Column, Integer, String, Float, Date, Table, ForeignKey, UniqueConstraint, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base

# Tabla many-to-many entre alimentos y tiendas (sin atributos extra)
alimento_tienda = Table(
    "alimento_tienda",
    Base.metadata,
    Column("id_alimento", Integer, ForeignKey("alimentos.id_alimento"), nullable=False),
    Column("id_tienda", Integer, ForeignKey("tiendas.id_tienda"), nullable=False),
    UniqueConstraint("id_alimento", "id_tienda", name="uq_alimento_tienda")
)

# Tabla many-to-many entre alimentos y recetas, con columna adicional "cantidad"
alimento_receta = Table(
    "alimento_receta",
    Base.metadata,
    Column("id_alimento", Integer, ForeignKey("alimentos.id_alimento"), nullable=False),
    Column("id_receta", Integer, ForeignKey("recetas.id_receta"), nullable=False),
    Column("cantidad", Integer, nullable=True, default=1),
    UniqueConstraint("id_alimento", "id_receta", name="uq_alimento_receta")
)

class Alimento(Base):
    __tablename__ = "alimentos"

    id_alimento = Column(Integer, primary_key=True, index=True)
    nombre_alimento = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)
    caducidad = Column(Date, nullable=True)
    congelado = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        CheckConstraint("cantidad>=0", name="check_cantidad_no_negativa"),
        # Evitar checks con CURRENT_DATE en la definición si no estás seguro del dialecto DB
    )

    tiendas = relationship("Tienda", secondary=alimento_tienda, back_populates="alimentos")
    recetas = relationship("Receta", secondary=alimento_receta, back_populates="alimentos")


class Tienda(Base):
    __tablename__ = "tiendas"

    id_tienda = Column(Integer, primary_key=True, index=True)
    nombre_tienda = Column(String, nullable=False, unique=False)
    pagina_web = Column(String, nullable=True)
    lugar = Column(String, nullable=True)

    alimentos = relationship("Alimento", secondary=alimento_tienda, back_populates="tiendas")


class Receta(Base):
    __tablename__ = "recetas"

    id_receta = Column(Integer, primary_key=True, index=True)
    nombre_receta = Column(String, nullable=False)
    autor = Column(String, nullable=True)
    url = Column(String, nullable=True)

    alimentos = relationship("Alimento", secondary=alimento_receta, back_populates="recetas")
