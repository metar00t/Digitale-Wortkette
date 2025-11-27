from flask_restful import Resource

class LobbySpecification(Resource):
    def get(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/CurrentLobby.yml
        """