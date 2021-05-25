from flask import Blueprint, Flask, request, json, Response
from Model.ciudad_model import Ciudad

from database import get_db_session


ciudad_api = Blueprint('ciudad_api', __name__)


@ciudad_api.route('/ciudades')
def getCiudades():
  s = get_db_session()
  ciudad = s.query(Ciudad)
  return Response(json.dumps([u.to_dict() for u in ciudad]), status=200, mimetype='application/json')