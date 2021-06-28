from re import escape
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
  print(escenario)
  if escenario != None:
    return Response(json.dumps(escenario.to_dict()), status=200, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)

@escenario_api.route('/escenarios',methods=['GET'])
def getListaEscenario():
  s = get_db_session()
  escenario = s.query(Escenario).filter(Escenario.estado==True).order_by(Escenario.id.desc())
  escenariojson=json.dumps([u.to_dict() for u in escenario])
  return Response(escenariojson, status=200, mimetype='application/json')

@escenario_api.route('/escenarios', methods=['POST'])
def nuevoEscenario():
  nuevoEscenario = request.get_json().get('body')
  print(nuevoEscenario)
  escenario = Escenario(descripcion=nuevoEscenario.get('descripcion') ,objetivo=nuevoEscenario.get('objetivo') , pre_condicion=nuevoEscenario.get('pre_condicion') ,pos_condicion=nuevoEscenario.get('pos_condicion'), id_historia=nuevoEscenario.get('id_historia'), estado=True)
  if escenario.descripcion and escenario.descripcion != None and escenario.objetivo and escenario.objetivo != None and escenario.pre_condicion and escenario.pre_condicion != None and escenario.pos_condicion and escenario.pos_condicion != None and escenario.id_historia and escenario.id_historia != None:
    s = get_db_session()
    s.add(escenario)
    s.commit()
    escenario = s.query(Escenario).filter(Escenario.id_historia==escenario.id_historia).filter(Escenario.estado==True).order_by(Escenario.id.desc())
    escenariojson=json.dumps([u.to_dict() for u in escenario])
    return Response(escenariojson, status=201, mimetype='application/json')
  return Response("Campos incompletos para crear una historia", status=400)

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
  editarEscenario = request.get_json().get('body')
  s = get_db_session()
  escenario = s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id==id).one_or_none()
  if escenario != None:
    if editarEscenario.get('descripcion') and editarEscenario.get('descripcion') != None:
      escenario.descripcion = editarEscenario.get('descripcion')
    if editarEscenario.get('objetivo') and editarEscenario.get('objetivo') != None:
      escenario.objetivo = editarEscenario.get('objetivo')
    if editarEscenario.get('pre_condicion') and editarEscenario.get('pre_condicion') != None:
      escenario.pre_condicion = editarEscenario.get('pre_condicion')
    if editarEscenario.get('pos_condicion') and editarEscenario.get('pos_condicion') != None:
      escenario.pos_condicion = editarEscenario.get('pos_condicion')
    if editarEscenario.get('id_historia') and editarEscenario.get('id_historia') != None:
      escenario.id_historia = editarEscenario.get('id_historia')
    if escenario.descripcion == editarEscenario.get('descripcion') or escenario.objetivo == editarEscenario.get('objetivo') or escenario.pre_condicion == editarEscenario.get('pre_condicion') or escenario.pos_condicion == editarEscenario.get('pos_condicion') or escenario.id_historia == editarEscenario.get('id_historia'):
      s.query(Escenario).filter(Escenario.id==id).update({Escenario.descripcion: escenario.descripcion, Escenario.objetivo: escenario.objetivo, Escenario.pre_condicion: escenario.pre_condicion, Escenario.pos_condicion: escenario.pos_condicion, Escenario.id_historia: escenario.id_historia})
      s.commit()
      escenario = s.query(Escenario).filter(Escenario.id_historia==escenario.id_historia).filter(Escenario.estado==True).order_by(Escenario.id.desc())
      escenariojson=json.dumps([u.to_dict() for u in escenario])
      return Response(escenariojson, status=201, mimetype='application/json')
    else:
      return Response('Datos del escenario vacios', status=400) 
  return Response('Id inexistente en la base de datos', status=404)

@escenario_api.route('/escenariohistoria/<int:id>',methods=['GET'])
def getListaEscenario_historia(id):
  s = get_db_session()
  escenario = s.query(Escenario).filter(Escenario.estado==True).filter(Escenario.id_historia==id)
  historiajson=json.dumps([u.to_dict() for u in escenario])
  return Response(historiajson, status=200, mimetype='application/json')