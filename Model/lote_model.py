from sqlalchemy import Column, Integer, String , ForeignKey  , Float
from webargs.core import T
from database import Base
from Utils.utils import ToDict


class Lote(Base,ToDict):
 __tablename__ = 'lote'
 id = Column(Integer, primary_key=True)
 direccion = Column(String(100))
 metros = Column(String(10))
 precio = Column(Integer)
 hectareas = Column(Float)


def __init__(self, direccion ,metros,hectareas,precio):
 self.direccion = direccion
 self.metros = metros
 self.hectareas = hectareas 
 self.precio = precio