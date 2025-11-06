from flask import Flask, jsonify, request
from flask_restful import Api, http_status_message
from flask_swagger import swagger

from Model.User import User
from api.v1.dwk.execute.Model.Lobby import Lobby
from swagger.classes.userdoc import UserDoc
from Controller.SwaggerController import SwaggerDoc

app = Flask(__name__)

swaggerinfo = SwaggerDoc(app, Api(app), "/swagger", "/spec")
swaggerinfo.setup()
swaggerinfo.addResource(UserDoc, "/")

@app.route("/spec")
def spec():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Digitale Wortkette"
    return jsonify(swag)

# Hier wird der Main Code stehen, der ausgeführt wird
@app.get("/home")
def home():
    lobby = Lobby(5540,"john","Tiere",0)
    #lobby2 = Lobby(5541, "jane", "Pflanzen", 4)
    return jsonify(lobby.getLobbyInfo())

if __name__ == '__main__':
    app.run(debug = True)