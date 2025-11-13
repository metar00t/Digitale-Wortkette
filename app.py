from flask import Flask, jsonify, request
from flask_restful import Api, http_status_message
from flask_swagger import swagger

from Sysfiles.Controller.LobbyController import LobbyController
from Swagger.ClassSpecification.LobbyDoc import LobbyDoc
from Sysfiles.Controller.SwaggerController import SwaggerDoc

app = Flask(__name__)

swaggerInfo = SwaggerDoc(app, Api(app), "/api/v1/dwk/docs", "/api/v1/dwk/spec")
swaggerInfo.setup()
lobbyController = LobbyController()

@app.get("/api/v1/dwk/spec")
def spec():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Digitale Wortkette"
    return jsonify(swag)

@app.route("/api/v1/dwk/host-lobby", methods=['GET', 'POST'])
def hostLobby():
    if request.method == 'POST':
        return lobbyController.createLobby()
    if request.method == 'GET':
        return lobbyController.getPlayerList()
    return http_status_message(200)

swaggerInfo.addResource(LobbyDoc, "/api/v1/dwk/host-lobby")

@app.route("/api/v1/dwk/join-lobby", methods=['GET', 'POST'])
def joinLobby():
    if request.method == 'GET':
        return lobbyController.getLobbySettings()
    if request.method == 'POST':
        return lobbyController.playerJoins()
    return http_status_message(200)

@app.get("/api/v1/dwk/home")
def home():
    return lobbyController.getLobbyList()

@app.get("/api/v1/dwk/lobby/")
def lobby():
    return lobbyController.getPlayerList()

if __name__ == '__main__':
    app.run(debug = True)