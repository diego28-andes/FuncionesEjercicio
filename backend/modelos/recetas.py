from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from  .base_declarativa import Base

class Receta(Base):
    __tablename__ = 'recetas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    tiempo_preparacion = Column(Integer)
    dificultad = Column(String)    
    porciones = Column(Integer)
    ingrediente_id = Column(Integer,ForeignKey('ingredientes.id'))