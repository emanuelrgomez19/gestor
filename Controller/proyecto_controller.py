from flask import Blueprint, Flask, request, json, Response, jsonify
from marshmallow.fields import Method
from webargs.core import Request
from Model.proyecto_model import Proyecto
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound
from flask_cors import cross_origin


from database import get_db_session


proyecto_api = Blueprint('proyecto_api', __name__)

create_proyecto_request = {
  "nombre": fields.Str(required=True, validate=validate.Length(min=1)),
  "estado": fields.Boolean()
}



@proyecto_api.route('/proyectos',methods=['GET'])
def getProyecto():
  s = get_db_session()
  proyecto = s.query(Proyecto)
  proyectojson=json.dumps([u.to_dict() for u in proyecto])
  return Response(proyectojson, status=200, mimetype='application/json')


@proyecto_api.route('/proyecto', methods=['POST'])
def nuevoProyecto():
  nombre = request.json['nombre']
  estado = request.json['estado']
  descripcion = request.json['descripcion']
  proyecto = Proyecto(nombre = nombre,estado=estado,descripcion=descripcion)
  print(proyecto)
  s = get_db_session()
  s.add(proyecto)
  s.commit()
  return Response("Proyecto "+nombre+" created", 201)