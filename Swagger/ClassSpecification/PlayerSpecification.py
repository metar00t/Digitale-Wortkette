from flask_restful import Resource

class PlayerSpecification(Resource):
    def post(self):
        """
        swagger_from_file: ./Swagger/Endpoints/JoinLobby.yml
        """

    def get(self):
        """
        swagger_from_file: ./Swagger/Endpoints/DisplayLobbySettings.yml
        """