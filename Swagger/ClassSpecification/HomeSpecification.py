from flask_restful import Resource

class HomeSpecification(Resource):
    def get(self):
        """
        swagger_from_file: ./Swagger/Endpoints/ActiveLobbies.yml
        """