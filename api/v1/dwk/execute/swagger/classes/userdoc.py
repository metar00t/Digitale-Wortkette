from flask_restful import Resource

class UserDoc(Resource):
    def get(self):
        """
        swagger_from_file: endpoint-documentation/user_specification.yml
        """