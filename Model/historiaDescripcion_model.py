from sqlalchemy import Column, Integer, String , ForeignKey  , Float
from webargs.core import T
from database import Base
from Utils.utils import ToDict


class Descripcion(Base,ToDict):
 __tablename__ = 'DESCRIPCION_HISTORIA'
 id = Column(Integer, primary_key=True)
 como = Column(String(1000))
 quiero = Column(String(1000))
 para = Column(String(1000))


def __init__(self, como ,quiero,para):
 self.como = como
 self.quiero = quiero
 self.para = para 
