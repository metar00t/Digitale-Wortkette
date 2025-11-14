from flask_swagger_ui import *

class SwaggerDoc:
    def __init__(self):
        self.app = None
        self.api = None
        self.swagger_url = None
        self.api_url = None

    def setup(self, app, api, swagger_url, api_url):
        self.app = app
        self.api = api
        self.swagger_url = swagger_url
        self.api_url = api_url

    def setBlueprint(self):
        swaggerUIBlueprint = get_swaggerui_blueprint(
            self.swagger_url,  # Endpoint, an der die Swagger UI Oberflaeche ausgegeben wird
            self.api_url,
            config={  # (Optional) Swagger UI config overrides
                'app_name': "Digitale Wortkette"
            }
        )
        self.app.register_blueprint(swaggerUIBlueprint)

    def addResource(self, model, endpointForModel):
        # Ressourcen fuer die Swagger Dokumentation werden hinzugefuegt
        self.api.add_resource(model, endpointForModel)