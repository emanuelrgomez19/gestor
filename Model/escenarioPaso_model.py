from sqlalchemy import Column, Integer, String , ForeignKey  , Float
from webargs.core import T
from database import Base
from Utils.utils import ToDict


class Paso(Base,ToDict):
 __tablename__ = 'PASO_ESCENARIO'
 id = Column(Integer, primary_key=True)
 descripcion = Column(String(1000))

def __init__(self, descripcion):
 self.descripcion = descripcion

