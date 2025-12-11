from flask_restful import Resource

class HostSpecification(Resource):
    def post(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/Host/UpdateLobby.yml
        """

    def get(self):
        """
        swagger_from_file: ./Swagger/EndpointDefinitions/Host/CreateLobby.yml
        """