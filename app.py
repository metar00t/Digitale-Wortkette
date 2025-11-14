from flask import Flask, jsonify, request, redirect
from flask_restful import Api, http_status_message
from flask_swagger import swagger

from Sysfiles.Controller.LobbyController import LobbyController
from Swagger.ClassSpecification.HostSpecification import HostSpecification
from Swagger.ClassSpecification.LobbySpecification import LobbySpecification
from Sysfiles.Controller.SwaggerController import SwaggerDoc

app = Flask(__name__)

swaggerInfo = SwaggerDoc()
swaggerInfo.setup(app, Api(app), "/api/v1/dwk/docs", "/api/v1/dwk/spec")
swaggerInfo.setBlueprint()
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
        lobbyController.setLobbySettings()
        return lobbyController.createLobby(), 201
    if request.method == 'GET':
        return lobbyController.getPlayerList()
    return http_status_message(418)

@app.route("/api/v1/dwk/join-lobby", methods=['GET', 'POST'])
def joinLobby():
    if request.method == 'GET':
        return lobbyController.getChosenLobbySettings()
    if request.method == 'POST':
        return lobbyController.playerJoins()
    return http_status_message(200)

@app.get("/api/v1/dwk/home")
def home():
    return lobbyController.getLobbyList()

@app.get("/api/v1/dwk/lobby/")
def lobby():
    return lobbyController.getPlayerList()

swaggerInfo.addResource(HostSpecification, "/api/v1/dwk/host-lobby")
swaggerInfo.addResource(LobbySpecification, "/api/v1/dwk/lobby/")

if __name__ == '__main__':
    app.run(debug = True)