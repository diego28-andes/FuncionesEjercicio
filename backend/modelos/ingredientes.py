from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_declarativa import Base

class Ingrediente(Base):
    __tablename__='ingredientes'
    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    tipo = Column(String)
    unidad_medida = Column(String)
    disponible = Column(Boolean)