  
from flask import Blueprint, Flask, request, json, Response, jsonify
from Model.user_model import User
from database import get_db_session
from webargs import fields, validate
from webargs.flaskparser import use_args
from sqlalchemy.orm.exc import NoResultFound

user_api = Blueprint('user_api', __name__)

create_user_request = {
  "username": fields.Str(required=True, validate=validate.Length(min=1)),
  "firstname": fields.Str(required=True, validate=validate.Length(min=1)),
  "lastname": fields.Str(required=True, validate=validate.Length(min=1))
}

patch_user_request = {
  "username": fields.Str(validate=validate.Length(min=1)),
  "firstname": fields.Str(validate=validate.Length(min=1)),
  "lastname": fields.Str(validate=validate.Length(min=1))
}

# Return validation errors as JSON
@user_api.errorhandler(422)
@user_api.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

@user_api.route('/user/<int:id>',methods=['GET'])
def getUsuario(id):
  s = get_db_session()
  user = s.query(User).filter(User.estado==True).filter(User.id==id).one_or_none()
  if user != None:
    return Response(json.dumps(user.to_dict()), status=200, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)

@user_api.route('/user',methods=['GET'])
def list_user():
  s = get_db_session()
  users = s.query(User).filter(User.estado==True)
  usersjson=json.dumps([u.to_dict() for u in users])
  return Response(usersjson, status=200, mimetype='application/json')

@user_api.route('/user', methods=['POST'])
def nuevoUser():
  nuevoUser = request.get_json()#.get('body')
  username = nuevoUser['username']
  firstname = nuevoUser['firstname']
  lastname = nuevoUser['lastname']
  estado = nuevoUser['estado']
  user = User(username=username, firstname=firstname, lastname=lastname, estado=estado)
  s = get_db_session()
  s.add(user)
  s.commit()
  return Response(json.dumps(user.to_dict()), status=201, mimetype='application/json')

@user_api.route('/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
  s = get_db_session()
  user = s.query(User).filter(User.estado==True).filter(User.id==id).one_or_none()
  if user != None:
    s.query(User).filter(User.estado==True).filter(User.id==id).update({User.estado: False})    
    s.commit()
    return Response('Usuario eliminado de la base de datos', status=200)
  return Response('Id inexistente en la base de datos', status=404)

@user_api.route('/user/<int:id>', methods=['PATCH'])
def editarUser(id):
  editarUser = request.get_json()#.get('body')
  username = editarUser['username']
  firstname = editarUser['firstname']
  lastname = editarUser['lastname']
  estado = editarUser['estado']
  s = get_db_session()
  user = s.query(User).filter(User.estado==True).filter(User.id==id).one_or_none()
  if user != None:
    if username != None:
      s.query(User).filter(User.estado==True).filter(User.id==id).update({User.username: username})
    if firstname != None:
      s.query(User).filter(User.estado==True).filter(User.id==id).update({User.firstname: firstname})
    if lastname != None:
      s.query(User).filter(User.estado==True).filter(User.id==id).update({User.lastname: lastname})
    if estado != None:
      s.query(User).filter(User.estado==True).filter(User.id==id).update({User.estado: estado})
    s.commit()
    userUpdate = s.query(User).filter(User.estado==True).filter(User.id==id).one_or_none()
    return Response(json.dumps(userUpdate.to_dict()), status=201, mimetype='application/json')
  return Response('Id inexistente en la base de datos', status=404)

