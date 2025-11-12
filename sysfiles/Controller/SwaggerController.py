from flask_swagger_ui import *

class SwaggerDoc:
    def __init__(self, app, api, swagger_url, api_url):
        self.app = app
        self.api = api
        self.swagger_url = swagger_url
        self.api_url = api_url

    def setup(self):
        swaggerui_blueprint = get_swaggerui_blueprint(
            self.swagger_url,  # Endpoint, an der die Swagger UI Oberflaeche ausgegeben wird
            self.api_url,
            config={  # (Optional) Swagger UI config overrides
                'app_name': "Digitale Wortkette"
            }
        )
        self.app.register_blueprint(swaggerui_blueprint)

    def addResource(self, model, endpointformodel):
        # Ressourcen fuer die Swagger Dokumentation werden hinzugefuegt
        self.api.add_resource(model, endpointformodel)