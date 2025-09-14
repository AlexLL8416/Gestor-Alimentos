from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cantidad = Column(Float)
    tienda = Column(String)
    caducidad = Column(Date,nullable=True)
