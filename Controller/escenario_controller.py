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

@escenario_api.route('/escenarios/<int:id>',methods=['GET'])
def getEscenario(id):
  s = get_db_session()
  escenario = s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).one_or_none()
  if escenario != None:
    return Response(json.dumps(escenario.to_dict()), status=200, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)

@escenario_api.route('/escenarios',methods=['GET'])
def getListaEscenario():
  s = get_db_session()
  escenario = s.query(Escenario).filter(Escenario.estado==True)
  escenariojson=json.dumps([u.to_dict() for u in escenario])
  return Response(escenariojson, status=200, mimetype='application/json')

@escenario_api.route('/escenarios', methods=['POST'])
def nuevoEscenario():
  nuevoEscenario = request.get_json()#.get('body')
  descripcion = nuevoEscenario['descripcion']
  objetivo = nuevoEscenario['objetivo']
  pre_condicion = nuevoEscenario['pre_condicion']
  pos_condicion = nuevoEscenario['pos_condicion']
  id_historia = nuevoEscenario['id_historia']
  estado = nuevoEscenario['estado']
  escenario = Escenario(descripcion=descripcion ,objetivo=objetivo , pre_condicion=pre_condicion ,pos_condicion=pos_condicion, id_historia=id_historia, estado=estado)  
  s = get_db_session()
  s.add(escenario)
  s.commit()
  return Response(json.dumps(escenario.to_dict()), status=201, mimetype='application/json')

@escenario_api.route('/escenarios/<int:id>', methods=['DELETE'])
def deleteEscenario(id):
  s = get_db_session()
  escenario = s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).one_or_none()
  if escenario != None:
    s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).update({Escenario.estado: False})    
    s.commit()
    return Response('Escenario eliminado de la base de datos', status=200)
  return Response('Id inexistente en la base de datos', status=404)

@escenario_api.route('/escenarios/<int:id>', methods=['PATCH'])
def editarEscenario(id):
  editarEscenario = request.get_json()#.get('body')
  descripcion = editarEscenario['descripcion']
  objetivo = editarEscenario['objetivo']
  pre_condicion = editarEscenario['pre_condicion']
  pos_condicion = editarEscenario['pos_condicion']
  id_historia = editarEscenario['id_historia']
  s = get_db_session()
  escenario = s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).one_or_none()
  if escenario != None:
    if descripcion != None:
      s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).update({Escenario.descripcion: descripcion})
    if objetivo != None:
      s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).update({Escenario.objetivo: objetivo})
    if pre_condicion != None:
      s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).update({Escenario.pre_condicion: pre_condicion})
    if pos_condicion != None:
      s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).update({Escenario.pos_condicion: pos_condicion})
    if id_historia != None:
      s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).update({Escenario.id_historia: id_historia})
    s.commit()
    escenarioUpdate = s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).one_or_none()
    return Response(json.dumps(escenarioUpdate.to_dict()), status=201, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)