from flask import Blueprint, Flask, request, json, Response, jsonify
from webargs.core import Request
from Model.user_model import User
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from Model.lote_model import Lote
from sqlalchemy.orm.exc import NoResultFound

from database import get_db_session


lote_api = Blueprint('lote_api', __name__)

create_lote_request = {
  "direccion": fields.Str(required=True, validate=validate.Length(min=1)),
  "metros": fields.Str(required=True, validate=validate.Length(min=1)),
  "hectareas":fields.Float(required=True),
  "precio":fields.Int(required=True)
}



@lote_api.route('/lotes')
def getLotes():
  s = get_db_session()
  lote = s.query(Lote)
  return Response(json.dumps([u.to_dict() for u in lote]), status=200, mimetype='application/json')


@lote_api.route('/lote', methods=['POST'])
def nuevoLote():
  direccion = request.json['direccion']
  metros = request.json['metros']
  hectareas = request.json['hectareas']
  precio = request.json['precio']
  lote = Lote(direccion = direccion,metros=metros,hectareas=hectareas,precio=precio)
  print(lote)
  s = get_db_session()
  s.add(lote)
  s.commit()
  return Response('User created', 201)

