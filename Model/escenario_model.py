from marshmallow.fields import Int
from sqlalchemy import Column, Integer, String , Boolean  , Float
from webargs.core import T
from database import Base
from Utils.utils import ToDict


class Escenario(Base,ToDict):
 __tablename__ = 'ESCENARIO_HISTORIA'
 id = Column(Integer, primary_key=True)
 objetivo = Column(String(1000))
 descripcion = Column(String(1000))
 pre_condicion = Column(String(1000))
 pos_condicion = Column(String(1000))
 id_historia = Column(Integer)
 estado = Column(Boolean(True))

 #id_paso = Column(Integer,ForeignKey('paso.id'))


def __init__(self,objetivo,descripcion,pre_condicion,pos_condicion):
 self.objetivo = objetivo
 self.descripcion = descripcion
 self.pre_condicion = pre_condicion 
 self.pos_condicion = pos_condicion