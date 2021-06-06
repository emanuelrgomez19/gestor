from flask import Blueprint, Flask, request, json, Response, jsonify
from marshmallow.fields import Method
from webargs.core import Request
from Model.proyecto_model import Proyecto
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

from database import get_db_session

proyecto_api = Blueprint('proyecto_api', __name__)

create_proyecto_request = {
  "nombre": fields.Str(required=True, validate=validate.Length(min=1)),
  "estado": fields.Boolean()
}


@proyecto_api.route('/proyectos/<int:id>',methods=['GET'])
def getProyecto(id):
  s = get_db_session()
  proyecto = s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).one_or_none()
  if proyecto != None:
    return Response(json.dumps(proyecto.to_dict()), status=200, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)

@proyecto_api.route('/proyectos',methods=['GET'])
def getListaProyectos():
  s = get_db_session()
  proyecto = s.query(Proyecto).filter(Proyecto.estado==True)
  proyectojson=json.dumps([u.to_dict() for u in proyecto])
  return Response(proyectojson, status=200, mimetype='application/json')


@proyecto_api.route('/proyectos', methods=['POST'])
def nuevoProyecto():
  nuevoProyecto = request.get_json().get('body')
  nombre = nuevoProyecto['nombre']
  estado = nuevoProyecto['estado']
  descripcion = nuevoProyecto['descripcion']
  proyecto = Proyecto(nombre = nombre,estado=estado,descripcion=descripcion)
  s = get_db_session()
  s.add(proyecto)
  s.commit()
  return Response(json.dumps(proyecto.to_dict()), status=201, mimetype='application/json')

@proyecto_api.route('/proyectos/<int:id>', methods=['DELETE'])
def deleteProyecto(id):
  s = get_db_session()
  proyecto = s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).one_or_none()
  if proyecto != None:
    s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).update({Proyecto.estado: False})    
    s.commit()
    return Response('Proyecto eliminado de la base de datos', status=200)
  return Response('Id inexistente en la base de datos', status=404)

@proyecto_api.route('/proyectos/<int:id>', methods=['PATCH'])
def editarProyecto(id):
  editaProyecto = request.get_json()#.get('body')
  nombre = editaProyecto['nombre']
  estado = editaProyecto['estado']
  descripcion = editaProyecto['descripcion']
  s = get_db_session()
  proyecto = s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).one_or_none()
  if proyecto != None:
    if nombre != None:
      s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).update({Proyecto.nombre: nombre})
    if estado != None:
      s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).update({Proyecto.estado: estado})
    if descripcion != None:
      s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).update({Proyecto.descripcion: descripcion})
    s.commit()
    proyectoUpdate = s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).one_or_none()
    return Response(json.dumps(proyectoUpdate.to_dict()), status=201, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)