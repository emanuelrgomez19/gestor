from flask import Blueprint, Flask, request, json, Response, jsonify
from webargs.core import Request
from Model.historiaUsuario_model import Historia
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

from database import get_db_session


historia_api = Blueprint('historia_api', __name__)

create_historia_request = {
  "titulo": fields.Str(required=True, validate=validate.Length(min=1)),
  "criterio_aceptacion": fields.Str(required=False, validate=validate.Length(min=1)),
  "id_proyecto": fields.Int(requiere=True)
}



@historia_api.route('/historias')
def getHistoria():
  s = get_db_session()
  historia = s.query(Historia)
  return Response(json.dumps([u.to_dict() for u in historia]), status=200, mimetype='application/json')


@historia_api.route('/historia', methods=['POST'])
def nuevoHistoria():
  titulo = request.json['titulo']
  criterio_aceptacion = request.json['criterio_aceptacion']
  id_proyecto = request.json['id_proyecto']
  historia = Historia(titulo = titulo, criterio_aceptacion = criterio_aceptacion,id_proyecto=id_proyecto)
  print(historia)
  s = get_db_session()
  s.add(historia)
  s.commit()
  return Response('Historia created', 201)