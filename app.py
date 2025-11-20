from flask import Flask, jsonify, request, redirect, url_for
from flask_restful import Api, http_status_message
from flask_swagger import swagger

from Swagger.ClassSpecification.PlayerSpecification import PlayerSpecification
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

@app.get("/api/v1/dwk/home")
def home():
    return lobbyController.getLobbyList()

@app.route("/api/v1/dwk/host-lobby", methods=['GET', 'POST'])
def hostLobby():
    if request.method == 'GET':
        return lobbyController.createLobby(), 201
    if request.method == 'POST':
        lobbyController.saveCurrentLobby()
    return http_status_message(200)

@app.get("/api/v1/dwk/join-lobby")
def joinLobby():
    return redirect(url_for('join', lobbyID=lobbyController.getCurrentLobbyID()))

@app.get("/api/v1/dwk/lobby/<int:lobbyID>/lobbySettings")
def lobbySettings(lobbyID):
    return lobbyController.getChosenLobbySettings(lobbyID)

@app.get("/api/v1/dwk/lobby/<int:lobbyID>/playerList")
def playerList(lobbyID):
    return lobbyController.getPlayerList(lobbyID)

@app.post("/api/v1/dwk/lobby/<int:lobbyID>/join")
def join(lobbyID):
    lobbyController.playerJoins(lobbyID)
    return {"message" : "Beitritt erfolgreich"}

@app.post("/api/v1/dwk/start-game")
def startGame():
    lobbyController.setGameStatus()
    return redirect(url_for('game'))

@app.route("/api/v1/dwk/game", methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        return lobbyController.gameSession()
    if request.method == 'POST':
        result = lobbyController.checkInput()
        if result:
            return lobbyController.addWord(result)
        else:
            return {}

swaggerInfo.addResource(HostSpecification, "/api/v1/dwk/host-lobby")
swaggerInfo.addResource(LobbySpecification, "/api/v1/dwk/lobby/")
swaggerInfo.addResource(PlayerSpecification, "/api/v1/dwk/join-lobby")

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')