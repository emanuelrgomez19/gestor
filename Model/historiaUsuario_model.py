from sqlalchemy import Column, Integer, String , ForeignKey  , Float
from webargs.core import T
from database import Base
from Utils.utils import ToDict


class Historia(Base,ToDict):
 __tablename__ = 'HISTORIA_USUARIO'
 id = Column(Integer, primary_key=True)
 titulo = Column(String(100))
 criterio_aceptacion = Column(String(1000))
#  id_descripcion = Column(Integer,ForeignKey('DESCRIPCION.id'))
 id_proyecto  = Column(Integer,ForeignKey('PROYECTO.id'))
# id_escenario = Column(Integer,ForeignKey('ESCENARIO_HISTORIA.id'))
 


def __init__(self, titulo ,criterio_aceptacion):
 self.titulo = titulo
 self.criterio_aceptacion = criterio_aceptacion