from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from webargs.core import T
from database import Base
from Utils.utils import ToDict


class Proyecto(Base, ToDict):
  __tablename__ = 'PROYECTO'
  id = Column(Integer, primary_key=True)
  nombre = Column(String(100))
  estado = Column(Boolean(True))
  descripcion = Column(String(100))
 


  def __init__(self, nombre, estado , descripcion):
   self.nombre = nombre
   self.estado = estado
   self.descripcion = descripcion