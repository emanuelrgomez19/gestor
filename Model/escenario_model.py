from marshmallow.fields import Int
from sqlalchemy import Column, Integer, String , ForeignKey  , Float
from webargs.core import T
from database import Base
from Utils.utils import ToDict


class Escenario(Base,ToDict):
 __tablename__ = 'ESCENARIO_HISTORIA'
 id = Column(Integer, primary_key=True)
 descripcion = Column(String(1000))
 objetivo = Column(String(1000))
 pre_condicion = Column(String(1000))
 pos_condicion = Column(String(1000))
 id_historia = Column(Integer)
 #id_paso = Column(Integer,ForeignKey('paso.id'))


def __init__(self, como ,quiero,para):
 self.como = como
 self.quiero = quiero
 self.para = para 
