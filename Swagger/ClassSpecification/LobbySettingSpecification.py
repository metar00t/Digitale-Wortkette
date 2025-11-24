from flask_restful import Resource

class LobbySettingSpecification(Resource):
    def get(self):
        """
        swagger_from_file: ./Swagger/Endpoints/DisplayLobbySettings.yml
        """