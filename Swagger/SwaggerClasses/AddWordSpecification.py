from flask_restful import Resource


class AddWordSpecification(Resource):
    def post(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/Game/AddWordDuringGame.yml
        """
