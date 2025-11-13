from flask_restful import Resource

class LobbyDoc(Resource):
    def post(self):
        """
        swagger_from_file: ./Swagger/Endpoints/CreateLobby.yml
        """

    def get(self):
        """
        swagger_from_file: ./Swagger/Endpoints/CurrentLobbies.yml
        """