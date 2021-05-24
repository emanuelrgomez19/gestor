from flask import Blueprint, Flask, request, json, Response, jsonify
from webargs.core import Request
from Model.escenario_model import Escenario
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

from database import get_db_session


escenario_api = Blueprint('escenario_api', __name__)

create_escenario_request = {
  "descripcion": fields.Str(required=True, validate=validate.Length(min=1)),
  "objetivo": fields.Str(required=False, validate=validate.Length(min=1)),
  "pre_condicion": fields.Str(required=False, validate=validate.Length(min=1)),
  "pos_condicion": fields.Str(required=False, validate=validate.Length(min=1)),
  "id_historia": fields.Int(required=True)


}



@escenario_api.route('/escenarios')
def getEscenario():
  s = get_db_session()
  escenario = s.query(Escenario)
  return Response(json.dumps([u.to_dict() for u in escenario]), status=200, mimetype='application/json')


@escenario_api.route('/escenario', methods=['POST'])
def nuevoEscenario():
  descripcion = request.json['descripcion']
  objetivo = request.json['objetivo']
  pre_condicion = request.json['pre_condicion']
  pos_condicion = request.json['pos_condicion']
  id_historia = request.json['id_historia']
  escenario = Escenario(descripcion = descripcion ,objetivo = objetivo ,  pre_condicion = pre_condicion , pos_condicion = pos_condicion,id_historia=id_historia)
  print(escenario)
  s = get_db_session()
  s.add(escenario)
  s.commit()
  return Response('Escenario created', 201)