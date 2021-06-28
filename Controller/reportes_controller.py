from flask import Blueprint, Flask, request, json, Response, jsonify
from marshmallow.fields import Method
from sqlalchemy.sql.functions import func
from webargs.core import Request
from Model.historiaUsuario_model import Historia
from Model.proyecto_model import Proyecto
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

from database import get_db_session


reporte_api = Blueprint('reporte_api', __name__)


@reporte_api.route('/historiaxproyecto',methods=['GET'])
def getHistoriaXproyecto():
    s = get_db_session()
    reporte = s.query(func.count(Proyecto.nombre))
    #reporte = s.query(Proyecto.nombre).join(Historia,Proyecto.id == Historia.id_proyecto).count(Proyecto.nombre).group_by(Proyecto.nombre)
    print(reporte)
    reporteJson=json.dumps([u.to_dict() for u in reporte])
    return Response(reporteJson, status=200, mimetype='application/json')
    
