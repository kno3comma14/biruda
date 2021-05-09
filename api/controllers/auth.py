from flask_restful import reqparse, abort, Resource

from api.models.models import User
from api.utils.errors import ValidationError

class AuthLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='You need to enter your e-mail address', required=True)
        parser.add_argument('password', type=str, help='You need to enter your password', required=True)
        
        args = parser.parse_args()
        
        email = args.get('email')
        password = args.get('password')
        
        try:
            token = User.validate(email, password)
            return {'token': token}
        except ValidationError as e:
            abort(400, message='There was an error while trying to log you in -> {}'.format(e.message))

class AuthRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, help='You need to enter your fistname', required=True)
        parser.add_argument('lastname', type=str, help='You need to enter your lastname', required=True)
        parser.add_argument('email', type=str, help='You need to enter your e-mail address', required=True)
        parser.add_argument('password', type=str, help='You need to enter your chosen password', required=True)
        parser.add_argument('confirmation_password', type=str, help='You need to enter the confirm password field', required=True)
        
        args = parser.parse_args()
        
        email = args.get('email')
        password = args.get('password')
        confirmation_password = args.get('confirmation_password')
        firstname = args.get('firstname')
        lastname = args.get('lastname')
        
        try:
            User.create(
                email=email,
                password=password,
                confirmation_password=confirmation_password,
                firstname=firstname,
                lastname=lastname
            )
            return {'message': 'Successfully created your account.'}
        except ValidationError as e:
            abort(400, message='There was an error while trying to create your account -> {}'.format(e.message))



