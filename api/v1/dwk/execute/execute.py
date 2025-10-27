from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import *

from api.v1.dwk.execute.Controller import SwaggerController

app = Flask(__name__)
api = Api(app)

SWAGGER_URL = "/swagger-docs"
API_URL = "/spec"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    })

app.register_blueprint(swaggerui_blueprint)

# Swagger base-path fuer die yml Datei
@app.route("/spec")
def spec():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Digitale Wortkette"
    return jsonify(swag)

# Ressourcen fuer die Swagger Dokumentation
api.add_resource(SwaggerController.SwaggerController,"/temp")

# Hier wird der Main Code stehen, der ausgeführt wird
@app.route("/api/v1/dwk/home")
def start():
    return render_template("landingpage.html")

if __name__ == '__main__':
    app.run(debug = True)