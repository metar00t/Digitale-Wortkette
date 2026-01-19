from flask_swagger_ui import *


class SwaggerDoc:
    def __init__(self):
        self.app = None
        self.api = None
        self.swagger_url = None
        self.api_url = None

    def setup(self, app, api, swagger_url : str, api_url : str) -> None:
        """
        Setup for the use of the Swagger API
        :param app: API Object
        :type app: Any
        :param api: API Object init
        :type api: Any
        :param swagger_url: Endpoint to expose the Swagger API
        :type swagger_url: str
        :param api_url: Enpoint to where the API is being exposed
        :type api_url: str
        :return: Nothing
        :rtype: None
        """
        self.app = app
        self.api = api
        self.swagger_url = swagger_url
        self.api_url = api_url

    def setBlueprint(self) -> None:
        """
        Prepare the Blueprint for the Overlay in Swagger
        :return: Nothing
        :rtype: None
        """
        swaggerUIBlueprint = get_swaggerui_blueprint(
            self.swagger_url,  # Endpoint, an der die Swagger UI Oberflaeche ausgegeben wird
            self.api_url,
            config={  # (Optional) Swagger UI config overrides
                'app_name': "Digitale Wortkette"
            }
        )
        self.app.register_blueprint(swaggerUIBlueprint)

    def addResource(self, model, endpointForModel : str) -> None:
        """
        Add the Resource to display on the Swagger API
        :param model: Class in which the Swagger Doc is being pointed to
        :type model: Any
        :param endpointForModel: Endpoint for Testing with Swagger
        :type endpointForModel: str
        :return: Nothing
        :rtype: None
        """
        # Ressourcen fuer die Swagger Dokumentation werden hinzugefuegt
        self.api.add_resource(model, endpointForModel)
