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
  historia = s.query(Historia).filter(Historia.estado==True).order_by(Historia.id.desc())
  historiajson=json.dumps([u.to_dict() for u in historia])
  return Response(historiajson, status=200, mimetype='application/json')

@historia_api.route('/historias', methods=['POST'])
def nuevoHistoria():
  nuevoHistoria = request.get_json().get('body')
  historia = Historia(titulo=nuevoHistoria.get('titulo'), criterio_aceptacion=nuevoHistoria.get('criterio_aceptacion'), como=nuevoHistoria.get('como'), para=nuevoHistoria.get('para'), id_proyecto=nuevoHistoria.get('id_proyecto'), estado=True)
  if historia.titulo and historia.titulo != None and historia.criterio_aceptacion and historia.criterio_aceptacion != None and historia.como and historia.como != None and historia.para and historia.para != None and historia.id_proyecto and historia.id_proyecto != None:
    s = get_db_session()
    s.add(historia)
    s.commit()  
    historia = s.query(Historia).filter(Historia.estado==True).filter(Historia.id_proyecto==historia.id_proyecto).order_by(Historia.id.desc())
    historiajson=json.dumps([u.to_dict() for u in historia])
    return Response(historiajson, status=201, mimetype='application/json')
  return Response("Campos incompletos para crear una historia", status=400)

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
  s = get_db_session()
  historia = s.query(Historia).filter(Historia.estado==True).filter(Historia.id==id).one_or_none()
  if historia != None:
    if editarHistorias.get('titulo') and editarHistorias.get('titulo') != None:
      historia.titulo = editarHistorias.get('titulo')
    if editarHistorias.get('criterio_aceptacion') and editarHistorias.get('criterio_aceptacion') != None:
      historia.criterio_aceptacion = editarHistorias.get('criterio_aceptacion')
    if editarHistorias.get('como') and editarHistorias.get('como') != None:
      historia.como = editarHistorias.get('como')
    if editarHistorias.get('para') and editarHistorias.get('para') != None:
      historia.para = editarHistorias.get('para')
    if editarHistorias.get('id_proyecto') and editarHistorias.get('id_proyecto') != None:
      historia.id_proyecto = editarHistorias.get('id_proyecto')
    if historia.titulo == editarHistorias.get('titulo') or historia.criterio_aceptacion == editarHistorias.get('criterio_aceptacion') or historia.como == editarHistorias.get('como') or historia.para == editarHistorias.get('para') or historia.id_proyecto == editarHistorias.get('id_proyecto'):
      s.query(Historia).filter(Historia.id==id).update({Historia.titulo: historia.titulo, Historia.criterio_aceptacion: historia.criterio_aceptacion, Historia.como: historia.como, Historia.para: historia.para, Historia.id_proyecto: historia.id_proyecto})
      s.commit()
      historia = s.query(Historia).filter(Historia.estado==True).filter(Historia.id_proyecto==historia.id_proyecto).order_by(Historia.id.desc())
      historiajson=json.dumps([u.to_dict() for u in historia])
      return Response(historiajson, status=201, mimetype='application/json')
    else:
      return Response('Datos necesarios de la historia vacios', status=400) 
  return Response('Id inexistente en la base de datos', status=404)

@historia_api.route('/historiasproyecto/<int:id>',methods=['GET'])
def getListaHistoria_proyecto(id):
  s = get_db_session()
  historia = s.query(Historia).filter(Historia.estado==True).filter(Historia.id_proyecto==id)
  historiajson=json.dumps([u.to_dict() for u in historia])
  return Response(historiajson, status=200, mimetype='application/json')