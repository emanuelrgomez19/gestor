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


@historia_api.route('/historias/<int:id>',methods=['GET'])
def getHistoria(id):
  s = get_db_session()
  historia = s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).one_or_none()
  if historia != None:
    return Response(json.dumps(historia.to_dict()), status=200, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)

@historia_api.route('/historias',methods=['GET'])
def getListaHistoria():
  s = get_db_session()
  historia = s.query(Historia).filter(Historia.estado==True)
  historiajson=json.dumps([u.to_dict() for u in historia])
  return Response(historiajson, status=200, mimetype='application/json')

@historia_api.route('/historias', methods=['POST'])
def nuevoHistoria():
  nuevoHistoria = request.get_json()#.get('body')
  titulo = nuevoHistoria['titulo']
  criterio_aceptacion = nuevoHistoria['criterio_aceptacion']
  como = nuevoHistoria['como']
  para = nuevoHistoria['para']
  id_proyecto = nuevoHistoria['id_proyecto']
  estado = nuevoHistoria['estado']
  historia = Historia(titulo=titulo, criterio_aceptacion=criterio_aceptacion, como=como, para=para, id_proyecto=id_proyecto, estado=estado)
  s = get_db_session()
  s.add(historia)
  s.commit()
  return Response(json.dumps(historia.to_dict()), status=201, mimetype='application/json')

@historia_api.route('/historias/<int:id>', methods=['DELETE'])
def deleteHistoria(id):
  s = get_db_session()
  historia = s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).one_or_none()
  if historia != None:
    s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).update({Historia.estado: False})    
    s.commit()
    return Response('Historia eliminada de la base de datos', status=200)
  return Response('Id inexistente en la base de datos', status=404)

@historia_api.route('/historias/<int:id>', methods=['PATCH'])
def editarHistorias(id):
  editarHistorias = request.get_json()#.get('body')
  titulo = editarHistorias['titulo']
  criterio_aceptacion = editarHistorias['criterio_aceptacion']
  como = editarHistorias['como']
  para = editarHistorias['para']
  id_proyecto = editarHistorias['id_proyecto']
  s = get_db_session()
  historia = s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).one_or_none()
  if historia != None:
    if titulo != None:
      s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).update({Historia.titulo: titulo})
    if criterio_aceptacion != None:
      s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).update({Historia.criterio_aceptacion: criterio_aceptacion})
    if como != None:
      s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).update({Historia.como: como})
    if para != None:
      s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).update({Historia.para: para})
    if id_proyecto != None:
      s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).update({Historia.id_proyecto: id_proyecto})
    s.commit()
    historiaUpdate = s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).one_or_none()
    return Response(json.dumps(historiaUpdate.to_dict()), status=201, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)