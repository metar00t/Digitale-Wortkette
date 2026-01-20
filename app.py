import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, redirect, url_for, g
from flask_restful import Api
from flask_swagger import swagger

from Config.config import Config
from Swagger.SwaggerClasses.HomeSpecification import HomeSpecification
from Swagger.SwaggerClasses.HostSpecification import HostSpecification
from Swagger.SwaggerClasses.LobbySettingSpecification import LobbySettingSpecification
from Swagger.SwaggerClasses.LobbySpecification import LobbySpecification
from Swagger.SwaggerClasses.PlayerSpecification import PlayerSpecification
from Sysfiles.Controller.GameController import GameController
from Sysfiles.Controller.LobbyController import LobbyController
from Sysfiles.Controller.PlayerController import PlayerController
from Sysfiles.Controller.SwaggerController import SwaggerDoc

app = Flask(__name__)
app.config.from_object(Config)

# Define the Handler
handler = RotatingFileHandler(
    app.config["LOG_FILE"],
    backupCount=app.config["LOG_BACKUP_COUNT"],
    encoding=app.config["LOG_ENCODING"],
)

# Set the LogLevel (Level-Severity is defined in the Documentation) for both in the loglevel variable
loglevel = app.config["LOG_LEVEL"]
handler.setLevel(loglevel)
app.logger.setLevel(loglevel)

# Define the Format for Logging
formatter = logging.Formatter(
    app.config["LOG_FORMAT"],
    datefmt=app.config["LOG_DATEFORMAT"]
)

# Set the formatter
handler.setFormatter(formatter)
# Add Log handler to Flask
app.logger.addHandler(handler)

# --- Swagger Setup ---
swaggerInfo = SwaggerDoc()
swaggerInfo.setup(app, Api(app), "/api/v1/dwk/docs", "/api/v1/dwk")
swaggerInfo.setBlueprint()

# --- Controller Classes ---
lobbyController = LobbyController()
playerController = PlayerController(lobbyController)
gameController = GameController(playerController)


# --- Log incoming requests ---
@app.before_request
def incoming_request():
    """Store start time for request duration"""
    g.start_time = time.time()
    app.logger.debug(
        f"→ Incoming request: {request.method} {request.path} "
        f"from {request.remote_addr}"
    )


# --- Log processed requests ---
@app.after_request
def log_response(response):
    """Log completed request with duration and status code"""
    duration = round(time.time() - g.start_time, 4)
    app.logger.debug(
        f"← Completed request: {request.method} {request.path} "
        f"status={response.status_code} duration={duration}s"
    )
    return response


# --- Global Error Logging ---
@app.errorhandler(Exception)
def handle_unhandled_exception(e):
    """Log any uncaught exception with traceback"""
    app.logger.exception(
        f"Unhandled Exception in {request.method} {request.path}: {e}"
    )
    return {"error": "Internal Server Error"}, 500


# Swagger Specifications
@app.get("/api/v1/dwk")
def spec():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Digitale Wortkette - FlaskAPI"
    swag['info']['description'] = (
        "This is the Documentation of the EndpointDefinitions for the Flask-API.\nSome useful links:\n- "
        "[The Digitale Wortkette Repository](https://github.com/metar00t/Digitale-Wortkette)")
    swag['info']['contact'] = {
        "email": "david-paul.adams@outlook.de"
    }
    swag['info']['license'] = {
        "name": "Repository License",
        "url": "https://github.com/metar00t/Digitale-Wortkette/blob/main/LICENSE"
    }
    return jsonify(swag)


# Entrypoint
@app.get("/api/v1/dwk/home")
def home():
    if lobbyController.getLobbyList() is None:
        # app.logger.debug("No Lobbies created")
        return {}, 204
    else:
        # app.logger.debug("Lobbies found")
        return lobbyController.getLobbyList(), 200


# Endpoint for Creating a new Lobby
@app.route("/api/v1/dwk/host/host-lobby", methods=['GET', 'POST'])
def hostLobby():
    # Create a new Lobby with Default Values
    if request.method == 'GET':
        return lobbyController.createLobby(), 201
    # Updating the created Lobby with chosen Values
    if request.method == 'POST':
        lobbyController.updateLobby()
    return {"status": "OK"}


# Endpoint for exposing the chosen Lobby-Settings for a specified LobbyID
@app.get("/api/v1/dwk/lobby/<int:lobbyID>/lobbySettings")
def lobbySettings(lobbyID: int) -> dict[str,int]:
    return lobbyController.getChosenLobbySettings(lobbyID)


# Endpoint for exposing the current Playerlist for a specified LobbyID
@app.get("/api/v1/dwk/lobby/<int:lobbyID>/playerList")
def playerList(lobbyID: int):
    return lobbyController.getListOfPlayers(lobbyID)


# Endpoint for joining a Lobby with a given LobbyID
@app.post("/api/v1/dwk/player/<int:lobbyID>/join")
def join(lobbyID: int) -> dict[str,str] | dict[str,int]:
    userID = request.form.get('userID')
    if lobbyController.isPlayerLimitReached(lobbyID):
        return {"message": "Spielerlimit erreicht"}
    else:
        return playerController.playerJoins(lobbyID, int(userID))


# Endpoint for Leaving the Lobby
@app.post("/api/v1/dwk/player/<int:lobbyID>/leave")
def leave(lobbyID: int) -> dict[str, str] | None:
    hostID = request.form.get('hostID')
    userID = request.form.get('userID')
    if int(hostID) == 0:  # Gets called when a Player is leaving
        playerController.removePlayer(lobbyID, int(userID))
        return {"message": f"Lobby #{lobbyID} wurde verlassen"}
    if int(hostID) > 0:  # Gets called when the Host leaves the Lobby (Close Lobby)
        lobbyController.closeLobby(lobbyID, int(hostID))
        return {"message": f"Lobby #{lobbyID} wurde geschlossen"}
    return None


@app.post("/api/v1/dwk/start-game")
def startGame():
    gameController.setGameStatus()
    return redirect(url_for('game'))


@app.route("/api/v1/dwk/game", methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        return gameController.gameSession()
    if request.method == 'POST':
        result = gameController.checkInput()
        if result:
            return gameController.addWord(result)
        else:
            return {}
    return None  # Temporary Return Statement


# Add Resources to Swagger
swaggerInfo.addResource(HomeSpecification, "/api/v1/dwk/home")
swaggerInfo.addResource(HostSpecification, "/api/v1/dwk/host/host-lobby")
swaggerInfo.addResource(LobbySpecification, "/api/v1/dwk/lobby/<int:lobbyID>/playerList")
swaggerInfo.addResource(LobbySettingSpecification, "/api/v1/dwk/lobby/<int:lobbyID>/lobbySettings")
swaggerInfo.addResource(PlayerSpecification, "/api/v1/dwk/player/<int:lobbyID>/join")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
