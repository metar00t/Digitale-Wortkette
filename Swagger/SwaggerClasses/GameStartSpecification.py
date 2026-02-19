from flask_restful import Resource


class GameStartSpecification(Resource):
    def get(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/Game/StartGame.yml
        """
