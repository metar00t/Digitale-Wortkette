from flask_restful import Resource

class PlayerLeaves(Resource):
    def post(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/Player/PlayerLeavesLobby.yml
        """