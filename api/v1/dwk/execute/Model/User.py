from flask_restful import Resource

class UserModel(Resource):
    def get(self):
        """
        swagger_from_file: api-documentation/specs.yml
        """