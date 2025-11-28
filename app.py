from flask import Flask, jsonify, request, redirect, url_for, g
from flask_restful import Api, http_status_message
from flask_swagger import swagger
from logging.handlers import RotatingFileHandler
import logging
import time

from Swagger.SwaggerClasses.HomeSpecification import HomeSpecification
from Swagger.SwaggerClasses.HostSpecification import HostSpecification
from Swagger.SwaggerClasses.LobbySettingSpecification import LobbySettingSpecification
from Swagger.SwaggerClasses.LobbySpecification import LobbySpecification
from Swagger.SwaggerClasses.PlayerSpecification import PlayerSpecification
from Sysfiles.Controller.LobbyController import LobbyController
from Sysfiles.Controller.SwaggerController import SwaggerDoc

app = Flask(__name__)

# Define the Handler
handler = RotatingFileHandler(
    "Logger/Logs/Backend.log",
    maxBytes=10000,
    backupCount=3,
    encoding="utf-8",
)

# Set the LogLevel (Level-Severity is defined in the Documentation) for both in the loglevel variable
loglevel = logging.DEBUG
handler.setLevel(loglevel)
app.logger.setLevel(loglevel)

# Define the Format for Logging
formatter = logging.Formatter(
    "%(asctime)s [%(funcName)s] %(levelname)s %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S"
)
# Set the formatters
handler.setFormatter(formatter)
# Add the handler to the Flask API
app.logger.addHandler(handler)

swaggerInfo = SwaggerDoc()
swaggerInfo.setup(app, Api(app), "/api/v1/dwk/docs", "/api/v1/dwk")
swaggerInfo.setBlueprint()
lobbyController = LobbyController()

# Request Logging
@app.before_request
def start_timer():
    """Store start time for request duration"""
    g.start_time = time.time()
    app.logger.debug(
        f"→ Incoming request: {request.method} {request.path} "
        f"from {request.remote_addr}"
    )

@app.after_request
def log_response(response):
    """Log completed request with duration and status code"""
    duration = round(time.time() - g.start_time, 4)
    app.logger.debug(
        f"← Completed request: {request.method} {request.path} "
        f"status={response.status_code} duration={duration}s"
    )
    return response

# Automatically log exceptions globally
@app.errorhandler(Exception)
def catch_all(e):
    app.logger.exception("Unhandled Exception:")
    return {"error": "Internal Server Error"}, 500


# Swagger Specifications
@app.get("/api/v1/dwk")
def spec():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Digitale Wortkette - FlaskAPI"
    swag['info']['description'] = ("This is the Documentation of the EndpointDefinitions for the Flask-API.\nSome useful links:\n- "
                                   "[The Digitale Wortkette Repository](https://github.com/metar00t/Digitale-Wortkette)")
    swag['info']['contact'] = {
        "email" : "david-paul.adams@outlook.de"
    }
    swag['info']['license'] = {
        "name" : "Repository License",
        "url" : "https://github.com/metar00t/Digitale-Wortkette/blob/main/LICENSE"
    }
    return jsonify(swag)

# Entrypoint
@app.get("/api/v1/dwk/home")
def home():
    if lobbyController.getLobbyList() is None:
        #app.logger.debug("No Lobbies created")
        return {}, 204
    else:
        #app.logger.debug("Lobbies found")
        return lobbyController.getLobbyList(), 200

# Endpoint for Creating a new Lobby
@app.route("/api/v1/dwk/host-lobby", methods=['GET', 'POST'])
def hostLobby():
    # Create a new Lobby with Default Values
    if request.method == 'GET':
        return lobbyController.createLobby(), 201
    # Updating the created Lobby with chosen Values
    if request.method == 'POST':
        lobbyController.saveCurrentLobby()
    return http_status_message(200)

# TODO: Clarify if this Endpoint is still needed / used
@app.get("/api/v1/dwk/join-lobby")
def joinLobby():
    return redirect(url_for('join', lobbyID=lobbyController.getCurrentLobbyID()))

# Endpoint for exposing the chosen Lobbysettings for a specified LobbyID
@app.get("/api/v1/dwk/lobby/<int:lobbyID>/lobbySettings")
def lobbySettings(lobbyID):
    return lobbyController.getChosenLobbySettings(lobbyID)

# Endpoint for exposing the current Playerlist for a specified LobbyID
@app.get("/api/v1/dwk/lobby/<int:lobbyID>/playerList")
def playerList(lobbyID):
    return lobbyController.getPlayerList(lobbyID)

# Endpoint for joining a Lobby with a given LobbyID
@app.post("/api/v1/dwk/lobby/<int:lobbyID>/join")
def join(lobbyID):
    if lobbyController.isPlayerLimitReached(lobbyID):
        return {"message": "Spielerlimit erreicht"}
    else:
        lobbyController.playerJoins(lobbyID)
        return {"message": "Beitritt erfolgreich"}


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

swaggerInfo.addResource(HomeSpecification, "/api/v1/dwk/home")
swaggerInfo.addResource(HostSpecification, "/api/v1/dwk/host-lobby")
swaggerInfo.addResource(LobbySpecification, "/api/v1/dwk/lobby/<int:lobbyID>/playerList")
swaggerInfo.addResource(LobbySettingSpecification, "/api/v1/dwk/lobby/<int:lobbyID>/lobbySettings")
swaggerInfo.addResource(PlayerSpecification, "/api/v1/dwk/lobby/<int:lobbyID>/join")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
