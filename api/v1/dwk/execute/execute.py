from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_swagger import swagger

from Model.User import *
from Controller.SwaggerController import SwaggerDoc

app = Flask(__name__)

swaggerinfo = SwaggerDoc(app, Api(app), "/swagger-docs", "/spec")
swaggerinfo.setup()
swaggerinfo.addResource(UserModel, "/temp")

# Swagger base-path fuer die yml Datei
@app.route("/spec")
def spec():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Digitale Wortkette"
    return jsonify(swag)

# Hier wird der Main Code stehen, der ausgeführt wird
@app.route("/api/v1/dwk/home")
def start():
    return render_template("landingpage.html")

if __name__ == '__main__':
    app.run(debug = True)