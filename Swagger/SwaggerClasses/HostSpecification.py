from flask_restful import Resource

class HostSpecification(Resource):
    def post(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/UpdateLobby.yml
        """

    def get(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/CreateLobby.yml
        """