from flask import Flask, request, json, Response
from Utils.utils import ToDict

from database import setup_database

from Controller.user_controller import user_api
from Controller.proyecto_controller import proyecto_api
from Controller.historia_controller import historia_api
from Controller.escenario_controller import escenario_api

app = Flask(__name__)
app.debug = True

app.register_blueprint(user_api)
app.register_blueprint(proyecto_api)
app.register_blueprint(historia_api)
app.register_blueprint(escenario_api)

if __name__ == '__main__':
  setup_database(app)
  app.run('localhost', port=8081)