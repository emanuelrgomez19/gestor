from flask import Blueprint, Flask, request, json, Response, jsonify
from marshmallow.fields import Method
from webargs.core import Request
from Model.proyecto_model import Proyecto
from Model.historiaUsuario_model import Historia
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import func, join, text

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
  proyecto = s.query(Proyecto).filter(Proyecto.estado==True).order_by(Proyecto.id.desc())
  proyectojson=json.dumps([u.to_dict() for u in proyecto])
  return Response(proyectojson, status=200, mimetype='application/json')


@proyecto_api.route('/proyectos', methods=['POST'])#Devolver lista con la creación del proyecto
def nuevoProyecto():
  nuevoProyecto = request.get_json().get('body')  
  proyecto = Proyecto(nombre=nuevoProyecto.get('nombre'),estado=nuevoProyecto.get('estado'),descripcion=nuevoProyecto.get('descripcion'))
  if proyecto.nombre and proyecto.nombre != None and proyecto.descripcion and proyecto.descripcion != None:
    s = get_db_session()
    s.add(proyecto)
    s.commit()
    proyecto = s.query(Proyecto).filter(Proyecto.estado==True).order_by(Proyecto.id.desc())
    proyectojson=json.dumps([u.to_dict() for u in proyecto])
    return Response(proyectojson, status=201, mimetype='application/json')
  return Response('nombre o descripción sin completar', status=400)

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
  editaProyecto = request.get_json().get('body')
  s = get_db_session()
  proyecto = s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).one_or_none()
  if proyecto != None:
    if editaProyecto.get('nombre') and editaProyecto.get('nombre') != None:
      proyecto.nombre = editaProyecto.get('nombre')
    if editaProyecto.get('descripcion') and editaProyecto.get('descripcion') != None:
      proyecto.descripcion = editaProyecto.get('descripcion')
    if proyecto.nombre == editaProyecto.get('nombre') or proyecto.descripcion == editaProyecto.get('descripcion'):
      s.query(Proyecto).filter(Proyecto.estado==True).filter(Proyecto.id==id).update({Proyecto.descripcion: proyecto.descripcion, Proyecto.nombre: proyecto.nombre})
      s.commit()
      proyecto = s.query(Proyecto).filter(Proyecto.estado==True).order_by(Proyecto.id.desc())
      proyectojson=json.dumps([u.to_dict() for u in proyecto])
      return Response(proyectojson, status=201, mimetype='application/json')
    else:
      return Response('Datos del nombre o descripción vacios', status=400)    
  return Response('Id inexistente en la base de datos', status=404)

@proyecto_api.route('/reportes',methods=['GET'])
def getReporte():
  s = get_db_session()
  proyecto = s.query(Proyecto).from_statement(text("select * from v_ProyectoCount"))
  #proyecto = s.query(Proyecto.descripcion).options(joinedload(func.count(Proyecto.historiales))).filter(Proyecto.estado==True).group_by(Proyecto.descripcion).all()
  #proyecto = s.query(Proyecto).outerjoin(Historia).filter(Proyecto.estado==True).all()
  if proyecto != None:
    proyectojson=json.dumps([u.to_dict() for u in proyecto])
    return Response(proyectojson, status=200, mimetype='application/json')
  return Response('No se puede acceder al reporte en eeste momento', status=404)