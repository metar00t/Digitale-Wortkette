from flask_restful import Resource

class PlayerSpecification(Resource):
    def post(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/Player/RegisterPlayerToLobby.yml
        """